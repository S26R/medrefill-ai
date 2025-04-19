with open('medicine_details_1.json', 'r') as file:
    contents = file.read()
    print(contents)
import json

with open('medicine_details_1.json', 'r') as file:
    data = json.load(file)

print(data['medicine_names'])  # Output: Paracetamol
print(data['expiry_dates'])  # Output: 2025-12-31
print(data['dosages'])  # Output: 500mg