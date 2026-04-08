from ..helper import *
###from helper import * # only testing
from typing import List
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Define Structured Output ---
class ResearchStep(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., TSLA)")
    reason: str = Field(description="Why this ticker is relevant to the user's query")

class ResearchPlan(BaseModel):
    plan_title: str = Field(description="A brief title for the research strategy")
    steps: List[ResearchStep] = Field(max_items=3, description="A list of 3 tickers to investigate")

config = get_model_config("planner_agent")

custom_model = LiteLlm(
    model=config["model_name"], 
    api_base=config["api_base"],    
    api_key=config["api_key"],
)

# Define the Agent ---
planner_agent = LlmAgent(
    name="Financial_Planner",
    model=custom_model,
    instruction="""
    You are a strategic financial analyst. 
    Analyze the user's request and identify the 3 most relevant tickers to investigate. 
    Your output must follow the research plan structure exactly.
    """,
    output_schema=ResearchPlan,
    output_key="research_plan"
)






