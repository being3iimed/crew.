import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import VisionTool
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('V_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL_VISION')


@CrewBase
class ImageCarAnalysisCrew:

    def vision_tool(self):
        return VisionTool()

    agents_config = 'agents/image_car_analysis_agents.yaml'
    tasks_config = 'tasks/image_car_analysis_tasks.yaml'

    llm = LLM(
        model=LLM_MODEL,
        base_url="https://api.groq.com/openai/v1/",
        api_key=API_KEY,
        temperature=0.3
    )
    

    @agent
    def image_interpreter(self) -> Agent:
        return Agent(
            config=self.agents_config['image_interpreter'], 
            llm=self.llm, 
            multimodal=True, 
            allow_delegation=False,
            tools=[self.vision_tool()],
            verbose=True
            )

    @agent
    def visual_valuator(self) -> Agent:
        return Agent(config=self.agents_config['visual_valuator'], llm=self.llm, multimodal=True, verbose=True)

    @agent
    def coverage_recommender(self) -> Agent:
        return Agent(config=self.agents_config['coverage_recommender'], llm=self.llm, verbose=True)

    @agent
    def response_summarizer(self) -> Agent:
        return Agent(config=self.agents_config['response_summarizer'], llm=self.llm, verbose=True)

    
    @task
    def interpret_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['interpret_image_task'],
            tools=[self.vision_tool()],
            )

    @task
    def estimate_value_task(self) -> Task:
        return Task(config=self.tasks_config['estimate_value_task'])

    @task
    def recommend_coverage_task(self) -> Task:
        return Task(config=self.tasks_config['recommend_coverage_task'])

    @task
    def summarize_results_task(self) -> Task:
        return Task(config=self.tasks_config['summarize_results_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.image_interpreter(),
                self.visual_valuator(),
                self.coverage_recommender(),
                self.response_summarizer()
            ],
            tasks=[
                self.interpret_image_task(),
                self.estimate_value_task(),
                self.recommend_coverage_task(),
                self.summarize_results_task()
            ],
            process=Process.sequential,
            verbose=True
        )
