from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Set up the URLs for the microservices
json_validate_url = "http://json-validate-service:8001"
change_to_csv_url = "http://change-to-csv-service:8002"
remove_duplicate_url = "http://remove-duplicate-service:8003"
convert_to_json_url = "http://convert-to-json-service:8004"

@app.route("/process", methods=["POST"])
def process_input():
    # Get the JSON input from the request body
    json_input = request.get_json()

    # Validate the JSON input using the json-validate microservice
    response = requests.post(json_validate_url, json=json_input)
    if response.status_code != 200:
        return "Error: Invalid JSON input"

    # Convert the JSON input to CSV using the change-to-csv microservice
    response = requests.post(change_to_csv_url, json=json_input)
    if response.status_code != 200:
        return "Error: Could not convert input to CSV"

    # Remove duplicates from the CSV using the remove-duplicate microservice
    csv_data = response.json()
    response = requests.post(remove_duplicate_url, json=csv_data)
    if response.status_code != 200:
        return "Error: Could not remove duplicates from CSV"

    # Convert the CSV data back to JSON using the convert-to-json microservice
    csv_data = response.json()
    response = requests.post(convert_to_json_url, json=csv_data)
    if response.status_code != 200:
        return "Error: Could not convert CSV data to JSON"

    # Return the final JSON output to the client
    json_output = response.json()
    return jsonify(json_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
