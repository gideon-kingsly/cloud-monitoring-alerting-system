import requests
import os

def send_slack_alert(message):

    import os

    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

    payload = {
        "text": message
    }

    response = requests.post(
        webhook_url,
        json=payload
    )

    return response.status_code