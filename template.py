import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "src/__init__.py",
    "kyc_onboarding_assistant/app.py",
    "kyc_onboarding_assistant/ocr_utils.py",
    "kyc_onboarding_assistant/groq_utils.py",
    "kyc_onboarding_assistant/validation_utils.py",
    "kyc_onboarding_assistant/data/input.jpg",  
    "kyc_onboarding_assistant/output/.gitkeep",  
    "requirements.txt",
    "project-structure.txt"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
