from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
import os

# get api key from .env file
GROQ_API_KEY=os.getenv('GROQ_API_KEY')

# make custom llm
llm= LLM(
    model="llama3-8b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

@before_kickoff
def before_kickoff_function(self, inputs):
  print(f"Before kickoff function with inputs: {inputs}")
  return inputs # You can return the inputs or modify them as needed

@after_kickoff
def after_kickoff_function(self, result):
  print(f"After kickoff function with result: {result}")
  return result # You can return the result or modify it as needed

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
      verbose=True
    )