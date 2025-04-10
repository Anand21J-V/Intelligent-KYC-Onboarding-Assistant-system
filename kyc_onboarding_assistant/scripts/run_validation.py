import sys
import json
import logging
import os
from kyc_onboarding_assistant.validation_utils import validate_pan, validate_gst, validate_registration_date

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

# Get paths from CLI args or set default
input_path = sys.argv[1] if len(sys.argv) > 1 else "kyc_onboarding_assistant/output/llm_output.json"
output_path = sys.argv[2] if len(sys.argv) > 2 else "kyc_onboarding_assistant/output/validation_output.json"

logging.info(f"Reading input data from: {input_path}")

# Check if file exists and is not empty
if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
    logging.error("Input file is missing or empty.")
    sys.exit(1)

try:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    logging.error(f"Failed to parse JSON: {e}")
    sys.exit(1)

logging.info("Validating PAN, GST, and Registration Date...")
result = {
    "PAN Valid": validate_pan(data.get("PAN Number", "")),
    "GST Valid": validate_gst(data.get("GST Number", "")),
    "Registration Date Valid": validate_registration_date(data.get("Registration Date", ""))
}

logging.info(f"Writing validation results to: {output_path}")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

logging.info("Validation stage completed successfully.")
