from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    data = request.get_json()
    url = "http://validate-json:8080/validate"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        return {"error": "Invalid JSON format"}, 400

    url = "http://convert-to-csv:8080/convert"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    csv_data = r.json()["csv_data"]

    url = "http://remove-duplicates:8080/remove_duplicates"
    headers = {"Content-Type": "text/csv"}
    r = requests.post(url, data=csv_data, headers=headers)
    csv_data = r.content.decode()

    url = "http://convert-to-json:8080/convert"
    headers = {"Content-Type": "text/csv"}
    r = requests.post(url, data=csv_data, headers
