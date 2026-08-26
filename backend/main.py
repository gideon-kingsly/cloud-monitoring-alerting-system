from fastapi import FastAPI
from monitor import get_system_stats, check_website, get_health_status
from alerts import check_alerts, check_website_alerts
from database import cursor
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import cursor

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Cloud Monitoring API Running"}

@app.get("/stats")
def stats():
    return get_system_stats()

@app.get("/website")
def website_status():
    return check_website("https://www.google.com")

@app.get("/health")
def health():
    return get_health_status()

@app.get("/websites")
def websites_status():
    websites = [
    "https://google.com",
    "https://github.com",
    "https://aws.amazon.com",
    "https://azure.microsoft.com",
    "https://chatgpt.com"
    ]

    results = []

    for website in websites:
        results.append(check_website(website))

    return results

@app.get("/alerts")
def alerts():
    stats = get_system_stats()
    return {
        "alerts": check_alerts(stats)
    }



@app.get("/history")
def history():

    cursor.execute("""
    SELECT timestamp,
           cpu_usage,
           memory_usage,
           disk_usage
    FROM system_stats
    ORDER BY id DESC
    LIMIT 10
    """)

    rows = cursor.fetchall()

    return rows

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    # Current system statistics
    stats = get_system_stats()

    # Health status
    health = get_health_status()

    # Website monitoring
    websites = [
        check_website("https://www.google.com"),
        check_website("https://github.com"),
        check_website("https://aws.amazon.com"),
        check_website("https://azure.microsoft.com"),
        check_website("https://chatgpt.com"),
    ]

    check_website_alerts(websites)

    # Alerts
    alerts = check_alerts(stats)

    # ==============================
    # System History
    # ==============================

    cursor.execute("""
        SELECT timestamp,
               cpu_usage,
               memory_usage,
               disk_usage
        FROM system_stats
        ORDER BY id DESC
        LIMIT 100
    """)

    history = cursor.fetchall()

    # ==============================
    # Website History
    # ==============================

    cursor.execute("""
        SELECT timestamp,
               website,
               status,
               response_time
        FROM website_history
        ORDER BY id DESC
        LIMIT 100
    """)

    website_history_data = cursor.fetchall()

    # ==============================
    # Chart Data
    # ==============================

    timestamps = [row[0][-8:] for row in history][::-1]
    cpu_history = [row[1] for row in history][::-1]
    memory_history = [row[2] for row in history][::-1]
    disk_history = [row[3] for row in history][::-1]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "stats": stats,
            "health": health,
            "websites": websites,
            "alerts": alerts,
            "history": history,
            "website_history": website_history_data,
            "timestamps": timestamps,
            "cpu_history": cpu_history,
            "memory_history": memory_history,
            "disk_history": disk_history
        }
    )

@app.get("/website-history")
def website_history():

    cursor.execute("""
        SELECT timestamp,
               website,
               status,
               response_time
        FROM website_history
        ORDER BY id DESC
        LIMIT 100
    """)

    return cursor.fetchall()