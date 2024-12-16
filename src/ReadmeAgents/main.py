import sys
import os
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from ReadmeAgents.crew import ReadmeCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
github_r=os.getenv('github_r')

def run():
    """
    Run the crew.
    """
    inputs = {
        'url': github_r
    }
    print("Initializing the crew...")
    crew = ReadmeCrew().crew()  
    print("Crew initialized. Starting kickoff...")
    result = crew.kickoff(inputs=inputs)
    print("Kickoff complete. Writing result to file...")

    # Ensure the output directory exists
    os.makedirs("output", exist_ok=True)

    # Write the result to the file
    with open("output/README.md", "w") as f:
        f.write(str(result))

    print("Result saved to output/README.md")

if __name__ == "__main__":
    run()
