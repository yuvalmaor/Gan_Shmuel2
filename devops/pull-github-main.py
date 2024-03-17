from flask import Flask, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load configuration from .env file
load_dotenv()

REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
GITHUB_API_URL = os.getenv('GITHUB_API_URL')


@app.route('/webhook', methods=['POST'])
def pull_from_github():
# def main():
    data = request.get_json()

    if not is_valid_request(data):
        app.logger.warning('Invalid webhook request')
        return 'Invalid request', 400

    # if pull_from_github():
    #     return 'Success: Pulled from GitHub'
    # else:
    #     return 'Failed to pull from GitHub', 500


    if not all([REPO_OWNER, REPO_NAME, GITHUB_ACCESS_TOKEN, GITHUB_API_URL]):
        app.logger.error('GitHub configuration missing')
        return False

    headers = {
        'Authorization': f'token {GITHUB_ACCESS_TOKEN}'
    }
    url = f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls'
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        app.logger.info('Pull request created successfully')
        return True
    else:
        app.logger.error(f'Failed to create pull request: {response.status_code}, {response.text}')
        return False


def is_valid_request(data):
    return True


# if __name__ == '__main__':
#     main()
    # app.run(debug=True)
