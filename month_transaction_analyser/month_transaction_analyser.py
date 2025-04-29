import pandas as pd
import os

def analizza_transazioni(df):
    """
    Analizza le transazioni finanziarie di un dato mese.

    Args:
        df (pd.DataFrame): DataFrame contenente i dati delle transazioni
                           con le colonne 'Data', 'Entrate', 'Uscite', 'Descrizione', 'Descrizione_Completa'.

    Returns:
        tuple: Un tuple contenente:
                   - float: Somma delle entrate del mese.
                   - float: Somma delle spese del mese dopo le modifiche.
                   - float: Somma delle spese con carta di credito da accreditare.
                   - pd.DataFrame: DataFrame filtrato per il mese e con le modifiche applicate.
    """
    mese_da_elaborare = input("Inserisci il mese che vuoi elaborare (formato MM/AAAA): ")

    # Converti la colonna 'Data' in formato datetime
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

    # Filtra il DataFrame per il mese selezionato
    df_mese = df[df['Data'].dt.strftime('%m/%Y') == mese_da_elaborare].copy()

    # Calcola la somma delle entrate
    somma_entrate = df_mese['Entrate'].fillna(0).sum()

    # Inizializza le variabili per le spese
    spese_totali = df_mese['Uscite'].fillna(0).copy()
    spese_carta_credito = 0

    # Applica le modifiche alle uscite
    for index, row in df_mese.iterrows():
        descrizione = row['Descrizione']
        descrizione_completa = row['Descrizione_Completa']
        uscita = row['Uscite']

        if pd.notna(uscita):
            if "Wind Tre" in descrizione:  # Modifica basata sulla colonna 'Descrizione'
                spese_totali.at[index] = -10
            elif "Scalable" in descrizione_completa:  # Eliminazione basata su 'Descrizione_Completa'
                spese_totali.at[index] = 0
            elif "Ricarica carta ricaricabile" in descrizione:  # Eliminazione basata su 'Descrizione'
                spese_totali.at[index] = 0
            elif "MONOFUNZIONE CONTACTLESS CHIP 5100 **** **** 8057" in descrizione:  # Conteggio speciale basato su 'Descrizione_Completa'
                spese_carta_credito += abs(uscita)
                pass # Manteniamo l'uscita nel totale generale

    # Rimuovi le righe con spese azzerate
    df_mese = df_mese[spese_totali != 0].copy()

    # Calcola la somma totale delle spese dopo le modifiche
    somma_spese = df_mese['Uscite'].fillna(0).sum()

    return somma_entrate, somma_spese, spese_carta_credito, df_mese

# --- Esempio di utilizzo ---
# Assicurati di avere la libreria pandas installata: pip install pandas
excel_file = None
for filename in os.listdir():
    if "movements_" in filename:
        excel_file = filename
        break

if excel_file:
    df = pd.read_excel(excel_file)
    entrate, spese, carta_credito, df_filtrato = analizza_transazioni(df)

    print(f"Somma delle entrate del mese: {entrate:.2f} €")
    print(f"Somma delle spese del mese (dopo modifiche): {spese:.2f} €")
    print(f"Spese con carta di credito da accreditare il 10 del mese successivo: {carta_credito:.2f} €")

    # Salva il DataFrame filtrato in un nuovo file Excel
    df_filtrato.to_excel("transazioni_filtrate.xlsx", index=False)
    print("Il file 'transazioni_filtrate.xlsx' è stato generato.")
else:
    print("Nessun file Excel con 'movements_' nel nome trovato nella cartella corrente.")