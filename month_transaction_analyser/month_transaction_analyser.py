import pandas as pd
import os

def analizza_transazioni(df, mese_selezionato):
    """
    Analizza le transazioni finanziarie per il mese selezionato.

    Args:
        df (pd.DataFrame): DataFrame contenente i dati delle transazioni.
        mese_selezionato (str): Mese da elaborare nel formato 'MM/AAAA'.

    Returns:
        tuple: Un tuple contenente:
                   - float: Somma delle entrate del mese.
                   - float: Somma delle spese del mese dopo le modifiche.
                   - float: Somma delle spese con carta di credito da accreditare.
                   - pd.DataFrame: DataFrame filtrato per il mese e con le modifiche applicate.
    """
    # Filtra il DataFrame per il mese selezionato
    df_mese = df[df['Data'].dt.strftime('%m/%Y') == mese_selezionato].copy()

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
            if "Wind Tre" in descrizione:
                spese_totali.at[index] = -10
            elif "Scalable" in descrizione_completa:
                spese_totali.at[index] = 0
            elif "Ricarica carta ricaricabile" in descrizione:
                spese_totali.at[index] = 0
            elif "MONOFUNZIONE CONTACTLESS CHIP 5100 **** **** 8057" in descrizione_completa:
                spese_carta_credito += abs(uscita)
                pass

    # Rimuovi le righe con spese azzerate
    df_mese = df_mese[spese_totali != 0].copy()

    # Calcola la somma totale delle spese dopo le modifiche
    somma_spese = df_mese['Uscite'].fillna(0).sum()

    return somma_entrate, somma_spese, spese_carta_credito, df_mese

# --- Esempio di utilizzo ---
excel_file = None
for filename in os.listdir():
    if "movements_" in filename:
        excel_file = filename
        break

if excel_file:
    df = pd.read_excel(excel_file)

    # Converti la colonna 'Data' in formato datetime (se non lo è già)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    df.dropna(subset=['Data'], inplace=True) # Rimuovi eventuali date non valide

    # Trova gli ultimi due anni presenti nei dati
    anni_presenti = sorted(df['Data'].dt.year.unique(), reverse=True)[:2]
    mesi_disponibili = []
    for anno in anni_presenti:
        mesi_anno = sorted(df[df['Data'].dt.year == anno]['Data'].dt.strftime('%m').unique())
        for mese in mesi_anno:
            mesi_disponibili.append(f"{mese}/{anno}")

    # Chiedi all'utente di scegliere tra i mesi disponibili
    print("Seleziona il mese che vuoi elaborare:")
    for i, mese in enumerate(mesi_disponibili):
        print(f"{i + 1}. {mese}")

    while True:
        try:
            scelta = int(input("Inserisci il numero corrispondente al mese: "))
            if 1 <= scelta <= len(mesi_disponibili):
                mese_selezionato = mesi_disponibili[scelta - 1]
                break
            else:
                print("Scelta non valida. Inserisci un numero dalla lista.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    entrate, spese, carta_credito, df_filtrato = analizza_transazioni(df.copy(), mese_selezionato)

    print(f"\nSomma delle entrate del mese di {mese_selezionato}: {entrate:.2f} €")
    print(f"Somma delle spese del mese di {mese_selezionato} (dopo modifiche): {spese:.2f} €")
    print(f"Spese con carta di credito da accreditare il 10 del mese successivo: {carta_credito:.2f} €")

    # Salva il DataFrame filtrato in un nuovo file Excel
    df_filtrato.to_excel(f"transazioni_filtrate_{mese_selezionato.replace('/', '_')}.xlsx", index=False)
    print(f"Il file 'transazioni_filtrate_{mese_selezionato.replace('/', '_')}.xlsx' è stato generato.")

else:
    print("Nessun file Excel con 'movements_' nel nome trovato nella cartella corrente.")