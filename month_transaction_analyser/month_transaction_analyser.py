import pandas as pd
import glob
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Dizionario per tradurre i mesi in italiano
mesi_italiani = {
    '01': 'Gennaio', '02': 'Febbraio', '03': 'Marzo', '04': 'Aprile', 
    '05': 'Maggio', '06': 'Giugno', '07': 'Luglio', '08': 'Agosto', 
    '09': 'Settembre', '10': 'Ottobre', '11': 'Novembre', '12': 'Dicembre'
}

# Funzione per eseguire i calcoli e aggiornare i risultati
def calculate():
    selected_month = month_var.get()
    if not selected_month:
        messagebox.showwarning("Errore nella selezione", "Per favore, seleziona un mese.")
        return
    
    # Verifica che il formato selected_month sia corretto (YYYY-MM)
    if len(selected_month) != 7:
        messagebox.showwarning("Errore nel formato del mese", "Formato mese non valido.")
        return
    
    # Estrai il mese in formato 'MM' per mappare con il dizionario
    month_code = selected_month[5:7]
    
    # Verifica se il codice del mese è valido
    if month_code not in mesi_italiani:
        messagebox.showwarning("Errore", "Mese selezionato non valido.")
        return

    # Filtra i dati per il mese selezionato
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

    df_credit_card = df_month[df_month['Description'].str.contains('5100 \*\*\*\* \*\*\*\* 8057', na=False)]
    total_credit_card_expenses = df_credit_card['Expenses'].sum(skipna=True)

    result_text.set(
        f"Risultati per {mesi_italiani[month_code]}:\n"
        f"Entrate totali: {abs(total_income):.2f} €\n"
        f"Spese totali: {abs(total_expenses):.2f} €\n"
        f"Spese carta di credito: {abs(total_credit_card_expenses):.2f} €\n"
        f"Trasferimenti per investimenti: {abs(total_transfer_investments):.2f} €"
    )

# Trova il primo file Excel che inizia con 'movements' nella directory corrente
files = glob.glob('movements*.xlsx')
if not files:
    print("Nessun file Excel che inizia con 'movements' trovato nella directory corrente.")
    exit()

file_path = files[0]

# Carica il file Excel
df = pd.read_excel(file_path, skiprows=5)

# Pulizia degli header
new_columns = ['Date', 'Income', 'Expenses', 'Description', 'Full_Description', 'Status']
df = df[1:]  # Salta la riga dell'header duplicato
df.columns = new_columns

# Conversione delle colonne nei tipi di dati appropriati
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')

# Crea una colonna con il mese nel formato 'YYYY-MM'
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Traduci i mesi in italiano
available_months = [f"{year}-{month}" for year, month in [x.split('-') for x in df['Month'].dropna().unique()]]

# Crea la GUI
root = tk.Tk()
root.title("Analizzatore Movimenti Mensili")

month_var = tk.StringVar()
result_text = tk.StringVar()

ttk.Label(root, text="Seleziona un mese:").pack(pady=5)
month_cb = ttk.Combobox(root, textvariable=month_var, values=sorted(available_months))
month_cb.pack(pady=5)

calc_btn = ttk.Button(root, text="Calcola", command=calculate)
calc_btn.pack(pady=5)

result_label = ttk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

root.mainloop()
