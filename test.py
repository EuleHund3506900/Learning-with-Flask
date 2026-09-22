import tkinter as tk
from tkinter import filedialog, messagebox
import json
import logging

logging.basicConfig(filename="logs/gui.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataFormatError(Exception):
    pass

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
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

def main():
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("JSON-Dateien", "*.json")])
        if file_path:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, file_path)

    def load_and_display():
        file_path = entry_file.get()
        try:
            data = load_data(file_path)
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Daten erfolgreich geladen:\n{json.dumps(data, indent=2)}")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, f"Fehler: {str(e)}")

    root = tk.Tk()
    root.title("Daten laden")
    tk.Label(root, text="JSON-Datei:").grid(row=0, column=0, padx=5, pady=5)
    entry_file = tk.Entry(root, width=50)
    entry_file.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Durchsuchen", command=select_file).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(root, text="Laden", command=load_and_display).grid(row=1, column=0, columnspan=3, pady=10)
    text_result = tk.Text(root, height=10, width=60)
    text_result.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
    root.mainloop()

if __name__ == "__main__":
    logging.info("Starte GUI-Datenladen")
    main()
    logging.info("GUI-Datenladen abgeschlossen")