import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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
            global df, mesi_disponibili
            df = pd.read_excel(file_path, skiprows=5)
            new_columns = ['Date', 'Income', 'Expenses', 'Description', 'Full_Description', 'Status']
            df = df[1:]  # Skip the duplicated header row
            df.columns = new_columns

            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
            df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')

            df['Month'] = df['Date'].dt.to_period('M').astype(str)

            mesi_disponibili = sorted(df['Month'].dropna().unique())

            # Rimuoviamo vecchi bottoni (se esistono)
            for widget in mesi_frame.winfo_children():
                widget.destroy()

            # Creiamo bottoni cliccabili per ogni mese
            for mese in mesi_disponibili:
                anno, num_mese = mese.split('-')
                nome_mese = f"{mesi_italiani[num_mese]} {anno}"
                btn = ttk.Button(mesi_frame, text=nome_mese, command=lambda m=mese: calculate(m))
                btn.pack(pady=2, fill='x')

            messagebox.showinfo("File Caricato", "File Excel caricato correttamente.")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore durante il caricamento del file: {e}")

# Funzione per eseguire i calcoli
def calculate(selected_month):
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

    num_mese = selected_month[5:7]
    anno = selected_month[0:4]

    # Puliamo il frame risultati
    for widget in results_frame.winfo_children():
        widget.destroy()

    # Font professionale
    font_titolo = ("Arial", 14, "bold")
    font_testo = ("Arial", 12)

    # Titolo
    titolo = tk.Label(results_frame, text=f"Risultati per {mesi_italiani[num_mese]} {anno}", font=font_titolo)
    titolo.pack(pady=5)

    # Entrate
    entrate_label = tk.Label(results_frame, text=f"Totale Entrate: {abs(total_income):.2f} €", fg="green", font=font_testo)
    entrate_label.pack(pady=2)

    # Uscite
    uscite_label = tk.Label(results_frame, text=f"Totale Uscite: {abs(total_expenses):.2f} €", fg="red", font=font_testo)
    uscite_label.pack(pady=2)

    # Spese carta di credito in fucsia
    carta_label = tk.Label(results_frame, text=f"Spese carta di credito: {abs(total_credit_card_expenses):.2f} €", fg="magenta", font=font_testo)
    carta_label.pack(pady=2)

    # Trasferimenti investimenti
    investimenti_label = tk.Label(results_frame, text=f"Trasferimenti per investimenti: {abs(total_transfer_investments):.2f} €", fg="blue", font=font_testo)
    investimenti_label.pack(pady=2)

# Creazione GUI
root = tk.Tk()
root.title("Analizzatore Movimenti Mensili")

# Pulsante caricamento file
load_button = ttk.Button(root, text="Carica file Excel", command=carica_file)
load_button.pack(pady=5)

# Label selezione mese
ttk.Label(root, text="Seleziona un mese:").pack(pady=5)

# Frame mesi disponibili
mesi_frame = ttk.Frame(root)
mesi_frame.pack(pady=5)

# Separatore
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', pady=10)

# Frame risultati, con bordo
results_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
results_frame.pack(pady=10, fill='both', expand=True)

root.mainloop()
