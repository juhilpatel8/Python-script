import requests
from requests.auth import HTTPBasicAuth

# Configuration
GITHUB_TOKEN = 'your_github_token_here'
REPO_OWNER = 'your_username_or_org'
REPO_NAME = 'your_repository_name'
OLD_FILE_PATH = 'path/to/old_file_name.txt'
NEW_FILE_PATH = 'path/to/new_file_name.txt'
BRANCH_NAME = 'main'  # or your target branch

# GitHub API endpoints
API_BASE_URL = 'https://api.github.com'
REPO_URL = f'{API_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}'
CONTENT_URL = f'{REPO_URL}/contents/{OLD_FILE_PATH}?ref={BRANCH_NAME}'

# Fetch the file's current details
response = requests.get(CONTENT_URL, auth=HTTPBasicAuth('username', GITHUB_TOKEN))
response.raise_for_status()

file_info = response.json()
sha = file_info['sha']
message = 'Renaming file using GitHub API'

# Prepare the payload for the rename operation
data = {
    'message': message,
    'sha': sha,
    'content': file_info['content'],
    'branch': BRANCH_NAME
}

# Create the new file with the new name
rename_url = f'{REPO_URL}/contents/{NEW_FILE_PATH}'
response = requests.put(rename_url, json=data, auth=HTTPBasicAuth('username', GITHUB_TOKEN))
response.raise_for_status()

# Delete the old file
delete_url = f'{REPO_URL}/contents/{OLD_FILE_PATH}'
delete_data = {
    'message': 'Deleting old file after rename',
    'sha': sha,
    'branch': BRANCH_NAME
}
response = requests.delete(delete_url, json=delete_data, auth=HTTPBasicAuth('username', GITHUB_TOKEN))
response.raise_for_status()

print('File renamed successfully!')
