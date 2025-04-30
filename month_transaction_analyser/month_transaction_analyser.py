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

# Calculate sums
total_income = df_month['Income'].sum(skipna=True)
total_expenses = df_month['Expenses'].sum(skipna=True)

print(f"\nResults for {selected_month}:")
print(f"Total Income: {total_income:.2f} €")
print(f"Total Expenses: {total_expenses:.2f} €")