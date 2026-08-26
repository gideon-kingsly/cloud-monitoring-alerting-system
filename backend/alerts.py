from email_alert import send_email_alert
from slack_alert import send_slack_alert


# System resource alerts
def check_alerts(stats):

    alerts = []

    if stats["cpu_usage"] > 90:
        alerts.append(f"High CPU Usage: {stats['cpu_usage']}%")

    if stats["memory_usage"] > 90:
        alerts.append(f"High Memory Usage: {stats['memory_usage']}%")

    if stats["disk_usage"] > 90:
        alerts.append(f"High Disk Usage: {stats['disk_usage']}%")

    if alerts:
        message = "\n".join(alerts)

        send_email_alert(
            "Cloud Monitor Alert",
            message
        )

        send_slack_alert(
            f"🚨 Cloud Monitor Alert\n{message}"
        )

    return alerts


# Website DOWN alerts
def check_website_alerts(websites):

    for website in websites:

        if website["status"] == "DOWN":

            message = f"""
🚨 WEBSITE DOWN ALERT

Website: {website['url']}
Status: DOWN
"""

            send_email_alert(
                "Website Down Alert",
                message
            )

            send_slack_alert(message)