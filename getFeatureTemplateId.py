import requests
import json
import os
from getpass import getpass
import urllib3

# no mo' warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Prompt for vManage IP or hostname
vmanage_host = input("Enter the IP address or hostname of vManage: ")

# Initialize session
session = requests.Session()

# Login to establish session
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

# Get CSRF Token
token_url = f"https://{vmanage_host}/dataservice/client/token"
token_response = session.get(token_url, verify=False)
token = token_response.text

# Prepare headers
headers = {
    "Content-Type": "application/json",
    "X-XSRF-TOKEN": token
}

# Fetch all feature template IDs and names
feature_template_url = f"https://{vmanage_host}/dataservice/template/feature"

feature_template_response = session.get(feature_template_url, headers=headers, verify=False)

if feature_template_response.status_code == 200:
    feature_templates = feature_template_response.json()["data"]

    # Write the feature template IDs and names to a text file
    with open("FeatureTemplateIDs.txt", "w") as f:
        for template in feature_templates:
            template_id = template.get("templateId", "N/A")
            template_name = template.get("templateName", "N/A")
            f.write(f"ID: {template_id}, Name: {template_name}\n")
            
    print("Successfully fetched and saved feature template IDs and names to FeatureTemplateIDs.txt")
else:
    print(f"Failed to fetch feature template IDs: {feature_template_response.content}")


