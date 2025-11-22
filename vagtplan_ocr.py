import re
from datetime import datetime, timedelta
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Hvis Tesseract ligger et andet sted på Windows, sæt path her:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMAGE_PATH = r"C:\Users\Johnny\Desktop\Vagter\50.png"  # ← skift stien til dit eget billede

def extract_text(path):
    img = Image.open(path)
    # Prøv både dansk og engelsk træningsdata for bedre OCR på danske planer
    text = pytesseract.image_to_string(img, lang="dan+eng")
    return text

def parse_shifts(text):
    # Rens OCR-tekst for mærkelige tegn
    text = text.replace("‘", "").replace("’", "").replace("`", "")

    # Matcher dage med eventuel dagnummer
    day_pattern = r"(?i)\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Man|Tir|Ons|Tor|Fre|L[oø]r|S[oø]n|Mandag|Tirsdag|Onsdag|Torsdag|Fredag|L[øo]rdag|S[øo]ndag)\b\s*(\d{1,2})?"
    # Matcher tider
    time_pattern = r"(\d{1,2}:\d{2})\s*[-–]\s*(\d{1,2}:\d{2})(?:\s*\(?([0-9]{1,3})\)?)?"

    shifts = []
    current_day = None

    # Find alle dage først
    day_matches = list(re.finditer(day_pattern, text))
    time_matches = list(re.finditer(time_pattern, text))

    day_idx = 0
    for time_match in time_matches:
        # Tildel den nærmeste dag før tiden
        while day_idx + 1 < len(day_matches) and day_matches[day_idx + 1].start() < time_match.start():
            day_idx += 1
        day_match = day_matches[day_idx]

        weekday = day_match.group(1)
        day_num = int(day_match.group(2)) if day_match.group(2) else None

        start = time_match.group(1)
        end = time_match.group(2)
        pause_group = time_match.group(3)
        pause = int(pause_group) if pause_group and pause_group.isdigit() else 0

        shifts.append({
            "weekday": weekday,
            "day": day_num,
            "start": start,
            "end": end,
            "pause_min": pause
        })

    return shifts


def calculate_hours(shifts):
    for s in shifts:
        start = datetime.strptime(s["start"], "%H:%M")
        end = datetime.strptime(s["end"], "%H:%M")
        # Hvis slut er tidligere end start, antag overnatning og læg en dag til
        if end <= start:
            end = end + timedelta(days=1)

        duration = (end - start) - timedelta(minutes=s.get("pause_min", 0))
        seconds = max(0, duration.total_seconds())
        s["hours"] = round(seconds / 3600, 2)

    total = sum(s.get("hours", 0) for s in shifts)
    return total

def main():
    print("🔍 Læser billede...")
    text = extract_text(IMAGE_PATH)

    print("\n📄 OCR indhold:")
    print("--------------------------------")
    print(text)
    print("--------------------------------")

    shifts = parse_shifts(text)
    # Beregn timer før vi forsøger at udskrive dem
    total = calculate_hours(shifts)

    print("\n📅 Udtræk af vagter:")
    if not shifts:
        print("Ingen vagter fundet i OCR-teksten. Prøv 'lang' parameter eller tjek billedet.")
    for s in shifts:
        print(
            f"{s['weekday']} {s['day']}: "
            f"{s['start']} - {s['end']} (pause {s['pause_min']} min) → {s['hours']} timer"
        )

    print("\n⏱️ Total arbejdstid i perioden:", total, "timer")

if __name__ == "__main__":
    main()
