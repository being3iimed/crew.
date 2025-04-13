import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def query_gemini(prompt: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text