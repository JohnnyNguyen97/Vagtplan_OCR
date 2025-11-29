from PIL import Image
import pytesseract

def extract_text(image_path, tesseract_path=None):
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang="dan+eng")
