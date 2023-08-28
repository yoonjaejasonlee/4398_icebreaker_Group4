import json

import requests
from datetime import datetime
from config import AUTH_KEY, PIC, WEBHOOK

url = "https://courses.ianapplebaum.com/api/syllabus/1"

headers = {
    "Authorization": AUTH_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

response = requests.get(url, headers=headers)

print("Status", response.status_code)
data = response.json()

text = ""

def discord_webhook(text):
    data = {
        "username": "Syllabus Bot",
        "avatar_url": PIC,
        "embeds": [{
            "title": "CIS 4398 - Fall 2023",
            "thumbnail": {"url": PIC},
            "color": int(16744576),
            "timestamp": str(datetime.utcnow()),
            "description" : f"**{text}**",
        }]
    }

    result = requests.post(WEBHOOK, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


for i in range(len(data['events'])):
    line = f"({data['events'][i]['event_date']}) {data['events'][i]['event_name']}\n\n"
    text += line


discord_webhook(text)
