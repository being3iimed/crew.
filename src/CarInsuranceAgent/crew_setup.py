import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai_tools import GeminiQueryTool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')

@CrewBase
class CarInsuranceCrew:
    """Car Value Estimation & Insurance Query Crew"""

    # Paths to YAML configuration files
    agents_config = 'agents/agents.yaml'
    tasks_config = 'agents/tasks.yaml'

    # Make custom LLM
    llm = LLM(
        model=LLM_MODEL,
        base_url="https://generativelanguage.googleapis.com",
        api_key=GEMINI_API_KEY,
        temperature=0.4
    )

    @before_kickoff
    def prepare_inputs(self, inputs):
        # Add any necessary preprocessing of inputs
        if 'car_details' in inputs:
            inputs['car_details'] = inputs['car_details'].strip()
        if 'insurance_question' in inputs:
            inputs['insurance_question'] = inputs['insurance_question'].strip()
        return inputs

    @after_kickoff
    def process_output(self, output):
        # Add any necessary postprocessing of outputs
        if hasattr(output, 'raw'):
            output.raw = f"Processed by CarInsuranceCrew: {output.raw}"
        return output

    @agent
    def CarValueEstimator(self) -> Agent:
        return Agent(
            config=self.agents_config['CarValueEstimator'],
            verbose=True,
            tools=[GeminiQueryTool(api_key=GEMINI_API_KEY)],
            llm=self.llm
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
    def car_value_estimation_task(self) -> Task:
        return Task(
            config=self.tasks_config['car_value_estimation_task'],
            agent=self.CarValueEstimator()
        )
    
    @task
    def insurance_info_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['insurance_info_response_task'],
            agent=self.InsuranceInfoResponder()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

# Create crew instances
value_agent = CarInsuranceCrew().car_value_estimation_task()
info_agent = CarInsuranceCrew().insurance_info_response_task()
