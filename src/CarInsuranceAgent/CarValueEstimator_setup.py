import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')

@CrewBase
class CarValueEstimatorCrew():

    # Paths to YAML configuration files
    agents_config = 'agents/CarValueEstimator_agent.yaml'
    tasks_config = 'agents/car_value_estimation_task.yaml'

    # Make custom LLM
    llm = LLM(
        model=LLM_MODEL,
        base_url="https://api.groq.com/openai/v1/",
        api_key=GEMINI_API_KEY,
        temperature=0.4
    )

    @agent
    def CarValueEstimator(self) -> Agent:
        return Agent(
            config=self.agents_config['CarValueEstimator'],
            verbose=True,
            llm=self.llm
        )
    
    @task
    def car_value_estimation_task(self) -> Task:
        return Task(
            config=self.tasks_config['car_value_estimation_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
      agents=[
        self.CarValueEstimator()
      ],
      tasks=[
        self.car_value_estimation_task()
      ],
      process=Process.sequential,
      verbose=True,
    )
