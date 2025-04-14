from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import google.generativeai as genai
from PIL import Image
import io
import os

class CarDetails(BaseModel):
    make: str = Field(..., description="The manufacturer of the vehicle")
    model: str = Field(..., description="The specific model of the vehicle")
    year: int = Field(..., description="The manufacturing year of the vehicle", ge=1900, le=2024)
    mileage: int = Field(..., description="The current mileage of the vehicle", ge=0)
    condition: str = Field(..., description="The overall condition of the vehicle (Excellent/Good/Fair/Poor)")
    special_features: Optional[list[str]] = Field(default=[], description="Any special features or modifications")
    service_history: Optional[str] = Field(default=None, description="Details about the vehicle's service history")

class CarDetailsExtractor(BaseTool):
    name: str = "Car Details Extractor"
    description: str = """
    A tool that extracts structured car details from user queries, whether they are text descriptions or images.
    It can process:
    - Text descriptions of cars
    - Images of cars
    - Mixed text and image inputs
    
    The tool will return a structured CarDetails object with all available information.
    """

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def _process_text(self, text: str) -> CarDetails:
        prompt = f"""
        Extract car details from the following description and return them in a structured format.
        If any information is missing, make reasonable assumptions or mark as unknown.
        
        Description: {text}
        
        Required fields:
        - make (manufacturer)
        - model
        - year (between 1900 and 2024)
        - mileage (non-negative number)
        - condition (Excellent/Good/Fair/Poor)
        - special_features (list of features/modifications)
        - service_history (if mentioned)
        
        Return the information in JSON format.
        """
        
        response = self.model.generate_content(prompt)
        return CarDetails.parse_raw(response.text)

    def _process_image(self, image: Image.Image) -> CarDetails:
        prompt = """
        Analyze this car image and extract as much information as possible about the vehicle.
        Include:
        - make (manufacturer)
        - model
        - approximate year
        - visible condition
        - any special features visible
        - any modifications visible
        
        Return the information in JSON format.
        """
        
        response = self.model.generate_content([prompt, image])
        return CarDetails.parse_raw(response.text)

    def _run(self, query: str | bytes | Image.Image) -> CarDetails:
        """
        Process the query and extract car details.
        
        Args:
            query: Can be:
                - Text description of the car
                - Image bytes or PIL Image of the car
                - Path to an image file
        
        Returns:
            CarDetails object with extracted information
        """
        try:
            # Handle text input
            if isinstance(query, str):
                return self._process_text(query)
            
            # Handle image input
            if isinstance(query, bytes):
                image = Image.open(io.BytesIO(query))
            elif isinstance(query, Image.Image):
                image = query
            else:
                raise ValueError("Unsupported input type")
                
            return self._process_image(image)
            
        except Exception as e:
            raise Exception(f"Error processing car details: {str(e)}")

    async def _arun(self, query: str | bytes | Image.Image) -> CarDetails:
        """Async version of _run"""
        return self._run(query) 