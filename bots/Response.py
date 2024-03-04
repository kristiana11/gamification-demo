import os
from sys import argv
import requests
import json


def post_comment(repo, issue_number, comment_body):
    # GitHub authentication token
    token = os.getenv('GH_TOKEN')

    # API endpoint for creating a comment on an issue
    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/comments'

    # Request headers
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Request body
    data = {
        'body': comment_body
    }

    # Send POST request to create a comment
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 201:
        print('Comment posted successfully.')
    else:
        print(f'Failed to post comment. Status code: {response.status_code}')
        print(response.text)


if __name__ == "__main__":
    # GitHub repository information
    repo = argv[1]

    # Issue number where the comment will be posted
    issue_number = argv[2]  # Replace with the actual issue number

    # Comment to be posted
    comment_body = 'Thank you for your comment!'

    # Post the comment
    post_comment(repo, issue_number, comment_body)

    print(f"you said: ${argv[3:]}")
