import pandas as pd
import glob
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

# Dizionario mesi in italiano
mesi_italiani = {
    "01": "Gennaio",
    "02": "Febbraio",
    "03": "Marzo",
    "04": "Aprile",
    "05": "Maggio",
    "06": "Giugno",
    "07": "Luglio",
    "08": "Agosto",
    "09": "Settembre",
    "10": "Ottobre",
    "11": "Novembre",
    "12": "Dicembre"
}


# Funzione per caricare il file Excel selezionato
def carica_file():
    file_path = filedialog.askopenfilename(
        title="Seleziona il file Excel",
        filetypes=[("File Excel", "*.xlsx")]
    )
    if file_path:
        try:
            global df
            df = pd.read_excel(file_path, skiprows=5)
            new_columns = ['Date', 'Income', 'Expenses', 'Description', 'Full_Description', 'Status']
            df = df[1:]  # Skip the duplicated header row
            df.columns = new_columns

            # Converti le colonne nei tipi di dati appropriati
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
            df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')

            # Crea una colonna con il mese nel formato 'YYYY-MM'
            df['Month'] = df['Date'].dt.to_period('M').astype(str)
            available_months = df['Month'].dropna().unique()

            # Aggiorna il combobox con i mesi disponibili
            month_cb['values'] = sorted(available_months)
            messagebox.showinfo("File Caricato", "File Excel caricato correttamente.")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante il caricamento del file: {e}")

# Funzione per eseguire i calcoli e aggiornare i risultati
def calculate():
    selected_month = month_var.get()
    if not selected_month:
        messagebox.showwarning("Selection Error", "Per favore seleziona un mese.")
        return

    df_month = df[df['Month'] == selected_month]

    df_transfer_investments = df_month[df_month['Full_Description'].str.contains('Trasferimento Scalable', na=False)]
    total_transfer_investments = df_transfer_investments['Expenses'].sum(skipna=True)

    df_month_filtered = df_month[
        ~df_month['Description'].str.contains('Ricarica carta ricaricabile', na=False) &
        ~df_month['Description'].str.contains('Utilizzo carta di credito', na=False) &
        ~df_month['Full_Description'].str.contains('Trasferimento Scalable', na=False)
    ]

    total_income = df_month_filtered['Income'].sum(skipna=True)
    total_expenses = df_month_filtered['Expenses'].sum(skipna=True)

    df_credit_card = df_month[df_month['Description'].str.contains(r'5100 \*\*\*\* \*\*\*\* 8057', na=False)]
    total_credit_card_expenses = df_credit_card['Expenses'].sum(skipna=True)

    result_text.set(
        f"Risultati per {mesi_italiani[selected_month[5:7]]}:\n"
        f"Totale Entrate: {abs(total_income):.2f} €\n"
        f"Totale Uscite: {abs(total_expenses):.2f} €\n"
        f"Spese carta di credito: {abs(total_credit_card_expenses):.2f} €\n"
        f"Trasferimenti per investimenti: {abs(total_transfer_investments):.2f} €"
    )

# Creazione della GUI
root = tk.Tk()
root.title("Analizzatore Movimenti Mensili")

month_var = tk.StringVar()
result_text = tk.StringVar()

ttk.Label(root, text="Seleziona un mese:").pack(pady=5)
month_cb = ttk.Combobox(root, textvariable=month_var)
month_cb.pack(pady=5)

# Pulsante per caricare il file Excel
load_button = ttk.Button(root, text="Carica file Excel", command=carica_file)
load_button.pack(pady=5)

calc_btn = ttk.Button(root, text="Calcola", command=calculate)
calc_btn.pack(pady=5)

result_label = ttk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

root.mainloop()
