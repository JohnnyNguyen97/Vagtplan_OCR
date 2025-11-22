import re
from datetime import datetime, timedelta
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



IMAGE_PATH = r"C:\Users\Johnny\Desktop\Vagter\45.png"  #Path til screenshot af vagtplan

def extract_text(path):
    img = Image.open(path)
    
    text = pytesseract.image_to_string(img, lang="dan+eng")
    return text

def parse_shifts(text):
    import re

    # Rens OCR-tekst for mærkelige tegn
    text = text.replace("‘", "").replace("’", "").replace("`", "")

    # Matcher dage 
    day_pattern = r"(?i)\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Man|Tir|Ons|Tor|Fre|L[oø]r|S[oø]n|Mandag|Tirsdag|Onsdag|Torsdag|Fredag|L[øo]rdag|S[øo]ndag)\b\s*(\d{1,2})?"

    # Matcher tider og pause
    time_pattern = r"(\d{1,2}:\d{2})\s*[-–]\s*(\d{1,2}:\d{2})(?:\s*\(?([0-9]{1,3})\)?)?"
    
    # Eksempel: "08:00 - 16:00 (30)"
    shifts = []

    # Find alle dage og tider med positionsdata
    day_matches = list(re.finditer(day_pattern, text))
    time_matches = list(re.finditer(time_pattern, text))

    # Udvid dag_matches med .start() så vi kan relatere vagter til dagslinjer
    day_positions = [
        {
            "weekday": d.group(1),
            "day": int(d.group(2)) if d.group(2) else None,
            "pos": d.start()
        }
        for d in day_matches
    ]

    # Finder vagter og relaterer til dage
    for t in time_matches:
        t_pos = t.start()

        # Find dag hvor dag.pos < t.pos, og som er nærmest
        used_day = None
        for d in day_positions:
            if d["pos"] < t_pos:
                used_day = d
            else:
                break

        # Hvis vi af en eller anden grund ikke finder dag så skip denne vagt
        if not used_day:
            continue

        start = t.group(1)
        end = t.group(2)
        pause = int(t.group(3)) if (t.group(3) and t.group(3).isdigit()) else 0

        shifts.append({
            "weekday": used_day["weekday"],
            "day": used_day["day"],
            "start": start,
            "end": end,
            "pause_min": pause
        })

    return shifts




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

def main():
    print("Læser billede...")
    text = extract_text(IMAGE_PATH)

    print("\n OCR indhold:")
    print("--------------------------------")
    print(text)
    print("--------------------------------")

    shifts = parse_shifts(text)
    # Beregn timer før vi forsøger at udskrive dem
    total = calculate_hours(shifts)

    print("Udtræk af vagter:")
    if not shifts:
        print("Ingen vagter fundet i OCR-teksten. Prøv 'lang' parameter eller tjek billedet.")
    for s in shifts:
        print(
            f"\n {s['start']} - {s['end']} (pause {s['pause_min']} min) → {s['hours']} timer"
        )

    print("\n Total arbejdstid i perioden:", total, "timer\n")

if __name__ == "__main__":
    main()
