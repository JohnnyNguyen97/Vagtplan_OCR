import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from shift_parser import parse_shifts
from hour_calc import calculate_hours
from salary import calculate_salary_detailed
from ocr_reader import extract_text
from data_storage import save_shifts
import config


def get_data(image_path):
    try:
        text = extract_text(image_path, config.TESSERACT_PATH)
    except Exception:
        text = ""
    shifts = parse_shifts(text)
    total = calculate_hours(shifts)
    salary_data = calculate_salary_detailed(shifts, config.HOURLY_WAGE)
    return shifts, salary_data


class ShiftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vagtoversigt")
        self.geometry("700x400")
        
        self.image_path = r"C:\Users\Johnny\Desktop\Vagter\48.png"  # Default path
        self.current_shifts = []
        self.current_salary_data = {}

        # Top frame for file selection
        top_frame = ttk.Frame(self)
        top_frame.pack(fill='x', padx=8, pady=8)

        ttk.Label(top_frame, text="Billede:").pack(side='left', padx=(0, 5))
        self.path_label = ttk.Label(top_frame, text=self.image_path, foreground='blue')
        self.path_label.pack(side='left', fill='x', expand=True, padx=(0, 5))

        browse_btn = ttk.Button(top_frame, text="Vælg billede", command=self.browse_file)
        browse_btn.pack(side='left', padx=4)

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

        # Create a frame for salary details
        salary_frame = ttk.LabelFrame(bottom, text="Løn detaljer", padding=5)
        salary_frame.pack(fill='x', pady=(0, 8))

        self.details_text = tk.Text(salary_frame, height=8, width=60, font=('Courier', 9))
        self.details_text.pack(fill='x')
        self.details_text.config(state='disabled')

        btn_frame = ttk.Frame(bottom)
        btn_frame.pack(side='right')

        refresh_btn = ttk.Button(btn_frame, text="Opdater", command=self.update)
        refresh_btn.pack(side='left', padx=4)

        save_btn = ttk.Button(btn_frame, text="Gem til Historie", command=self.save_to_history)
        save_btn.pack(side='left', padx=4)

        open_main_btn = ttk.Button(btn_frame, text="Åbn i Terminal", command=self.open_main)
        open_main_btn.pack(side='left', padx=4)

        close_btn = ttk.Button(btn_frame, text="Luk", command=self.destroy)
        close_btn.pack(side='left', padx=4)

        self.update()

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Vælg vagtplan screenshot",
            filetypes=[("PNG billeder", "*.png"), ("JPEG billeder", "*.jpg *.jpeg"), ("Alle filer", "*.*")]
        )
        if file_path:
            self.image_path = file_path
            self.path_label.config(text=file_path)
            self.update()

    def update(self):
        try:
            shifts, salary_data = get_data(self.image_path)
        except Exception as e:
            messagebox.showerror("Fejl", f"Kunne ikke hente data: {e}")
            shifts, salary_data = [], {
                "total_hours": 0, "gross_pay": 0, "am_bidrag": 0, 
                "a_skat": 0, "atp": 0, "forsikring": 0, "total_taxes": 0, "net_pay": 0
            }

        # Store current data
        self.current_shifts = shifts
        self.current_salary_data = salary_data

        for i in self.tree.get_children():
            self.tree.delete(i)

        for s in shifts:
            self.tree.insert('', 'end', values=(s.get('weekday',''), s.get('start',''), s.get('end',''), s.get('pause_min',0), f"{s.get('hours',0):.2f}"))

        # Display salary details
        details = f"""
Timer og løn oversigt:
─────────────────────────────────────
Arbejdstimer:             {salary_data['total_hours']:>6.2f} timer

Bruttoløn:                {salary_data['gross_pay']:>10.2f} kr
─────────────────────────────────────
Skatter og bidrag:
  AM-bidrag (8%):         {salary_data['am_bidrag']:>10.2f} kr
  A-skat (39%):            {salary_data['a_skat']:>10.2f} kr
  ATP-pension:            {salary_data['atp']:>10.2f} kr
  Forsikring:             {salary_data['forsikring']:>10.2f} kr
─────────────────────────────────────
I alt skat og bidrag:     {salary_data['total_taxes']:>10.2f} kr
═════════════════════════════════════
UDBETALING:               {salary_data['net_pay']:>10.2f} kr
"""
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', details)
        self.details_text.config(state='disabled')


    def save_to_history(self):
        if not self.current_shifts:
            messagebox.showwarning("Advarsel", "Ingen vagter at gemme. Opdater først med et billede.")
            return
        
        try:
            entry_count = save_shifts(self.current_shifts, self.current_salary_data)
            messagebox.showinfo("Succes", f"Vagter gemt til historie! (Total indlæg: {entry_count})")
        except Exception as e:
            messagebox.showerror("Fejl", f"Kunne ikke gemme til historie: {e}")

    def open_main(self):
        import subprocess
        subprocess.Popen(['powershell', '-NoExit', '-Command', 'python main.py'], cwd='.')


if __name__ == '__main__':
    app = ShiftApp()
    app.mainloop()
