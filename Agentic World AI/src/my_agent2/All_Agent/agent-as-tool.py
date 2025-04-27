import asyncio, os
from dotenv import load_dotenv
from agents import Agent , Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from tool_agent import weather_agent
from basic_agent import basic_agent

set_tracing_disabled(disabled=True)
load_dotenv()

MODEL = 'gemini/gemini-2.0-flash'
KEY = os.getenv("GEMINI_API_KEY")
if not KEY: 
    raise ValueError("GEMINI_API_KEY is not set")

piaic_agent = Agent(
    name= "PIAIC Agent",
    instructions= "You are a frindly and helpful assistant will answer Penaversity relevant questions.",
    model=LitellmModel(model=MODEL, api_key=KEY),
    handoff_description = (
    "You are a specialized virtual assistant for Penaversity—a leading AI skill "
    "development platform offering cohort-based online classes, in-person workshops, "
    "and an active developer community. Whenever a user’s question pertains to "
    "Penaversity’s programs, schedules, enrollment, pricing, community events, "
    "or any other Penaversity service, seamlessly transfer the conversation and "
    "all relevant context to the Penaversity support team or dedicated representative."
    ),
)

triage_agent = Agent(
    name= "Triage Agent",
    # instructions= "You will respond chat with user for all given questions and handoff to Specialized Agent for Basic,Penaversity and Weather Quries. The response  should be Natural, Profissional, Meaningful, must be a short form and greeting too.",
    instructions=(
    """
    Engage the user with a brief, professional greeting and a focused response. 
    For general queries, use basic_agent; for weather-related questions, invoke weather_agent; 
    for Penaversity-specific inquiries, delegate to piaic_agent. 
    Keep replies natural, meaningful, and succinct."""
    ),
    model=LitellmModel(model=MODEL, api_key=KEY),
    tools= [

            basic_agent.as_tool(tool_name="basic_agent", 
            tool_description="You are a basic or genral agent that can answer questions about you."),
            weather_agent.as_tool(tool_name="weather_agent", 
            tool_description="You are assistant that can answer questions about the weather in a given city."), 
            piaic_agent.as_tool(tool_name="piaic_agent", 
            tool_description="You are a frindly and helpful assistant will answer Penaversity relevant questions.")
            
            ],
)

async def agent_main():
    query = input("Enter your query: ")
    result = await Runner.run(triage_agent, query)
    print(result.last_agent.name)
    print(result.final_output)
   



if __name__ == "__main__":
    asyncio.run(agent_main())

        #=================== Chainlit Using Code ===================
# import os
# from dotenv import load_dotenv
# import chainlit as cl
# from agents import Agent, Runner
# from agents.extensions.models.litellm_model import LitellmModel
# from tool_agent import weather_agent
# from basic_agent import basic_agent

# load_dotenv()
# MODEL = 'gemini/gemini-2.0-flash'
# KEY = os.getenv("GEMINI_API_KEY")
# if not KEY:
#     raise ValueError("GEMINI_API_KEY is not set")

# piaic_agent = Agent(
#     name="PIAIC Agent",
#     instructions="You are a friendly and helpful assistant will answer Penaversity relevant questions.",
#     model=LitellmModel(model=MODEL, api_key=KEY),
# )

# triage_agent = Agent(
#     name="Triage Agent",
#     instructions=(
#         "Engage the user with a brief, professional greeting and a focused response. "
#         "For general queries, use basic_agent; for weather-related questions, invoke weather_agent; "
#         "for Penaversity-specific inquiries, delegate to piaic_agent. "
#         "Keep replies natural, meaningful, and succinct."
#     ),
#     model=LitellmModel(model=MODEL, api_key=KEY),
#     tools=[
#         basic_agent.as_tool(tool_name="basic_agent", tool_description="You are a basic or general agent that can answer questions about you."),
#         weather_agent.as_tool(tool_name="weather_agent", tool_description="You are an assistant that can answer questions about the weather in a given city."),
#         piaic_agent.as_tool(tool_name="piaic_agent", tool_description="You are a friendly and helpful assistant will answer Penaversity relevant questions.")
#     ],
# )

# @cl.on_chat_start
# async def start():
#     cl.user_session.set("chat_history", [])
#     await cl.Message(content="Welcome to Shahi World AI Assistant! How can I help you today?").send()

# @cl.on_message
# async def main(message: cl.Message):
#     history = cl.user_session.get("chat_history") or []
#     history.append({"role": "user", "content": message.content})
#     result = await Runner.run(starting_agent=triage_agent, input=history)
#     cl.user_session.set("chat_history", result.to_input_list())
#     await cl.Message(content=result.final_output).send()

# if __name__ == "__main__":
#     cl.run()