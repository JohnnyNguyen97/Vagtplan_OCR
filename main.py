from ocr_reader import extract_text
from shift_parser import parse_shifts
from hour_calc import calculate_hours
from salary import calculate_salary
import config

IMAGE_PATH = r"C:\Users\Johnny\Desktop\Vagter\48.png"  #Path til screenshot af vagtplan



def main():
    print("Læser billede...")
    text = extract_text(IMAGE_PATH, config.TESSERACT_PATH)


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