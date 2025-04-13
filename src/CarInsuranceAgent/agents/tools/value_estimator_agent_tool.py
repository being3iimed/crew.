from services.gemini_client import query_gemini

def estimate_car_value(car_details: str) -> str:
    prompt = f"""Estimate the value of the following car based on typical market trends and car conditions.
    
    Car Details: {car_details}

    Give a concise estimate with reasoning.
    """
    return query_gemini(prompt)