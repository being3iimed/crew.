import sys
from bloggerCrew import bloggerCrew
from dotenv import load_dotenv

load_dotenv()

def run():
  """
  Run the crew.
  """
  inputs = {
    'topic': 'AI Agents'
  }
  bloggerCrew().crew().kickoff(inputs=inputs)
