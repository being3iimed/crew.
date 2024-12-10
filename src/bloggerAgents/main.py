import sys
import os
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crew import bloggerCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI Agents'
    }
    print("Initializing the crew...")
    crew = bloggerCrew().crew()  # Ensure bloggerCrew().crew() works as expected
    print("Crew initialized. Starting kickoff...")
    result = crew.kickoff(inputs=inputs)
    print("Kickoff complete. Writing result to file...")

    # Ensure the output directory exists
    os.makedirs("output", exist_ok=True)

    # Write the result to the file
    with open("output/blog.md", "w") as f:
        f.write(str(result))

    print("Result saved to output/blog.md")
# Ensure this script runs properly when executed
if __name__ == "__main__":
    run()
