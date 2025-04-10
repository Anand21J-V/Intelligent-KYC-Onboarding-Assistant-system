import re
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("validation.log"),
        logging.StreamHandler()
    ]
)

def validate_pan(pan):
    """Validate PAN number format."""
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    is_valid = re.match(pattern, pan) is not None
    logging.info(f"Validating PAN: {pan} -> {'Valid' if is_valid else 'Invalid'}")
    return is_valid

def validate_gst(gst):
    """Validate GST number format."""
    pattern = r'^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'
    is_valid = re.match(pattern, gst) is not None
    logging.info(f"Validating GST: {gst} -> {'Valid' if is_valid else 'Invalid'}")
    return is_valid

def validate_registration_date(date):
    """Validate registration date format (DD-MM-YYYY)."""
    pattern = r'^\d{2}-\d{2}-\d{4}$'
    is_valid = re.match(pattern, date) is not None
    logging.info(f"Validating Registration Date: {date} -> {'Valid' if is_valid else 'Invalid'}")
    return is_valid
