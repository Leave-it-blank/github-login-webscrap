import requests
from bs4 import BeautifulSoup
import pyotp

payload = {}
head = {}
session = requests.session()


def login_github(username: str, password: str, userOTP: str):
    global session
    url = 'https://github.com/login'
    # Send a GET request
    resp = session.get(url)
    print(resp.status_code)

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = ""
    timestamp = ""
    timestamp_secret = ""

    # Check if the request was successful (status code 200)
    if resp.status_code == 200:
        csrf_token = soup.find("input", {"name": "authenticity_token"}).get("value")
        timestamp = soup.find("input", {"name": "timestamp"}).get("value")
        timestamp_secret = soup.find("input", {"name": "timestamp_secret"}).get("value")

    else:
        print(f'Authentication failed. Status code: {resp.status_code}')
    global payload
    payload = {"login": username, "password": password, "authenticity_token": csrf_token,
               "timestamp": timestamp, "timestamp_secret": timestamp_secret}

    global head
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"}

    resp = session.post('https://github.com/session', data=payload, headers=head, allow_redirects=False)
    print(resp.text)
    print(resp.status_code)

    if resp.status_code == 302:
        URL = "https://github.com/sessions/two-factor/app"
        res = session.get(URL)
        print(res.status_code)

        if res.status_code == 200:
            totp = pyotp.TOTP(userOTP)
            otp = totp.now()  # => '492039'

            soup = BeautifulSoup(res.text, 'html.parser')

            csrf_token = soup.find("input", {"name": "authenticity_token"}).get("value")
            payload = {
                "authenticity_token": csrf_token,
                "app_otp": otp,
            }
            head = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            resp = session.post('https://github.com/sessions/two-factor', data=payload, headers=head,
                                allow_redirects=False)
            if resp.status_code == 302:
                print("Logged in...")
            else:
                print("Failed... to login.")


def fetch_pr_url(name: str, repo: str):
    global session
    URL = "https://github.com/" + name + "/" + repo + "/pulls"
    res = session.get(URL)
    if res.status_code == 200:
        pull_url: str = ""
        print("Fetching github url with status code : " + str(res.status_code))
        soup = BeautifulSoup(res.content, "html.parser")

        job_elements = soup.find_all("a",
                                     class_="Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")
        if len(job_elements) > 0:
            pull_url = "https://github.com" + job_elements[0]["href"]
            print(pull_url, end="\n" * 2)
        # print(pull_url)
    else:
        print("failed to fetch request with error code: " + str(res.status_code))
