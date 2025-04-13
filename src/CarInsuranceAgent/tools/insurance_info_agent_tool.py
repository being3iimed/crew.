from services.gemini_client import query_gemini

def answer_insurance_query(user_question: str) -> str:
    prompt = f"""You are a helpful assistant specialized in car insurance.
    
    User question: {user_question}

    Provide a clear and friendly response.
    """
    return query_gemini(prompt)