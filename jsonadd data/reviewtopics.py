import json

# Specify the path to your output JSON file
output_json_file_path = 'reviewstopic_data.json.json'

# Create a list of dictionaries, each representing an entry with an 'id' and 'reviewstopic'
reviewstopic_data = [
    {'id': 1, 'reviewstopic': 'Topic A'},
    {'id': 2, 'reviewstopic': 'Topic B'},
    {'id': 3, 'reviewstopic': 'Topic C'},
    {'id': 4, 'reviewstopic': 'Topic D'},
    # Add more entries as needed
]

# Write the data to the output JSON file
with open(output_json_file_path, 'w') as output_json_file:
    json.dump(reviewstopic_data, output_json_file, indent=2)

print(f'Data successfully created and stored in {output_json_file_path}')
