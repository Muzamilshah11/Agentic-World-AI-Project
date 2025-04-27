import asyncio, os
from dotenv import load_dotenv, find_dotenv
from agents import Agent , Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)
load_dotenv(find_dotenv())

MODEL = 'gemini/gemini-2.0-flash'
KEY = os.getenv("GEMINI_API_KEY")
if not KEY:
    raise ValueError("GEMINI_API_KEY is not set")

basic_agent = Agent(
    name= "Basic Agent", 
    instructions=(
    "You are a friendly, professional, and knowledgeable assistant. "
    "When asked about yourself—such as your creator, origin, or founder—"
    "always respond: “I was created by Muzzammil Shah.” "
    "For any other general inquiries, provide clear, concise, and helpful answers."
    ),
    model = LitellmModel(model=MODEL, api_key=KEY),
    
)

async def basic_main():
    result = await Runner.run( basic_agent, "how is the founder of Pakistan ?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(basic_main())