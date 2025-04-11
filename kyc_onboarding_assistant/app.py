import streamlit as st
from ocr_utils import extract_text_from_image
from groq_utils import extract_fields_with_groq_llm
from validation_utils import match_data
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="🧠 Intelligent KYC Assistant")
st.title("📄 Intelligent KYC/Onboarding Assistant")

st.markdown("Upload your **KYC documents** and fill the form to verify the information automatically.")

uploaded_file = st.file_uploader("Upload PAN/GST/Company Reg Document", type=["jpg", "jpeg", "png", "pdf"])

with st.form("kyc_form"):
    pan_input = st.text_input("PAN Number")
    gst_input = st.text_input("GST Number")
    company_name_input = st.text_input("Company Name")
    submitted = st.form_submit_button("Verify Document")

if uploaded_file and submitted:
    logger.info("Form submitted. Processing document...")
    
    st.info("🔍 Extracting text from image...")
    ocr_text = extract_text_from_image(uploaded_file)

    st.success("✅ OCR extraction done.")
    st.text_area("OCR Result", ocr_text, height=200)

    st.info("🤖 Extracting info with LLM (GROQ)...")
    llm_response = extract_fields_with_groq_llm(ocr_text)

    try:
        extracted_json = json.loads(llm_response)
        logger.info("Parsed LLM output successfully.")
        st.success("✅ LLM extraction successful")
        st.json(extracted_json)

        user_data = {
            "PAN Number": pan_input,
            "GST Number": gst_input,
            "Company Name": company_name_input
        }

        mismatches = match_data(extracted_json, user_data)

        if mismatches:
            st.warning("⚠️ Mismatches/Issues found:")
            for issue in mismatches:
                st.write(f"- {issue}")
        else:
            st.success("🎉 All document fields match the user input!")

    except Exception as e:
        logger.error(f"Failed to parse LLM response: {e}")
        st.error("❌ Failed to parse LLM output. Raw response below:")
        st.text(llm_response)
