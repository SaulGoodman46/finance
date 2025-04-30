import pandas as pd
import glob
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Function to perform calculations and update results
def calculate():
    selected_month = month_var.get()
    if not selected_month:
        messagebox.showwarning("Selection Error", "Please select a month.")
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

    df_credit_card = df_month[df_month['Description'].str.contains('5100 \*\*\*\* \*\*\*\* 8057', na=False)]
    total_credit_card_expenses = df_credit_card['Expenses'].sum(skipna=True)

    result_text.set(
        f"Results for {selected_month}:\n"
        f"Total Income: {abs(total_income):.2f} €\n"
        f"Total Expenses: {abs(total_expenses):.2f} €\n"
        f"Spese carta di credito: {abs(total_credit_card_expenses):.2f} €\n"
        f"Trasferimenti per investimenti: {abs(total_transfer_investments):.2f} €"
    )

# Find the first Excel file starting with 'movements' in the current directory
files = glob.glob('movements*.xlsx')
if not files:
    print("No Excel file starting with 'movements' found in the current directory.")
    exit()

file_path = files[0]

# Load the Excel file
df = pd.read_excel(file_path, skiprows=5)

# Clean up the headers
new_columns = ['Date', 'Income', 'Expenses', 'Description', 'Full_Description', 'Status']
df = df[1:]  # Skip the duplicated header row
df.columns = new_columns

# Convert columns to appropriate data types
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')

# Create a column with the month in 'YYYY-MM' format
df['Month'] = df['Date'].dt.to_period('M').astype(str)

available_months = df['Month'].dropna().unique()

# Create GUI
root = tk.Tk()
root.title("Monthly Movements Analyzer")

month_var = tk.StringVar()
result_text = tk.StringVar()

ttk.Label(root, text="Select a month:").pack(pady=5)
month_cb = ttk.Combobox(root, textvariable=month_var, values=sorted(available_months))
month_cb.pack(pady=5)

calc_btn = ttk.Button(root, text="Calculate", command=calculate)
calc_btn.pack(pady=5)

result_label = ttk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

root.mainloop()
