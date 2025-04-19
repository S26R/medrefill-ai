import pytesseract
<<<<<<< Updated upstream

# Specify the Tesseract executable path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if Tesseract is installed elsewhere
from PIL import Image

# Load the image
image = Image.open('prescription.jpg')
=======
from PIL import Image

# Load the image
image = Image.open('prescription_image.jpg')
>>>>>>> Stashed changes

# Use Tesseract to do OCR on the image
extracted_text = pytesseract.image_to_string(image)

print(extracted_text)
