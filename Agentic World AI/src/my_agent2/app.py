# Befor the run must add $env:PYHONPATH=1 in Termainal then the below command
# chainlit run src/my_agent2/app.py -w
import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from my_agent2.All_Agent.tool_agent import weather_agent
from my_agent2.All_Agent.basic_agent import basic_agent


load_dotenv()
MODEL = 'gemini/gemini-2.0-flash'
KEY = os.getenv("GEMINI_API_KEY")
if not KEY:
    raise ValueError("GEMINI_API_KEY is not set")

piaic_agent = Agent(
    name="PIAIC Agent",
    instructions="You are a friendly and helpful assistant will answer Penaversity relevant questions.",
    model=LitellmModel(model=MODEL, api_key=KEY),
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Engage the user with a brief, professional greeting and a focused response. "
        "For general queries, use basic_agent; for weather-related questions, invoke weather_agent; "
        "for Penaversity-specific inquiries, delegate to piaic_agent. "
        "Keep replies natural, meaningful, and succinct."
    ),
    model=LitellmModel(model=MODEL, api_key=KEY),
    tools=[
        basic_agent.as_tool(tool_name="basic_agent", tool_description="You are a basic or general agent that can answer questions about you."),
        weather_agent.as_tool(tool_name="weather_agent", tool_description="You are an assistant that can answer questions about the weather in a given city."),
        piaic_agent.as_tool(tool_name="piaic_agent", tool_description="You are a friendly and helpful assistant will answer Penaversity relevant questions.")
    ],
)

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="Welcome to the future! I’m your Agentic World AI Assistant. Ready to explore the possibilities? What can I do for you today?").send()

@cl.on_message
async def main(message: cl.Message):
    # Send a "Thinking..." message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Process the agent's response
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(starting_agent=triage_agent, input=history)
    cl.user_session.set("chat_history", result.to_input_list())

    # Update the "Thinking..." message with the actual response
    msg.content = result.final_output
    await msg.update()