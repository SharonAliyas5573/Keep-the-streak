from bs4 import BeautifulSoup
import requests
import datetime
import sys
import os
import errno

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
access_token = os.environ.get("PUSH_API_KEY")
if not access_token:
    print("Error: Access token is missing.")
    sys.exit(errno.EINVAL)

if result["data-level"] != "0":
    # Send push notification if contributions are not 0
    push_notification_command = (
        'echo "You have contributions today. Keep up the good work! 🚀" | '
        'curl -X POST -H "Authorization: Bearer $PUSH_API_KEY" -H "Content-Type: application/json" '
        '--data-binary @- https://api.pushbullet.com/v2/pushes'
    )

    os.system(push_notification_command)
    
    # Exit with an error status
    sys.exit(errno.ECANCELED)

# Exit with a success status if contributions are 0
sys.exit(os.EX_OK)
