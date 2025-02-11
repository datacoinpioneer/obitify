import requests
import json

# GitHub API endpoint for creating/updating a file
url = "https://api.github.com/repos/{owner}/{repo}/contents/docs/requirements.md"

# Authentication with GitHub token
headers = {
    'Authorization': 'token ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

# The content to be added (markdown format)
content = """
# Functional Requirements for MyApp

## 1. User Authentication
- **Feature**: Users must be able to log in and log out.
- **Requirements**:
  - Login using Google OAuth.
  - Password recovery through email.
  - User role management (Admin, Regular User).

## 2. User Profile Management
- **Feature**: Users can update their profiles.
- **Requirements**:
  - Allow users to update profile picture, name, and contact information.
  - Admins can manage users' permissions.
"""

# Convert the markdown content to Base64 (GitHub API requires Base64 encoding for content)
encoded_content = content.encode("utf-8")
base64_content = base64.b64encode(encoded_content).decode("utf-8")

# Data to be sent to the API
data = {
    "message": "Update functional requirements",
    "content": base64_content,
    "branch": "main"  # or the branch you're working on
}

# Send the POST request to GitHub to update the file
response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
    print("Documentation created/updated successfully!")
else:
    print(f"Failed to update documentation: {response.status_code}")
