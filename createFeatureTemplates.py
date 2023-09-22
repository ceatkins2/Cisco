import requests
import json
import os
from getpass import getpass
import urllib3

# no mo' warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Prompt for vManage IP or hostname
vmanage_host = input("Enter the IP address or hostname of vManage: ")

# Function to read JSON data from a file
def read_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Function to post data to the API
def post_data(session, data, headers):
    api_url = f"https://{vmanage_host}/dataservice/template/feature"
    response = session.post(api_url, json=data, headers=headers, verify=False)

    if response.status_code == 200:
        print(f"Successfully posted data for {filename}")
    else:
        print(f"Failed to post data for {filename}: {response.content}")

# Initialize session
session = requests.Session()

# Step 1: Login to establish session
login_url = f"https://{vmanage_host}/j_security_check"

# Prompt for username and password
username = input("Enter your username: ")
password = getpass("Enter your password: ")

login_payload = {
    "j_username": username,
    "j_password": password
}

login_response = session.post(login_url, data=login_payload, verify=False)

# Check if login was successful
if "login" in login_response.text:
    print("Login failed, exiting.")
    exit()

# Step 2: Get CSRF Token
token_url = f"https://{vmanage_host}/dataservice/client/token"
token_response = session.get(token_url, verify=False)
token = token_response.text

# Step 3: Prepare headers
headers = {
    "Content-Type": "application/json",
    "X-XSRF-TOKEN": token
}

# Read data from JSON files in the 'json_files' directory and post it
json_directory = 'FeatureTemplates-JSON'
json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]

for json_file in json_files:
    filename = os.path.join(json_directory, json_file)
    data = read_json_file(filename)
    post_data(session, data, headers)
