import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

def fetch_time():
    api_url = "http://worldtimeapi.org/api/timezone/Etc/UTC"
    retries = 2
    for attempt in range(retries + 1):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            current_utc_time_str = data["datetime"]
            current_utc_time = datetime.fromisoformat(current_utc_time_str.replace("Z", "+00:00"))
            break
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                time.sleep(1)  
                continue
            else:
                current_utc_time = datetime.utcnow()
                break


    next_week = current_utc_time + timedelta(weeks=1)
    try:
        next_month = current_utc_time + relativedelta(months=1)
    except ValueError:

        next_month = (current_utc_time + timedelta(days=32)).replace(day=1)
    next_year = current_utc_time + relativedelta(years=1)


    current_utc_time_iso = current_utc_time.isoformat()
    next_week_iso = next_week.isoformat()
    next_month_iso = next_month.isoformat()
    next_year_iso = next_year.isoformat()


    return {
        "current_time": current_utc_time_iso,
        "Weekly": next_week_iso,
        "Monthly": next_month_iso,
        "Yearly": next_year_iso
    }


