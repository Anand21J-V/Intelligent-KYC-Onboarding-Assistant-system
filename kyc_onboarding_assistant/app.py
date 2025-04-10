import streamlit as st
import json
import logging
import os
from ocr_utils import extract_text_from_image
from groq_utils import extract_information_with_llm
from validation_utils import validate_pan, validate_gst, validate_registration_date

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def main():
    st.title("Intelligent KYC/Onboarding Assistant")
    logging.info("App started: Intelligent KYC/Onboarding Assistant")

    uploaded_file = st.file_uploader("Upload Document (PAN/GST/Registration)", type=["jpg", "png", "pdf"])

    if uploaded_file is not None:
        file_path = f"./temp_{uploaded_file.name}"
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            logging.info(f"File uploaded and saved: {file_path}")
        except Exception as e:
            logging.exception("Failed to save uploaded file.")
            st.error("Failed to save uploaded file.")
            return

        # OCR processing
        try:
            extracted_text = extract_text_from_image(file_path)
            logging.info("OCR text extraction successful.")
            st.text_area("Extracted Text", extracted_text, height=300)
        except Exception as e:
            logging.exception("OCR failed.")
            st.error("Text extraction failed.")
            return

        # LLM-based extraction
        try:
            extracted_info = extract_information_with_llm(extracted_text)
            logging.info("LLM information extraction successful.")
            extracted_data = json.loads(extracted_info)
            st.json(extracted_data)
        except Exception as e:
            logging.exception("LLM information extraction failed.")
            st.error("Failed to extract structured info using LLM.")
            return

        # Validation
        try:
            pan_valid = validate_pan(extracted_data.get("PAN Number", ""))
            gst_valid = validate_gst(extracted_data.get("GST Number", ""))
            reg_date_valid = validate_registration_date(extracted_data.get("Registration Date", ""))

            validation_results = {
                "PAN Valid": pan_valid,
                "GST Valid": gst_valid,
                "Registration Date Valid": reg_date_valid
            }

            logging.info(f"Validation results: {validation_results}")
            st.write("Validation Results:")
            st.json(validation_results)
        except Exception as e:
            logging.exception("Validation failed.")
            st.error("Validation process failed.")

        # Optional: cleanup
        try:
            os.remove(file_path)
            logging.info(f"Temporary file deleted: {file_path}")
        except Exception as e:
            logging.warning(f"Failed to delete temporary file: {file_path}")

if __name__ == "__main__":
    main()
