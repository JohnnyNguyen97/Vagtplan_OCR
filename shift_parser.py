import re

def parse_shifts(text):
    

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