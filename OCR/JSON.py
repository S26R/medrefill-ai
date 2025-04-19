import json

# Replace 'yourfile.json' with the actual path to your file
with open('medicine_details_1.json', 'r') as f:
    data = json.load(f)

# Print the entire content
print(json.dumps(data, indent=4))  # nicely formatted output
