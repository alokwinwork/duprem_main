import requests
import json

# Step 1: Take input in JSON
json_input = {"firstname": "Mukesh", "lastname": "Srivastava", "age": 20, "gender": "male"}

# Step 2: Send JSON to json-validate microservice
response = requests.post('http://json-validate:8080/validate', json=json_input)

if response.status_code == 200:
    # Step 3: Send validated JSON to change_to_csv microservice
    csv_response = requests.post('http://change_to_csv:8080/convert', json=json_input)

    if csv_response.status_code == 200:
        # Step 4: Get response in CSV from change_to_csv microservice
        csv_data = csv_response.json()

        # Step 5: Send CSV response to remove_duplicate microservice
        dedup_response = requests.post('http://remove_duplicate:8080/remove_duplicate', json=csv_data)

        if dedup_response.status_code == 200:
            # Step 6: Send deduplicated CSV response to convert_to_json microservice
            json_response = requests.post('http://convert_to_json:8080/convert', json=dedup_response.json())

            if json_response.status_code == 200:
                # Step 7: Get final JSON response and print output
                output = json_response.json()
                print(output)
            else:
                print('Error converting CSV to JSON')
        else:
            print('Error removing duplicates from CSV')
    else:
        print('Error converting JSON to CSV')
else:
    print('Invalid JSON input')
