import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import json
import logging
from datetime import datetime

logging.basicConfig(filename="logs/gui.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataFormatError(Exception):
    pass

def load_data(file_path: str):
    try:
        with open(file_path, 'r') as f:
            if(file_path.find('.log') != -1):
                lines = f.readlines()
                data = []
                for line in lines:
                    data.append(f'{"{"}"timestamp": "{line.split(" - ")[0]}","level": "{line.split(" - ")[1]}","message": "{line.replace(line.split(" - ")[0], "").replace(line.split(" - ")[1], "").replace(" - ", "")}"{"}"}')
                    logging.info(f"Daten geladen: {file_path}")
                    return data

            data = json.load(f)
            if not isinstance(data, list):
                raise DataFormatError("Daten müssen eine Liste sein.")
            logging.info(f"Daten geladen: {file_path}")
            return data
    except FileNotFoundError:
        logging.error(f"Datei {file_path} nicht gefunden.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Ungültiges JSON-Format in {file_path}.")
        raise
    except DataFormatError as e:
        logging.error(f"Formatfehler: {e}")
        raise

def count_events(data, event_type=None):
    try:
        if event_type:
            return sum(1 for entry in data if entry["event"] == event_type)
        return len(data)
    except KeyError:
        logging.error("Ungültiges Datenformat (fehlender 'event'-Schlüssel).")
        raise

def get_user_events(data, user_id):
    try:
        if not isinstance(user_id, int):
            raise ValueError("User ID muss eine Ganzzahl sein.")
        return [entry["event"] for entry in data if entry["user_id"] == user_id]
    except KeyError:
        logging.error("Ungültiges Datenformat (fehlender 'user_id'-Schlüssel).")
        raise
    except ValueError as e:
        logging.error(f"Eingabefehler: {e}")
        raise

def generate_markdown_report(data, output_file):
    try:
        total_events = count_events(data)
        error_count = count_events(data, "ERROR")
        user_ids = set(entry["user_id"] for entry in data)
        user_event_summary = {uid: get_user_events(data, uid) for uid in user_ids}

        with open(output_file, "w") as f:
            f.write("# Datenanalyse-Bericht\n")
            f.write(f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Analyseergebnisse\n")
            f.write("| Metrik | Wert |\n")
            f.write("|--------|------|\n")
            f.write(f"| Gesamtereignisse | {total_events} |\n")
            f.write(f"| Fehlerereignisse | {error_count} |\n")
            f.write("\n## Ereignisse pro Benutzer\n")
            f.write("| User ID | Ereignisse |\n")
            f.write("|---------|------------|\n")
            for uid, events in user_event_summary.items():
                f.write(f"| {uid} | {', '.join(events)} |\n")

        logging.info(f"Markdown-Bericht erstellt: {output_file}")
        return output_file
    except Exception as e:
        logging.error(f"Fehler beim Erstellen des Berichts: {e}")
        raise

def main():
    data = None

    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("JSON-Dateien", "*.json"), ("LOG-Dateien", "*.log")])
        if file_path:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, file_path)

    def load_and_display():
        nonlocal data
        file_path = entry_file.get()
        try:
            progress["value"] = 0
            root.update()
            data = load_data(file_path)
            progress["value"] = 100
            root.update()
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Daten erfolgreich geladen:\n{json.dumps(data, indent=2)}")
            messagebox.showinfo("Erfolg", "Daten geladen")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Fehler: {str(e)}")
            progress["value"] = 0

    def analyze_data():
        nonlocal data
        user_id = entry_user_id.get()
        if not data:
            messagebox.showerror("Fehler", "Bitte zuerst Daten laden")
            return
        try:
            progress["value"] = 0
            root.update()
            total_events = count_events(data)
            progress["value"] = 33
            root.update()
            error_count = count_events(data, "ERROR")
            progress["value"] = 66
            root.update()
            user_id = int(user_id) if user_id else 1
            user_events = get_user_events(data, user_id)
            progress["value"] = 100
            root.update()
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Gesamtereignisse: {total_events}\n")
            text_result.insert(tk.END, f"Fehlerereignisse: {error_count}\n")
            text_result.insert(tk.END, f"Ereignisse für User {user_id}: {user_events}")
            logging.info(f"Analyse: Gesamtereignisse={total_events}, Fehler={error_count}, User {user_id}={user_events}")
            messagebox.showinfo("Erfolg", "Analyse abgeschlossen")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Fehler: {str(e)}")
            progress["value"] = 0

    def generate_report():
        nonlocal data
        output_file = entry_output.get()
        if not output_file:
            output_file = "analysis_report.md"
        if not data:
            messagebox.showerror("Fehler", "Bitte zuerst Daten laden")
            return
        try:
            progress["value"] = 0
            root.update()
            output_file = generate_markdown_report(data, output_file)
            progress["value"] = 100
            root.update()
            with open(output_file, "r") as f:
                report_content = f.read()
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, report_content)
            messagebox.showinfo("Erfolg", f"Bericht erstellt: {output_file}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Fehler: {str(e)}")
            progress["value"] = 0

    root = tk.Tk()
    root.title("Datenanalyse")
    tk.Label(root, text="JSON-Datei:").grid(row=0, column=0, padx=5, pady=5)
    entry_file = tk.Entry(root, width=50)
    entry_file.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Durchsuchen", command=select_file).grid(row=0, column=2, padx=5, pady=5)
    tk.Label(root, text="User ID:").grid(row=1, column=0, padx=5, pady=5)
    entry_user_id = tk.Entry(root, width=10)
    entry_user_id.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    tk.Label(root, text="Ausgabedatei:").grid(row=2, column=0, padx=5, pady=5)
    entry_output = tk.Entry(root, width=50)
    entry_output.insert(0, "analysis_report.md")
    entry_output.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="Daten laden", command=load_and_display).grid(row=3, column=0, pady=5)
    tk.Button(root, text="Analysieren", command=analyze_data).grid(row=3, column=1, pady=5)
    tk.Button(root, text="Bericht erstellen", command=generate_report).grid(row=3, column=2, pady=5)
    progress = ttk.Progressbar(root, length=300, mode="determinate")
    progress.grid(row=4, column=0, columnspan=3, pady=5)
    text_result = tk.Text(root, height=10, width=60)
    text_result.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    root.mainloop()

if __name__ == "__main__":
    logging.info("Starte GUI-Hauptmenü")
    main()
    logging.info("GUI-Hauptmenü abgeschlossen")