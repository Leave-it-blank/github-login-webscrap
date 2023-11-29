import os
from dotenv import load_dotenv
from index import login_github, fetch_pr_url

if __name__ == '__main__':
    load_dotenv()
    GIT_USERNAME = os.getenv('GIT_USERNAME')
    GIT_TOTP = os.getenv('GIT_TOTP')
    GIT_PASSWORD = os.getenv('GIT_PASSWORD')
    if not GIT_PASSWORD or not GIT_USERNAME or not GIT_TOTP:
        print("Add env vars.")
        exit()

    login_github(GIT_USERNAME, GIT_PASSWORD, GIT_TOTP)
    fetch_pr_url('metaverse-ventures', 'xMail')
