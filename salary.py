WEEKEND_DAYS = {"Saturday", "Sunday", "Lørdag", "Søndag"}

# Danish tax rates 2025 (per pay slip)
AM_BIDRAG_RATE = 0.08  # 8%
A_SKAT_RATE = 0.39  # 39%
ATP_PER_HOUR = 15.68  # ATP fixed amount per hour (2025 estimate, adjust as needed)
FORSIKRING_PER_HOUR = 0  # Optional insurance, set by user if needed

def calculate_salary_detailed(shifts, hourly_rate, weekend_rate=None):
    """
    Calculate gross salary, taxes, and net pay.
    
    Returns dict with:
    - gross_pay: Total before taxes
    - am_bidrag: 8% employee contribution
    - a_skat: 8% income tax
    - atp: ATP pension contribution
    - forsikring: Optional insurance
    - total_taxes: Sum of all deductions
    - net_pay: Gross minus all taxes
    - total_hours: Total hours worked
    - weekend_hours: Weekend hours (if weekend_rate differs)
    """
    
    total_hours = 0
    weekend_hours = 0
    gross_pay = 0
    
    for s in shifts:
        is_weekend = s["weekday"] in WEEKEND_DAYS
        hours = s.get("hours", 0)
        total_hours += hours
        
        if is_weekend:
            weekend_hours += hours
            if weekend_rate:
                gross_pay += hours * weekend_rate
            else:
                gross_pay += hours * hourly_rate
        else:
            gross_pay += hours * hourly_rate
    
    # Calculate taxes
    am_bidrag = round(gross_pay * AM_BIDRAG_RATE, 2)
    a_skat = round(gross_pay * A_SKAT_RATE, 2)
    atp = round(total_hours * ATP_PER_HOUR, 2)
    forsikring = round(total_hours * FORSIKRING_PER_HOUR, 2)
    
    total_taxes = am_bidrag + a_skat + atp + forsikring
    net_pay = round(gross_pay - total_taxes, 2)
    
    return {
        "total_hours": total_hours,
        "weekend_hours": weekend_hours,
        "weekday_hours": total_hours - weekend_hours,
        "gross_pay": gross_pay,
        "am_bidrag": am_bidrag,
        "a_skat": a_skat,
        "atp": atp,
        "forsikring": forsikring,
        "total_taxes": total_taxes,
        "net_pay": net_pay
    }


def calculate_salary(shifts, weekday_rate, weekend_rate=None):
    """Legacy function for backwards compatibility."""
    result = calculate_salary_detailed(shifts, weekday_rate, weekend_rate)
    return result["net_pay"]

