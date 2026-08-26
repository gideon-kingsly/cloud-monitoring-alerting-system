import os
import time
import psutil
import requests

from datetime import datetime
from zoneinfo import ZoneInfo

from logger import write_log
from database import conn, cursor, save_website_history

def get_system_stats():

    disk_path = "C:\\" if os.name == "nt" else "/"

    stats = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage(
            disk_path
        ).percent
    }

    timestamp = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO system_stats (
        timestamp,
        cpu_usage,
        memory_usage,
        disk_usage
    )
    VALUES (?, ?, ?, ?)
    """, (
        timestamp,
        stats["cpu_usage"],
        stats["memory_usage"],
        stats["disk_usage"]
    ))

    conn.commit()

    write_log(
        f"{timestamp} | "
        f"CPU={stats['cpu_usage']}% | "
        f"RAM={stats['memory_usage']}% | "
        f"Disk={stats['disk_usage']}%"
    )

    return stats

# Website Monitoring
# Website Monitoring
def check_website(url):
    try:
        start_time = time.time()

        response = requests.get(url, timeout=5)

        response_time = round((time.time() - start_time) * 1000, 2)

        # Save successful result to database
        save_website_history(
            url,
            "UP",
            response_time
        )

        return {
            "url": url,
            "status": "UP",
            "status_code": response.status_code,
            "response_time_ms": response_time
        }

    except requests.exceptions.RequestException as e:

        # Save failed result to database
        save_website_history(
            url,
            "DOWN",
            None
        )

        return {
            "url": url,
            "status": "DOWN",
            "error": str(e)
        }

# Health Check Summary
def get_health_status():
    stats = get_system_stats()

    cpu_status = "Healthy"
    memory_status = "Healthy"
    disk_status = "Healthy"

    if stats["cpu_usage"] > 90:
        cpu_status = "Critical"

    if stats["memory_usage"] > 90:
        memory_status = "Critical"

    if stats["disk_usage"] > 90:
        disk_status = "Critical"

    return {
        "cpu": cpu_status,
        "memory": memory_status,
        "disk": disk_status
    }