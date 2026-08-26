import os
import requests


def send_slack_alert(message):

    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not slack_webhook_url:
        return {
            "success": False,
            "message": "SLACK_WEBHOOK_URL is not configured"
        }

    payload = {
        "text": message
    }

    try:
        response = requests.post(
            slack_webhook_url,
            json=payload,
            timeout=10
        )

        return {
            "success": response.ok,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "message": str(e)
        }