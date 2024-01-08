from bs4 import BeautifulSoup
import requests
import datetime
import sys
import os
import errno
from script import commit_to_private_repo
# Config
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

# Change this with your URL
url = "https://github.com/SharonAliyas5573"

# Get the page
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "html.parser")

# Get today's date
today = datetime.date.today()
# Format the date as a string
stringday = today.strftime("%Y-%m-%d")

# Get today's contributions
result = soup.find("td", {"data-date": stringday})

# Access token accessibility test
access_token = sys.argv[1]
gh_token = sys.argv[2]
if not access_token:
    print("Error: Access token is missing.")
    sys.exit(errno.EINVAL)

if result["data-level"] != "0":
    try:
        # Send push notification if contributions are not 0
        req = requests.get(f"https://push.techulus.com/api/v1/notify/{access_token}?title=Hi,Sharon👋&body=You have contributions today. Keep up the good work! 🚀")
        # Exit with an error status
        sys.exit(os.EX_OK)
    except Exception as e :
        print(e)
        sys.exit(errno.ECANCELED)
else:
    try:
        req = requests.get(f"https://push.techulus.com/api/v1/notify/{access_token}?title=Hi,Sharon👋&body=You haven't commited today. Don't lose your commit streak 🚀")
        commit_to_private_repo(gh_token)
        sys.exit(os.EX_OK)
    except Exception as e :
        print(e)
        sys.exit(errno.ECANCELED)
