import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from mem0 import MemoryClient
from crewai_tools import SerperDevTool

# get api key from .env file
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
mem0_API_KEY=os.getenv('mem0_API_KEY')
SERPER_API_KEY=os.getenv('SERPER_API_KEY')


# mem0: intialize client
client = MemoryClient(api_key="mem0_API_KEY")

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

# Add memory
messages = [
    {"role": "user", "content": "Hi, I'm Bran. I'm a blog writer focus on tech trends."},
    {"role": "assistant", "content": "Hello Bran! I've noted that you're a blog writer who focuses on tech trends. I'll keep this in mind for any food-related recommendations or discussions."}
]
client.add(messages, user_id="alex")

# Retrieve memory
query = "what can I cook for dinner tonight?"
client.search(query, user_id='alex')


# make custom llm
llm= LLM(
    model="llama3-8b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

""" @before_kickoff
def before_kickoff_function(self, inputs):
  print(f"Before kickoff function with inputs: {inputs}")
  return inputs 
@after_kickoff
def after_kickoff_function(self, result):
  print(f"After kickoff function with result: {result}")
  return result # You can return the result or modify it as needed
 """
@CrewBase
class bloggerCrew():
  """blogger crew"""

  @agent
  def Planner(self) -> Agent:
    return Agent(
      config=self.agents_config['Planner'],
      verbose=True,
      llm=llm
    )
  @task
  def planner_task(self) -> Task:
    return Task(
      config=self.tasks_config['planner_task']
    )

  @agent
  def Writer(self) -> Agent:
    return Agent(
      config=self.agents_config['Writer'],
      verbose=True,
      llm=llm
    )
  @task
  def writer_task(self) -> Task:
    return Task(
      config=self.tasks_config['writer_task']
    )
  @agent
  def Editor(self) -> Agent:
    return Agent(
      config=self.agents_config['Editor'],
      verbose=True,
      llm=llm
    )
  @task
  def editor_task(self) -> Task:
    return Task(
      config=self.tasks_config['editor_task']
    )
  
  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=[
        self.Planner(),
        self.Writer(),
        self.Editor()
      ],
      tasks=[
        self.planner_task(),
        self.writer_task(),
        self.editor_task()
      ],
      process=Process.sequential,
      memory=True,
      verbose=True,
  )