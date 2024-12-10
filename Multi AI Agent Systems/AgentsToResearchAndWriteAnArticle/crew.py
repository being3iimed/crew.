from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
)

@CrewBase
class bloggerCrew():
  """blogger crew"""

  @agent
  def Planner(self) -> Agent:
    return Agent(
      config=self.agents_config['Planner'],
      verbose=True,
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
      verbose=True
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
      verbose=True
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
      verbose=2
    )