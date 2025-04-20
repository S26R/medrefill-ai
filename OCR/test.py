import cv2
import pytesseract

# Path to the Tesseract executable (update this if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to your image
image_path = "I:\\Shounak Roy\\INFO\\IMPORTANT DOCUMENTS\\COLLEGE\\2ND YEAR\\4TH SEMESTER\\HACKATHON\\H4B\\medrefill-ai\\OCR\\captured_strip_2a.png"  # Replace with your image path

# Load the image
image = cv2.imread(image_path)

# Convert to grayscale for better OCR performance
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Optional: Thresholding to improve contrast (especially for handwriting)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Optional: Blur to reduce noise
blurred = cv2.GaussianBlur(thresh, (3, 3), 0)

# Perform OCR using Tesseract
text = pytesseract.image_to_string(blurred, config='--psm 6')  # PSM 6 assumes a block of text

# Print the OCR result
print("=== OCR Result ===")
print(text)
