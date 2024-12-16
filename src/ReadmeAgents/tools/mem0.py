import os
from mem0 import MemoryClient

MEM0_API_KEY=os.getenv('MEM0_API_KEY')


# mem0: intialize client
client = MemoryClient(api_key="MEM0_API_KEY")

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
        "content": "Sure! I'd be happy to help. Could you tell me a bit about you preferences for markdown document.",
    },
    {
        "role": "user",
        "content": "use appropriate Markdown headers, and ensure that a Sources section is included at the end, with references.",
    },
    {
    "role": "assistant",
    "content": (
        "Sure! To structure your document effectively, follow these guidelines: "
        "1. **Use Markdown headers** to organize content clearly, such as `# Header 1`, `## Header 2`, and so on.\n"
        "2. **Include a Sources section** at the end, listing all external references with numbered citations like:\n"
        "- [1] Author, *Title*, Year"
        "- [2] Author, *Title*, Year"
    )
},
]

# Storing the conversation
store_user_preferences("Mark", messages)

# Retrieve memory
query = "How to create Markdown document?"
client.search(query, user_id='Mark')
