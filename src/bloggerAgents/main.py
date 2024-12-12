import sys
import os
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from bloggerAgents.crew import bloggerCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Agentic Automation'
    }
    print("Initializing the crew...")
    crew = bloggerCrew().crew()  
    print("Crew initialized. Starting kickoff...")
    result = crew.kickoff(inputs=inputs)
    print("Kickoff complete. Writing result to file...")

    # Ensure the output directory exists
    os.makedirs("output", exist_ok=True)

    # Write the result to the file
    with open("output/blog.md", "w") as f:
        f.write(str(result))

    print("Result saved to output/blog.md")

if __name__ == "__main__":
    run()
