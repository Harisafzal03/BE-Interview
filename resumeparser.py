import requests
import json

def ats_extractor(resume_data):
    # Gemini API endpoint and API key
    GEMINI_API_KEY = "AIzaSyChInQB6FswlCsrMsUr_kz6ZfJoMpODasQ"
    GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    # Define the prompt
    prompt = f"""
    For the given resume, extract the following information:
    1. Full name
    2. Email ID
    3. GitHub portfolio
    4. LinkedIn ID
    5. Employment details
    6. Technical skills
    7. Soft skills
    Provide the output in JSON format only.

    Resume Data: {resume_data}
    """

    # Define the request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Define headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request to the Gemini API
    response = requests.post(GEMINI_URL, headers=headers, json=payload)

    # Handle the response
    if response.status_code == 200:
        try:
            response_data = response.json()
            # Extract the generated text
            generated_content = response_data["candidates"][0]["content"]["parts"][0]["text"]
            
         
            
            print("generatedcontent",generated_content)
            # Parse the cleaned content as JSON
            return generated_content
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse the response as JSON: {generated_content}")
    else:
        raise RuntimeError(f"Gemini API Error: {response.status_code}, {response.text}")