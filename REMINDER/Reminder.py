import cv2
import pytesseract
import json
import os
from datetime import datetime

# Ensure pytesseract can find the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Extract relevant medicine details from OCR text (for both printed and handwritten)
def extract_medicine_details(text):
    lines = text.split('\n')
    details = {
        "medicine_names": [],
        "expiry_dates": [],
        "dosages": [],
        "timings": []
    }

    for line in lines:
        line_lower = line.lower()
        if "mg" in line_lower or "ml" in line_lower:
            details["dosages"].append(line.strip())
        if "exp" in line_lower or "expiry" in line_lower:
            details["expiry_dates"].append(line.strip())
        if any(keyword in line_lower for keyword in ["tablet", "cap", "syrup", "medicine", "tab"]):
            details["medicine_names"].append(line.strip())
        if "morning" in line_lower or "afternoon" in line_lower or "night" in line_lower:
            details["timings"].append(line.strip())

    return details

# Preprocess image for better OCR results (works for both printed and handwritten text)
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding for handwritten and printed text
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh

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

            # Preprocess the captured image for better OCR
            processed_image = preprocess_image(frame)

            # Extract text using OCR
            text = pytesseract.image_to_string(processed_image)

            # Extract medicine details
            details = extract_medicine_details(text)

            # Save to JSON
            json_name = f"medicine_details_{img_counter}.json"
            with open(json_name, 'w') as f:
                json.dump(details, f, indent=4)

            print(f"Extracted details saved to {json_name}.")
            print("=== OCR Output ===")
            print(text)

    cap.release()
    cv2.destroyAllWindows()

# Reminder logic based on extracted medicine details
def schedule_reminders(timings):
    print("Scheduling reminders for medication based on extracted timings...")
    for timing in timings:
        # Here you can add a logic to schedule reminders
        # For simplicity, we will just print it
        print(f"Reminder: Take medicine at {timing}")

# Running the capture and extraction, and reminder scheduling
def run():
    capture_and_extract()
    # Assuming we have extracted timings from the OCR output
    # For demonstration, we hard-code the timings here, but you can get it from the extracted details
    timings = ["8:00 AM", "2:00 PM", "8:00 PM"]
    schedule_reminders(timings)

# Run the program
run()
