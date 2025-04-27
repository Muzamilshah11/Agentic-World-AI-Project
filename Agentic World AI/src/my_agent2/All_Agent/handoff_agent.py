import asyncio, os
from dotenv import load_dotenv
from agents import Agent , Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from my_agent2.All_Agent.tool_agent import weather_agent

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
    instructions= "You will chat with user for genral questions and handoff to Specialized Agent for Penaversity and Weather Quries and greet user.",
    model=LitellmModel(model=MODEL, api_key=KEY),
    handoffs= [weather_agent, piaic_agent]
    # tools= [weather_agent.as_tool(tool_name="weather_agent", 
    #         tool_description="You are assistant that can answer questions about the weather in a given city."), 
    #         piaic_agent.as_tool(tool_name="piaic_agent", 
    #         tool_description="You are a frindly and helpful assistant will answer Penaversity relevant questions.")
    #         ],
)

async def handoff_main():
    query = input("Enter your query: ")
    result = await Runner.run(triage_agent, query)
    print(result.last_agent.name)
    print(result.final_output)
   



if __name__ == "__main__":
    asyncio.run(handoff_main())