import sys
import json
import logging
from kyc_onboarding_assistant.groq_utils import extract_information_with_llm

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# Handle arguments with defaults
input_path = sys.argv[1] if len(sys.argv) > 1 else "kyc_onboarding_assistant/output/ocr_output.txt"
output_path = sys.argv[2] if len(sys.argv) > 2 else "kyc_onboarding_assistant/output/llm_output.json"

logging.info(f"Reading OCR output from: {input_path}")
with open(input_path, "r", encoding="utf-8") as f:
    doc_text = f.read()

logging.info("Extracting information using LLM...")
info_json = extract_information_with_llm(doc_text)

logging.info(f"Writing extracted info to: {output_path}")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(info_json)

logging.info("LLM processing completed successfully.")
