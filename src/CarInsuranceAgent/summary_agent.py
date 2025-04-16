import os
from crewai import LLM, Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys
API_KEY = os.getenv('API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')

llm = LLM(
        model=LLM_MODEL,
        base_url="https://api.groq.com/openai/v1/",
        api_key=API_KEY,
        temperature=0.4
    )
# Define the Summary Assistant Agent
summary_agent = Agent(
    role="Summary Assistant",
    goal="Summarize the car details, estimated value, and insurance suggestion in a friendly message.",
    backstory=(
        "You're the final step in the pipeline — you turn the structured output from the previous tasks "
        "into a brief valuation report or summary. Be conversational and clear, like a helpful app, using "
        "Markdown formatting (headings, bullet points, etc.) to present the information."
    ),
    llm=llm,
    verbose=True
)

# Define the task for the Summary Assistant
summary_task = Task(
    description=(
        "Take the structured results from previous agents — which include car details, estimated car value, "
        "and an insurance suggestion — and write a clear, concise, and friendly summary. "
        "Format the response in Markdown with appropriate headings and bullet points."
    ),
    expected_output=(
        "A short, friendly Markdown report including:\n"
        "- A heading with the car's make/model\n"
        "- Bullet points for key features or condition notes\n"
        "- An estimated value line\n"
        "- A section with the recommended insurance suggestion\n"
        "- A positive tone, like it's coming from a smart helpful assistant."
    ),
    agent=summary_agent,
    llm=llm
)
crew = Crew(
    agents=[summary_agent],
    tasks=[summary_agent],
    process=Process.sequential,
    verbose=True
)

crew.kickoff()