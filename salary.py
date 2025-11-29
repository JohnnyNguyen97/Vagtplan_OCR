WEEKEND_DAYS = {"Saturday", "Sunday", "Lørdag", "Søndag"}

def calculate_salary(shifts, weekday_rate, weekend_rate=None):
    total_pay = 0

    for s in shifts:
        is_weekend = s["weekday"] in WEEKEND_DAYS
        rate = weekend_rate if (weekend_rate and is_weekend) else weekday_rate
        total_pay += s["hours"] * rate

    return round(total_pay, 2)
