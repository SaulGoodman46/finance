import pandas as pd
import glob
import os

# Find the first Excel file starting with 'movements' in the current directory
files = glob.glob('movements*.xlsx')
if not files:
    print("No Excel file starting with 'movements' found in the current directory.")
    exit()

file_path = files[0]
print(f"Opening file: {file_path}")

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

# Show available months
available_months = df['Month'].dropna().unique()
print("Available months:")
for i, month in enumerate(available_months):
    print(f"{i+1}. {month}")

# Ask user to select a month
choice = int(input("Select the number of the month you want to analyze: "))
selected_month = available_months[choice - 1]

# Filter data for the selected month
df_month = df[df['Month'] == selected_month]

# Sum transfer to investments
df_transfer_investments = df_month[df_month['Full_Description'].str.contains('Trasferimento Scalable', na=False)]
total_transfer_investments = df_transfer_investments['Expenses'].sum(skipna=True)

# Exclude expenses with specific descriptions
df_month_filtered = df_month[
    ~df_month['Description'].str.contains('Ricarica carta ricaricabile', na=False) &
    ~df_month['Description'].str.contains('Utilizzo carta di credito', na=False) &
    ~df_month['Full_Description'].str.contains('Trasferimento Scalable', na=False)
]

# Calculate sums
total_income = df_month_filtered['Income'].sum(skipna=True)
total_expenses = df_month_filtered['Expenses'].sum(skipna=True)

# Sum credit card expenses
df_credit_card = df_month[df_month['Description'].str.contains('5100 \*\*\*\* \*\*\*\* 8057', na=False)]
total_credit_card_expenses = df_credit_card['Expenses'].sum(skipna=True)

print(f"\nResults for {selected_month}:")
print(f"Total Income: {abs(total_income):.2f} €")
print(f"Total Expenses: {abs(total_expenses):.2f} €")
print(f"Spese carta di credito: {abs(total_credit_card_expenses):.2f} €")
print(f"Trasferimenti per investimenti: {abs(total_transfer_investments):.2f} €")
