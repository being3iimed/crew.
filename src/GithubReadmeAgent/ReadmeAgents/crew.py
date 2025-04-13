import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai_tools import GithubSearchTool
from mem0 import MemoryClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get api key from .env file
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
GITHUB_TOKEN=os.getenv('GITHUB_TOKEN')
MEM0_API_KEY=os.getenv('MEM0_API_KEY')
LLM_MODEL=os.getenv('LLM_MODEL')
github_r=os.getenv('github_r')


# mem0: intialize client
client = MemoryClient(api_key=MEM0_API_KEY)

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
            "content": "Hi! I need help creating a README.md file for my project."
        },
        {
            "role": "assistant",
            "content": "Sure! I'd be happy to help. Could you tell me a bit about your preferences for the markdown document?"
        },
        {
            "role": "user",
            "content": "Use appropriate Markdown headers, and ensure that a Sources section is included at the end, with references."
        },
        {
            "role": "assistant",
            "content": "Of course! To structure your document effectively, here are some suggestions:\n\n1. Use Markdown headers (`#`, `##`, `###`, etc.) to organize content clearly.\n2. Include a **Sources** section at the end, with references listed properly, including author names, titles, and links.\n3. Format the document to be readable and visually appealing.\n\nIf you'd like, I can draft a template for you. Let me know the key points you'd like included!"
        },
        {
            "role": "user",
            "content": "Format the executive report into a beautiful markdown document without '```'.\nFollow these guidelines:\n1. Use proper markdown headers (#, ##, ###).\n2. Include emojis like this 🤖, 🖧 .\n3. Format key findings and insights as bullet points.\n4. Add proper spacing and section breaks.\n5. Make recommendations stand out using blockquotes.\n6. Ensure the date is properly formatted.\n7. Add a table of contents at the beginning.\n8. Use horizontal rules (---) to separate major sections."
        },
        {
            "role": "assistant",
            "content": "Understood! I can help format into a well-structured and visually appealing markdown document."
        }
]

# Storing the conversation
store_user_preferences("Mark", messages)

# Retrieve memory
query = "How to create and format Markdown document?"
client.search(query, user_id='Mark')

githubtool = GithubSearchTool(
    github_repo=github_r,
    gh_token=GITHUB_TOKEN,
    content_types=['code', 'repo'], 
    config=dict(
        llm=dict(
            provider="groq", 
            config=dict(
                model=LLM_MODEL,
                base_url="https://api.groq.com/openai/v1",
                api_key=GROQ_API_KEY,
                temperature=0.4,
            )
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="izhx/udever-bloom-1b1",
            ),
        ),
    )
)

@before_kickoff
def before_kickoff_function(self, inputs):
  print(f"Before kickoff function with inputs: {inputs}")
  return inputs
@after_kickoff
def after_kickoff_function(self, result):
  print(f"After kickoff function with result: {result}")
  return result # You can return the result or modify it as needed

@CrewBase
class ReadmeCrew():
  """README.md crew"""

  # make custom llm
  llm= LLM(
      model=LLM_MODEL,
      base_url="https://api.groq.com/openai/v1",
      api_key=GROQ_API_KEY,
      temperature=0.4
  )
    
  
  @agent
  def Retriever(self) -> Agent:
    return Agent(
      config=self.agents_config['Retriever'],
      verbose=True,
      tools=[githubtool],
      llm=self.llm
    )
  @task
  def retriever_task(self) -> Task:
    return Task(
      config=self.tasks_config['retriever_task']
    )
  
  @agent
  def Planner(self) -> Agent:
    return Agent(
      config=self.agents_config['Planner'],
      verbose=True,
      llm=self.llm
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
      llm=self.llm
    )
  @task
  def writer_task(self) -> Task:
    return Task(
      config=self.tasks_config['writer_task']
    )
  @agent
  def Refiner(self) -> Agent:
    return Agent(
      config=self.agents_config['Refiner'],
      verbose=True,
      llm=self.llm
    )
  @task
  def refiner_task(self) -> Task:
    return Task(
      config=self.tasks_config['refiner_task']
    )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=[
        self.Retriever(),
        self.Planner(),
        self.Writer(),
        self.Refiner()
      ],
      tasks=[
        self.retriever_task(),
        self.planner_task(),
        self.writer_task(),
        self.refiner_task()
      ],
      verbose=True,
      process=Process.sequential,
      memory=True,
      memory_config={
            "provider": "mem0",
           "config": {"user_id": "Mark"},
        },
)