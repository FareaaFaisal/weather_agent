# Make ui for currency convertor and get api key 
from agents import Agent, Runner, function_tool
from main import config

@function_tool
def usd_to_pkr():               # made a function tool in which we hardcoded USD to PKR rate
    """Convert USD to PKR."""
    return 'Today 1 USD is approximately 280 PKR.'
agent = Agent(
    name="General Agent",    
    instructions="You are a helpful assistant. Your task is to help the user with their queries.",
    tools=[usd_to_pkr]
)

result = Runner.run_sync(
    agent,
    input="What is the USD to PKR rate today?",
    run_config=config
)

print(result.final_output)            # only provide the answer, not the full log