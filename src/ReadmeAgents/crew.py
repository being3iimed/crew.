import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai_tools import GithubSearchTool

# get api key from .env file
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
GITHUB_TOKEN=os.getenv('GITHUB_TOKEN')

# make custom llm
llm= LLM(
    model="llama3-8b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    temperature=0.4
)

""" githubtool = GithubSearchTool(
    github_repo='https://github.com/being3iimed/ICP-Iterative-Closest-Point-Algorithm',
    gh_token=GITHUB_TOKEN,
    content_types=['code', 'repo'], # Options: code, repo, pr, issue
    config=dict(
      llm=dict(
          provider="groq",  # or google, openai, anthropic, llama2, ...
          config=dict(
              model="llama3-8b-8192",
              base_url="https://api.groq.com/openai/v1",
              api_key="your_groq_api_key",  # Ensure this is set
              temperature=0.4
          )
      ),
      embedder=dict(
              provider="huggingface", # or google, openai, anthropic, llama2.. 
              config=dict(
              model="izhx/udever-bloom-1b1", 
              ),
          ),  
    )
) """

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

  @agent
  def Retriever(self) -> Agent:
    return Agent(
      config=self.agents_config['Retriever'],
      verbose=True,
      llm=llm
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
  def Refiner(self) -> Agent:
    return Agent(
      config=self.agents_config['Refiner'],
      verbose=True,
      llm=llm
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
      # memory_config={
      #     "provider": "mem0",
      #     "config": {"user_id": "Mark"},
      # },
)