import requests
import json
from getpass import getpass
import urllib3

# no mo' warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Prompt for vManage IP or hostname
vmanage_host = input("Enter the IP address or hostname of vManage: ")

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

# Prepare headers
headers = {
    "Content-Type": "application/json",
    "X-XSRF-TOKEN": token
}

# Step 3: Read FeatureTemplateIDs.txt and fetch feature templates
with open("FeatureTemplateIDs.txt", "r") as f:
    lines = f.readlines()

    for line in lines:
        if "default" in line.lower():
            continue

        line_split = line.split(", ")
        template_id = line_split[0].split(": ")[1].strip()
        template_name = line_split[1].split(": ")[1].strip()

        feature_template_url = f"https://{vmanage_host}/dataservice/template/feature/object/{template_id}"
        feature_template_response = session.get(feature_template_url, headers=headers, verify=False)

        if feature_template_response.status_code == 200:
            feature_template = feature_template_response.json()

            # Step 4: Export to JSON file named after the feature template
            with open(f"{template_name}.json", 'w') as json_f:
                json.dump(feature_template, json_f, indent=4)

            print(f"Successfully exported feature template {template_name} to {template_name}.json")
        else:
            print(f"Failed to fetch feature template {template_name}: {feature_template_response.content}")
