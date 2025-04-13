import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai_tools import GeminiQueryTool
from mem0 import MemoryClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from .env file

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

LLM_MODEL = os.getenv('LLM_MODEL')


# Task for car value estimator
@CrewBase
class CarInsuranceCrew:
  """Car Value Estimation & Insurance Query Crew"""

  # Make custom LLM
  llm = LLM(
      model=LLM_MODEL,
      base_url="https://api.groq.com/openai/v1",
      api_key=GEMINI_API_KEY,
      temperature=0.4
  )

  @agent
  def CarValueEstimator(self) -> Agent:
    return Agent(
      config=self.agents_config['CarValueEstimator'],
      verbose=True,
      tools=[GeminiQueryTool(api_key=GEMINI_API_KEY)],
      llm=self.llm
    )
  
  @task
  def car_value_estimation_task(self) -> Task:
    return Task(
      config=self.tasks_config['car_value_estimation_task']
    )
  
  @agent
  def InsuranceInfoResponder(self) -> Agent:
    return Agent(
      config=self.agents_config['InsuranceInfoResponder'],
      verbose=True,
      tools=[GeminiQueryTool(api_key=GEMINI_API_KEY)],
      llm=self.llm
    )
  
  @task
  def insurance_info_response_task(self) -> Task:
    return Task(
      config=self.tasks_config['insurance_info_response_task']
    )
