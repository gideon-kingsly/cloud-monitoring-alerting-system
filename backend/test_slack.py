from slack_alert import send_slack_alert

status = send_slack_alert(
    "🚨 Test Alert from Cloud Monitor"
)

print("Slack Response:", status)