import os
import logging
from groq import Groq

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# Get API key
api_key = "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"

if not api_key:
    logging.error("GROQ_API_KEY environment variable not set.")
    raise EnvironmentError("GROQ_API_KEY environment variable not set.")

# Initialize Groq client
logging.info("Initializing Groq client.")
client = Groq(api_key=api_key)

def extract_information_with_llm(text: str) -> str:
    """
    Uses LLM to extract structured KYC information from raw OCR text.
    """
    logging.info("Preparing prompt for Groq LLM.")
    prompt = f"""
    Extract the following fields from the OCR text provided:
    - PAN Number
    - GST Number
    - Registration Date

    Return the result in JSON format.

    OCR Text:
    {text}
    """

    logging.info("Sending prompt to Groq LLM.")
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=512
        )
        response = completion.choices[0].message.content
        logging.info("Received response from Groq LLM.")
        return response
    except Exception as e:
        logging.error(f"Error occurred during LLM extraction: {e}")
        raise
