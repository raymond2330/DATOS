import requests

# API base URL (adjust if you're not running on localhost:8000)
BASE_URL = "http://localhost:8000"

# User credentials
login_data = {
    "username": "sample@gmail.com",  # Use your registered email here
    "password": "12345678" # Use your registered password here
}

# Step 1: Get JWT token
login_url = f"{BASE_URL}/api/token/"
response = requests.post(login_url, json=login_data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens["access"]
    print("Login successful. Access token received.")

    # Step 2: Make authenticated request to a protected endpoint (e.g., research papers)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    protected_url = f"{BASE_URL}/api/research-papers/"
    protected_response = requests.get(protected_url, headers=headers)

    print(f"\nAuthenticated GET /research-papers/: {protected_response.status_code}")
    print(protected_response.json())

else:
    print("Login failed:", response.status_code)
    print(response.text)
