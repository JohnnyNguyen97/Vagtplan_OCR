import tkinter as tk
from tkinter import ttk, messagebox
from shift_parser import parse_shifts
from hour_calc import calculate_hours
from salary import calculate_salary
from ocr_reader import extract_text
import config

IMAGE_PATH = r"C:\Users\Johnny\Desktop\Vagter\48.png"


def get_data():
    try:
        text = extract_text(IMAGE_PATH, config.TESSERACT_PATH)
    except Exception:
        text = ""
    shifts = parse_shifts(text)
    total = calculate_hours(shifts)
    wage = calculate_salary(shifts, config.HOURLY_WAGE)
    return shifts, total, wage


class ShiftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vagtoversigt")
        self.geometry("650x350")

        self.tree = ttk.Treeview(self, columns=("day", "start", "end", "pause", "hours"), show='headings')
        self.tree.heading('day', text='Dag')
        self.tree.heading('start', text='Start')
        self.tree.heading('end', text='Slut')
        self.tree.heading('pause', text='Pause (min)')
        self.tree.heading('hours', text='Timer')
        self.tree.column('day', width=120)
        self.tree.column('start', width=80)
        self.tree.column('end', width=80)
        self.tree.column('pause', width=100)
        self.tree.column('hours', width=80)
        self.tree.pack(fill='both', expand=True, padx=8, pady=8)

        bottom = ttk.Frame(self)
        bottom.pack(fill='x', padx=8, pady=(0,8))

        self.total_label = ttk.Label(bottom, text="Total timer: —")
        self.total_label.pack(side='left', padx=(0,12))

        self.wage_label = ttk.Label(bottom, text="Total løn: —")
        self.wage_label.pack(side='left')

        btn_frame = ttk.Frame(bottom)
        btn_frame.pack(side='right')

        refresh_btn = ttk.Button(btn_frame, text="Opdater", command=self.update)
        refresh_btn.pack(side='left', padx=4)

        open_main_btn = ttk.Button(btn_frame, text="Åbn i Terminal", command=self.open_main)
        open_main_btn.pack(side='left', padx=4)

        close_btn = ttk.Button(btn_frame, text="Luk", command=self.destroy)
        close_btn.pack(side='left', padx=4)

        self.update()

    def update(self):
        try:
            shifts, total, wage = get_data()
        except Exception as e:
            messagebox.showerror("Fejl", f"Kunne ikke hente data: {e}")
            shifts, total, wage = [], 0, 0

        for i in self.tree.get_children():
            self.tree.delete(i)

        for s in shifts:
            self.tree.insert('', 'end', values=(s.get('weekday',''), s.get('start',''), s.get('end',''), s.get('pause_min',0), f"{s.get('hours',0):.2f}"))

        self.total_label.config(text=f"Total timer: {total:.2f} timer")
        self.wage_label.config(text=f"Total løn: {wage:,.2f} kr")

    def open_main(self):
        import subprocess
        subprocess.Popen(['powershell', '-NoExit', '-Command', 'python main.py'], cwd='.')


if __name__ == '__main__':
    app = ShiftApp()
    app.mainloop()
