import re
from fuzzywuzzy import fuzz
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_pan(pan):
    valid = bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan))
    logger.info(f"PAN validation: {pan} -> {valid}")
    return valid

def validate_gst(gst):
    valid = bool(re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$', gst))
    logger.info(f"GST validation: {gst} -> {valid}")
    return valid

def match_data(extracted, user_input):
    mismatches = []

    logger.info("Starting field validation and matching.")

    if 'PAN Number' in extracted and not validate_pan(extracted['PAN Number']):
        mismatches.append("Invalid PAN format")

    if 'GST Number' in extracted and not validate_gst(extracted['GST Number']):
        mismatches.append("Invalid GST format")

    for key in ['Company Name', 'PAN Number', 'GST Number']:
        if key in user_input and key in extracted:
            similarity = fuzz.ratio(user_input[key], extracted[key])
            logger.info(f"Matching {key}: User='{user_input[key]}' vs Extracted='{extracted[key]}' -> Similarity={similarity}")
            if similarity < 85:
                mismatches.append(f"{key} mismatch (similarity: {similarity}%)")

    if mismatches:
        logger.warning(f"Mismatches found: {mismatches}")
    else:
        logger.info("All fields matched successfully.")

    return mismatches
