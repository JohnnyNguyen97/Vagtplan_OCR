from datetime import datetime, timedelta

def calculate_hours(shifts):
    for s in shifts:
        start = datetime.strptime(s["start"], "%H:%M")
        end = datetime.strptime(s["end"], "%H:%M")
        # Hvis slut er tidligere end start og læg en dag til
        if end <= start:
            end = end + timedelta(days=1)

        duration = (end - start) - timedelta(minutes=s.get("pause_min", 0))
        seconds = max(0, duration.total_seconds())
        s["hours"] = round(seconds / 3600, 2)

    total = sum(s.get("hours", 0) for s in shifts)
    return total
