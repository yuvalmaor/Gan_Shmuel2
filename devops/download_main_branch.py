from flask import Flask
import requests
import os

app = Flask(__name__)

REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')
GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

def download_main_branch():
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/tarball'

    headers = {
        'Authorization': f'Bearer {GITHUB_ACCESS_TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        path = './devops/tmp/'
        with open(f"}{path}{REPO_NAME}.tar.gz", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        app.logger.info('Pull request created successfully')
        return path 
    else:
        app.logger.error(f'Failed to create pull request: {response.status_code}, {response.text}')
        return False
