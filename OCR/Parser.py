import cv2
import pytesseract
import json
import os
from datetime import datetime

# Ensure pytesseract can find the Tesseract executable
# Update the path if Tesseract is installed in a different location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Extract relevant medicine details from OCR text
def extract_medicine_details(text):
    lines = text.split('\n')
    details = {
        "medicine_names": [],
        "expiry_dates": [],
        "dosages": []
    }

    for line in lines:
        line_lower = line.lower()
        if "mg" in line_lower or "ml" in line_lower:
            details["dosages"].append(line.strip())
        if "exp" in line_lower or "expiry" in line_lower:
            details["expiry_dates"].append(line.strip())
        if any(keyword in line_lower for keyword in ["tablet", "cap", "syrup", "medicine", "tab"]):
            details["medicine_names"].append(line.strip())

    return details

# Capture image from webcam and extract text using OCR
def capture_and_extract():
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture an image or Q to quit.")
    img_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow("Capture - Press SPACE to scan", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27 or k % 256 == ord('q'):
            # ESC or Q pressed
            print("Closing capture.")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = f"captured_strip_{img_counter}.png"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} saved!")
            img_counter += 1

            # Convert to grayscale for better OCR
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to improve text visibility for OCR
            _, thr = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

            # Optionally, apply GaussianBlur to reduce noise
            blurred = cv2.GaussianBlur(thr, (5, 5), 0)

            # Use Tesseract to extract text from the processed image
            text = pytesseract.image_to_string(blurred, config='--psm 6')

            # Print OCR output for debugging
            print("=== OCR Output ===")
            print(text)

            # Extract medicine details
            details = extract_medicine_details(text)

            # Save to JSON
            json_name = f"medicine_details_{img_counter}.json"
            with open(json_name, 'w') as f:
                json.dump(details, f, indent=4)

            print(f"Extracted details saved to {json_name}.")

    cap.release()
    cv2.destroyAllWindows()

# Run the capture and extraction
capture_and_extract()
