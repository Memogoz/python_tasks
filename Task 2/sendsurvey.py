#!/bin/usr/env python3
# Script to create and send a survey to a list of emails

import os
import sys
from dotenv import load_dotenv
import requests
import json

load_dotenv()
access_token = os.getenv("TOKEN")
if access_token is None:
    print("Error: TOKEN environment variable not set.")
    sys.exit(1)

# Function to create the survey
def create_survey(token,questions):
    url = "https://api.surveymonkey.com/v3/surveys"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}" 
    }

    response = requests.post(url, json=questions, headers=headers)

    print(response.status_code, end=" --> ")
    if response.status_code ==201:
        print("Survey successfully created.")
    else:
        print("Error creating survey.\n")
        print(response.json())
        return None, None

    preview_url = response.json()["preview"]
    survey_id = response.json()["id"]
    return survey_id, preview_url

# Function to create the collector
def create_collector(token,survey_id):
    url = f"https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors"

    collector_config = {
        "type": "weblink",       
        "name": "My survey link",  
        "thank_you_page": {
            "is_enabled": True,
            "message": "Thank you for your answer"
        },
        "allow_multiple_responses": True,
        "anonymous_type": "partially_anonymous",
        "redirect_type": "url",
        "redirect_url": "https://exampleredirect.com/thankyou"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=collector_config, headers=headers)
    
    if response.status_code not in [200, 201, 204]:
        print("Error", response.status_code, "creating collector -->", response.json()["error"]["message"])
        return False
    
    print("Collector succesfully created")
    collector_id = response.json()["id"]
    return collector_id


# Check number of arguments
if len(sys.argv) != 3:
    print("Usage: ./sendsurvey.py <questions.json> <emails.txt>")
    sys.exit(1)

questions_file = sys.argv[1]
emails_file = sys.argv[2]

# Check if questions file exists has JSON format and can be read
try:
    with open(questions_file, 'r') as f:
        questions = json.load(f)
except FileNotFoundError:
    print(f"File {questions_file} not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error decoding JSON from file {questions_file}.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file {questions_file}: {e}")
    sys.exit(1)
# Check if questions file is empty
if not questions:
    print(f"File {questions_file} is empty.")
    sys.exit(1)

# Check if emails file exists and can be read
try:
    with open(emails_file, 'r') as f:
        #emails = f.readlines()
        emails = [email.strip() for email in f]
except FileNotFoundError:
    print(f"File {emails_file} not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file {emails_file}: {e}")
    sys.exit(1)
# Check if emails file is empty
if not emails:
    print(f"File {emails_file} is empty.")
    sys.exit(1)


# Create Survey
survey_id, survey_url = create_survey(token=access_token, questions=questions)

# Create collector to share the survey with the list of emails
collector_id = create_collector(token=access_token, survey_id=survey_id)
if not collector_id: print("Collector couldn't be created with free account.")

for email in emails:
    print(f'"Sending" survey to {email} as {survey_url}')
