import os
from mem0 import MemoryClient
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Configuration
os.environ["MEM0_API_KEY"] = "your-mem0-api-key"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["SERPER_API_KEY"] = "your-serper-api-key"

# Initialize Mem0 client
client = MemoryClient()
def store_user_preferences(user_id: str, conversation: list):
    """
    Store user preferences from conversation history.
    
    Args:
        user_id (str): Unique identifier for the user.
        conversation (list): A list of messages exchanged between the user and the assistant.
    """
    client.add(conversation, user_id=user_id)

# Example conversation for a README.md creation process
messages = [
    {
        "role": "user",
        "content": "Hi! I need help creating a README.md file for my project.",
    },
    {
        "role": "assistant",
        "content": "Sure! I'd be happy to help. Could you tell me a bit about your project? What's its purpose?",
    },
    {
        "role": "user",
        "content": "It's a web scraper that extracts data from e-commerce websites.",
    },
    {
        "role": "assistant",
        "content": (
            "Great! To create a detailed README.md, could you provide more details? "
            "For example, the installation process, usage instructions, and features of the scraper?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Sure! Users can install it via `pip install ecom-scraper`. "
            "It supports multiple e-commerce sites and has customizable scraping rules. "
            "I'll provide more details about the features."
        ),
    },
]

# Storing the conversation
store_user_preferences("crew_user_1", messages)

