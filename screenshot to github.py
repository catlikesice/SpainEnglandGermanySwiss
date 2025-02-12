import pyautogui
import requests
import base64
import os
from datetime import datetime

# Replace these variables with your own information
GITHUB_TOKEN = 'your_github_token'
REPO_OWNER = 'your_github_username'
REPO_NAME = 'your_repository_name'
FILE_PATH_TEMPLATE = 'screenshot_{}.png'

def capture_screenshot():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = FILE_PATH_TEMPLATE.format(timestamp)
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)
    print(f"Screenshot saved to {file_path}")
    return file_path

def upload_to_github(file_path, repo_owner, repo_name, token):
    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode()

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{os.path.basename(file_path)}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    data = {
        "message": "Upload screenshot",
        "content": content
    }

    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    file_path = capture_screenshot()
    upload_to_github(file_path, REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
