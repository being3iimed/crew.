from crewai_tools import tool
import base64
import requests

@tool("Car Image Analysis Tool")
def car_image_analysis_tool(image_base64: str) -> str:
    """Takes a base64-encoded car image and returns the car's make, model, year, and visible condition."""
    # Replace this with your actual endpoint
    url = "https://your-image-analysis-api.com/analyze"
    try:
        response = requests.post(url, json={"image": image_base64})
        response.raise_for_status()
        result = response.json()
        return result.get("summary", "No summary returned from analysis.")
    except Exception as e:
        return f"Failed to analyze image: {str(e)}"
