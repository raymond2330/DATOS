import os
import requests
from django.test import TestCase
from django.urls import reverse
from .models import ResearchPaper, User, Category
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

# API base URL (adjust if you're not running on localhost:8000)
BASE_URL = "http://localhost:8000"

# User credentials
login_data = {
    "username": "admin@gmail.com",  # Use your registered email here
    "password": "12345678" # Use your registered password here
}

# Test for uploading datasets and research papers
def test_upload_to_drive():
    # Step 1: Get JWT token
    login_url = f"{BASE_URL}/api/token/"
    response = requests.post(login_url, json=login_data)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access"]
        print("Login successful. Access token received.")

        # Step 2: Upload a research paper
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        upload_url = f"{BASE_URL}/api/upload-to-drive/"

        research_paper_file = {
            "file": ("Thesis 2_Chapter 1-5.pdf", open(r"C:\Users\Raymond\Desktop\DATOS\backend\Thesis 2_Chapter 1-5.pdf", "rb")),
            "file_type": (None, "research_paper"),
            "title": (None, "Thesis Chapter 1-5"),
            "description": (None, "This is a test research paper"),
        }

        research_paper_response = requests.post(upload_url, headers=headers, files=research_paper_file)
        print(f"\nUpload Research Paper: {research_paper_response.status_code}")

        if research_paper_response.status_code == 200:
            try:
                response_json = research_paper_response.json()
                print(response_json)
            except requests.exceptions.JSONDecodeError:
                print("Failed to decode JSON. Raw response:")
                print(research_paper_response.text)
        else:
            print("Error during upload. Status code:", research_paper_response.status_code)
            print("Response:", research_paper_response.text)

    else:
        print("Login failed:", response.status_code)
        print(response.text)

test_upload_to_drive()

def test_view_paper():
    print("Starting test_view_paper...")

    try:
        # Step 1: Get JWT token
        login_url = f"{BASE_URL}/api/token/"
        response = requests.post(login_url, json=login_data)

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access"]
            print("Login successful. Access token received.")

            # Step 2: Access the view_paper endpoint
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            view_paper_url = f"{BASE_URL}/api/view-paper/1H2wgXbCS9fLcEK6YHzZEmbCSg7oPME44/"

            response = requests.get(view_paper_url, headers=headers)
            print(f"\nView Paper Response: {response.status_code}")

            if response.status_code == 302:
                print("Redirected to:", response.headers.get("Location"))
            elif response.status_code == 200:
                print("Rendered successfully.")
                # print(response.text)  # Print the HTML content for debugging
            else:
                print("Error during view paper. Status code:", response.status_code)
                print("Response:", response.text)
        else:
            print("Login failed:", response.status_code)
            print(response.text)

    except Exception as e:
        print("An error occurred:", str(e))

# test_view_paper()

def test_request_access():
    print("Starting test_request_access...")

    try:
        # Step 1: Get JWT token
        login_url = f"{BASE_URL}/api/token/"
        response = requests.post(login_url, json=login_data)

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access"]
            print("Login successful. Access token received.")

            # Step 2: Submit an access request
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            request_access_url = f"{BASE_URL}/api/request-access/"

            request_data = {
                "paper_id": 32,
                # "dataset_id": 1,
                "purpose": "Research purposes",
                "reason_for_access": "I need this paper for my thesis."
            }

            response = requests.post(request_access_url, headers=headers, json=request_data)
            print(f"\nRequest Access Response: {response.status_code}")

            if response.status_code == 201:
                print("Access request submitted successfully.")
                print("Response:", response.json())
            else:
                print("Error during access request. Status code:", response.status_code)
                print("Response:", response.text)
        else:
            print("Login failed:", response.status_code)
            print(response.text)

    except Exception as e:
        print("An error occurred:", str(e))

# test_request_access()

def test_update_request_permission():
    print("Starting test_update_request_permission...")

    try:
        # Step 1: Get JWT token
        login_url = f"{BASE_URL}/api/token/"
        response = requests.post(login_url, json=login_data)

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens["access"]
            print("Admin login successful. Access token received.")

            # Step 2: Update the status of a request
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            request_id = 14  # Replace with a valid request ID
            update_url = f"{BASE_URL}/api/update-request-permission/{request_id}/"

            update_data = {
                "status": "approved"
            }

            update_response = requests.patch(update_url, json=update_data, headers=headers)
            print(f"Update Request Permission Response: {update_response.status_code}")

            if update_response.status_code == 200:
                print("Request permission updated successfully.")
                print("Response:", update_response.json())
            else:
                print("Error during request permission update. Status code:", update_response.status_code)
                print("Response:", update_response.text)
        else:
            print("Admin login failed:", login_response.status_code)
            print(login_response.text)

    except Exception as e:
        print("An error occurred:", str(e))

# test_update_request_permission()