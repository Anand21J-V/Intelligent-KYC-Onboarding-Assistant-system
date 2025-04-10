from kyc_onboarding_assistant.ocr_utils import extract_text_from_image
import os

# Define input and output path
input_path = "kyc_onboarding_assistant/input/input.jpg"  
output_path = "kyc_onboarding_assistant/output/ocr_output.txt"

# Run OCR
extracted_text = extract_text_from_image(input_path)

# Save output
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(extracted_text)
