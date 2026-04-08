from ..helper import *
###from helper import * # only testing
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

config = get_model_config("verifier_agent")

custom_model = LiteLlm(
    model=config["model_name"], 
    api_base=config["api_base"],    
    api_key=config["api_key"],
)

# Define the Agent ---
verifier_agent = LlmAgent(
    name="Financial_Verifier",
    model=custom_model,
    instruction="""
    You are a Financial Auditor. Your only job is to ensure the Writer has not hallucinated numbers.
    
    INPUTS:
    1. The Draft Report: {{draft_report}}
    2. The Raw Data Context: (This is automatically available in the session history)
    
    YOUR TASK:
    - Compare every number in the draft (Prices, P/E ratios, % changes) against the raw data.
    - If any number is incorrect, start your response with 'CRITICAL ERROR: DATA MISMATCH'.
    - If the report is accurate, output 'VERIFIED: ACCURATE'.
    - Provide a short summary of your verification check.
    """,
    output_key="final_verification"
)       

