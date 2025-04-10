import cv2
import pytesseract
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("ocr_processing.log"),
        logging.StreamHandler()
    ]
)

def preprocess_image(image_path):
    """Preprocess the image for better OCR results."""
    logging.info(f"Preprocessing image: {image_path}")

    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        logging.error(f"Failed to load image: {image_path}")
        raise ValueError(f"Failed to load image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    logging.info("Image converted to grayscale.")
    # Additional preprocessing steps can be logged here
    return gray

def extract_text_from_image(image_path):
    """Extract text from a given image using Tesseract OCR."""
    logging.info(f"Extracting text from image: {image_path}")
    try:
        preprocessed_image = preprocess_image(image_path)
        text = pytesseract.image_to_string(preprocessed_image)
        logging.info("Text extraction completed successfully.")
        return text
    except Exception as e:
        logging.exception("Error occurred during OCR:")
        return ""
