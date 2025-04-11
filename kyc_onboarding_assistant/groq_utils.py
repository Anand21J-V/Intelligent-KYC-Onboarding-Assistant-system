import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = "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"  # Replace with your actual key
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def extract_fields_with_groq_llm(text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an intelligent assistant. Extract KYC fields from the following OCR text:

{text}

Return the output in pure JSON like this:
{{
  "Document Type": "",
  "PAN Number": "",
  "GST Number": "",
  "Company Name": "",
  "Date of Incorporation": ""
}}
"""

    payload = {
        "model": "mixtral-8x7b-32768",  # or llama3-8b-8192
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    try:
        logger.info("Sending request to GROQ LLM API.")
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        logger.info("LLM response received successfully.")
        return result['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"GROQ API error: {e}")
        return "{}"
