
import os
from google.genai import types
from dotenv import load_dotenv

def get_model_config(agent = "root_agent"):
    """
    Retrieves model configuration from environment variables.    
    """
    load_dotenv()
    config = {}
    match agent:
        case "root_agent":
            config["model_name"] = os.getenv("ROOT_MODEL_NAME", "gemini-2.5-flash")
            config["model_provider"] = os.getenv("ROOT_MODEL_PROVIDER", "GOOGLE")                           
        case "planner_agent":
            config["model_name"] = os.getenv("PLANNER_MODEL_NAME", "arcee-ai/trinity-large-preview:free")
            config["model_provider"] = os.getenv("PLANNER_MODEL_PROVIDER", "OPENROUTER")       
        case "writer_agent":                 
            config["model_name"] = os.getenv("WRITER_MODEL_NAME", "gemini-2.5-flash")
            config["model_provider"] = os.getenv("WRITER_MODEL_PROVIDER", "GOOGLE")
        case "verifier_agent":
            config["model_name"] = os.getenv("VERIFIER_MODEL_NAME", "stepfun/step-3.5-flash:free")
            config["model_provider"] = os.getenv("VERIFIER_MODEL_PROVIDER", "OPENROUTER")            
        case _:
            raise ValueError(f"Unknown agent type: {agent}")    
        
    config["api_key"], config["api_base"] =  get_api_config(config["model_provider"])  
    return config

def get_api_config(model_provider):
    """
    Retrieves API key and base URL based on the model provider from environment variables.
    """
    match model_provider:
        case "OPENROUTER":
            return os.getenv("OPENROUTER_API_KEY", "sk-no-key-required"), os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"), 
        case "GOOGLE":  # Default to GOOGLE            
            os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "sk-no-key-required")
            return None, None        
        case "LOCAL":
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "sk-no-key-required") # Set OpenAI key for local models that require it, even if it's a dummy value
            return None, os.getenv("LOCAL_MODEL_API_BASE", "http://localhost:11434/v1")

# Configure retry options for LLM calls to handle transient errors and rate limits.
# Automatic retry mechanism with exponential backoff to resubmit failed requests.
def get_retry_config():
    retry_config=types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
    )
    return retry_config
