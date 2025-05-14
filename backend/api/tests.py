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
            "description": (None, "This is a test research paper")
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

# test_upload_to_drive()


def test_view_paper():
    print("Starting test_view_paper...")  # Debugging start point

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
                print(1)
            elif response.status_code == 200:
                print("Preview rendered successfully.")
                print(2)
                print(response.text)  # Print the HTML content for debugging
            else:
                print("Error during view paper. Status code:", response.status_code)
                print(3)
                print("Response:", response.text)
        else:
            print("Login failed:", response.status_code)
            print(4)
            print(response.text)

    except Exception as e:
        print(5)
        print("An error occurred:", str(e))

test_view_paper()