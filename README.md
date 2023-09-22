# SDWAN
SDWAN Automation

This repository contains Python scripts that interact with Cisco's vManage API to perform various operations.

The goal of the project was to reduce the amount of time creating feature templates for new SDWAN environments. Given about a dozen of so "generic" templates that we usually create,
these scripts serve to let you copy existing Feature Templates and use them as a boilerplate to replicate to new environments.


## Features
Authentication with vManage.
Fetch feature template IDs and names.
Export individual feature templates to JSON files.
Create new feature templates from exported JSON

## Prerequisites
Python 3.x
requests library
Cisco vManage access


## Installation
Clone the repository and navigate to the project folder.

```
git clone https://github.com/ceatkins2/SDWAN.git
cd SDWAN
Install the required Python packages.
```

```
pip install -r requirements.txt
```

## Usage
### Step 1
Create a folder named "FeatureTemplates-JSON" in the directory youll be working out of (this is used in step 3)

### Step 2
Export Feature Template IDs and Template Names
Run the getFeatureTemplateId.py script.

```
python3 getFeatureTemplateId.py
#enter in required infor for vmanage and credentials
```
This creates a text file called "FeatureTemplateIDs.txt" in your local directory

### Step 3
Create individual JSON files per template ID in the "FeatureTemplateIDs.txt" (This ignores default feature templates created by Cisco that ship with vManage)

```
python3 exportFeatureTemplateAsJSON.py
#enter in required infor for vmanage and credentials
```
This will create a JSON file for each non-default feature template read from the "FeatureTemplateIDs.txt" in Step 2

### Step 4
Move the new JSON files to the "FeatureTemplates-JSON" folder created in Step 1

### Step 5
Create new feature templates using the JSON files in "FeatureTemplates-JSON"
```
python3 createFeatureTemplates.py
#enter in required infor for vmanage and credentials
```




Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
MIT

Feel free to copy this and adjust it according to the specific details of your project. Save this as a README.md file in the root directory of your GitHub repository.




