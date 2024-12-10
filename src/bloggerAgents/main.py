import sys
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crew import bloggerCrew
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