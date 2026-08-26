import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

conn = sqlite3.connect(
    "monitor.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================
# System Statistics Table
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS system_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    cpu_usage REAL,
    memory_usage REAL,
    disk_usage REAL
)
""")

conn.commit()

# =====================================
# Website History Table
# =====================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS website_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    website TEXT,
    status TEXT,
    response_time REAL
)
""")

conn.commit()


# =====================================
# Save Website History
# =====================================

def save_website_history(
    website,
    status,
    response_time
):

    timestamp = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO website_history (
            timestamp,
            website,
            status,
            response_time
        )
        VALUES (?, ?, ?, ?)
    """, (
        timestamp,
        website,
        status,
        response_time
    ))

    conn.commit()