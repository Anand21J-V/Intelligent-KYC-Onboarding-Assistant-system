import pytesseract
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_image(image_file):
    try:
        logger.info("Opening image for OCR.")
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        logger.info("OCR extraction completed.")
        return text
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return ""
