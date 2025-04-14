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
class InsuranceInfoResponderCrew():

    # Paths to YAML configuration files
    agents_config = 'agents/InsuranceInfoResponder_agent.yaml'
    tasks_config = 'tasks/insurance_info_response_task.yaml'

    # Make custom LLM
    llm = LLM(
        model=LLM_MODEL,
        base_url="https://ai.google.dev/gemini-api/",
        api_key=GEMINI_API_KEY,
        temperature=0.4
    )

    @agent
    def InsuranceInfoResponder(self) -> Agent:
        return Agent(
            config=self.agents_config['InsuranceInfoResponder'],
            verbose=True,
            llm=self.llm
        )
    
    @task
    def insurance_info_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['insurance_info_response_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
      agents=[
        self.InsuranceInfoResponder()
      ],
      tasks=[
        self.insurance_info_response_task()
      ],
      process=Process.sequential,
      verbose=True,
    )