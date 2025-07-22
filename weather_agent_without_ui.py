# Make ui for weather app and get api key 
from agents import Agent, Runner, function_tool
from main import config
import os
from dotenv import load_dotenv
import requests

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

@function_tool
def get_weather(city:str) -> str:          # made a function tool in which we  dynamically get the weather of a city
    """Get the current weather for a specified city."""
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}")
    data = response.json()
    return f'The weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}.'

agent = Agent(
    name = "Weather Agent",    
    instructions = "You are a helpful assistant. Your task is to help the user only by telling the weather.",
    tools = [get_weather]
)

result = Runner.run_sync(
    agent,
    input = "What is the current weather in Islamabad today?",
    run_config = config
)

print(result.final_output)            # only provide the answer, not the full log