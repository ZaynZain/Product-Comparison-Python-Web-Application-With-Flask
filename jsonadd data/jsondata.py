import json
import csv

# Specify the paths to your JSON files and CSV file
main_json_file_path = 'combined_data.json'
additional_json_file_path = 'reviewstopic_data.json.json'
csv_file_path = 'jsoncsv.csv'

# Read main JSON data from the main input file
with open(main_json_file_path, 'r') as main_json_file:
    main_data = json.load(main_json_file)

# Extract header from the first element in the main JSON data
header = list(main_data[0].keys())

# Add the new header field 'reviewstopic'
header.append('reviewstopic')

# Read additional JSON data from the second input file
with open(additional_json_file_path, 'r') as additional_json_file:
    additional_data = json.load(additional_json_file)

# Create a dictionary mapping each entry's ID to its 'reviewstopic' value
reviewstopic_mapping = {entry.get('id', None): entry.get('reviewstopic', None) for entry in additional_data}

# Write data to CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the modified header to the CSV file
    csv_writer.writerow(header)

    # Write the data rows to the CSV file
    for row in main_data:
        # Get the 'reviewstopic' value based on the entry's ID
        reviewstopic_value = reviewstopic_mapping.get(row.get('id', None), '')

        # Write the data row to the CSV file, including the 'reviewstopic' value and 'reviews' field
        csv_writer.writerow([row.get(key, '') for key in header[:-2]] + [reviewstopic_value, row.get('reviews', '')])

print(f'Data successfully converted and stored in {csv_file_path}')
