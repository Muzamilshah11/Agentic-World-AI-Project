import asyncio, os 
from dotenv import load_dotenv
from litellm import completion
from agents import Agent , Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

# from agents import enable_verbose_stdout_logging

# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
load_dotenv()   

MODEL = 'gemini/gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

@function_tool
def weather(city: str) -> str:
    """
    Expert weather poet: fetch current conditions for the given city, then craft
    a vivid, accurate haiku that captures its atmosphere.
    """
    print(f"[debug] getting weather for {city}")
    response = completion(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly, professional assistant. "
                    "Greet the user warmly, then deliver exactly one haiku "
                    "describing the current weather in the specified city."
                )
            },
            {"role": "user", "content": f"Write a weather haiku for {city}."}
        ],
        api_key=GEMINI_API_KEY
    )
    return response["choices"][0]["message"]["content"].strip()

weather_agent = Agent(
    name="Weather Agent",
    instructions=(
        "You are a concise, expert assistant. "
        "Always start with a brief greeting, then produce one precise haiku "
        "that reflects the city’s current weather—no extra commentary."
    ),
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    tools=[weather]
)

async def tool_main():
    query = input("Enter your query: ")
    result = await Runner.run(weather_agent, query)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(tool_main())