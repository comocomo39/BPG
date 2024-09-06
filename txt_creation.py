import random
import os

# Dati finti per generare i documenti
nomi = [
    "MARIO ROSSI", "LUIGI BIANCHI", "ANNA VERDI", "MATTEO COMINI", "PASQUALE CROCCO"
]
aziende = [
    "Tech Solutions S.p.A.", "Smart Devices S.r.l.", "Innovative Software Ltd.",
    "Green Energy Co.", "Digital Services Inc.", "BlueTech Enterprises"
]
prodotti = [
    "Laptop", "Smartphone", "Tablet", "Monitor", "Stampante", "Cuffie", "Router", "Televisore"
]
job_positions = [
    "Sviluppatore Software", "Analista Dati", "Manager di Progetto", "Contabile", "Marketing Specialist"
]
quantita_max = 10
importo_min = 100
importo_max = 2000

# Crea una cartella per salvare i documenti, se non esiste già
os.makedirs("documenti_generati", exist_ok=True)


# Funzione per generare un contratto di lavoro
def genera_contratto_lavoro(customer_id):
    nome = random.choice(nomi)
    azienda = random.choice(aziende)
    posizione = random.choice(job_positions)
    stipendio_annuale = random.randint(25000, 60000)

    contenuto_contratto = f"""
    CONTRATTO DI LAVORO

    L'azienda {azienda} assume {nome} per la posizione di {posizione}.
    Stipendio annuale: €{stipendio_annuale}

    Inizio del contratto: 01/10/2024
    Termini del contratto: il contratto è valido per un periodo di 12 mesi.

    Firma del dipendente: ____________________
    Firma del datore di lavoro: ____________________

    Grazie per aver scelto {azienda}.
    """

    # Salva il contratto in un file .txt
    nome_file = f"contratto_lavoro_{customer_id}.txt"
    with open(f"documenti_generati/{nome_file}", "w") as file:
        file.write(contenuto_contratto)


# Funzione per generare una ricevuta di pagamento
def genera_ricevuta_pagamento(customer_id):
    nome = random.choice(nomi)
    azienda = random.choice(aziende)
    importo = round(random.uniform(importo_min, importo_max), 2)
    data_pagamento = f"{random.randint(1, 28)}/09/2024"

    contenuto_ricevuta = f"""
    RICEVUTA DI PAGAMENTO

    Nome: {nome}
    Azienda: {azienda}
    Data del pagamento: {data_pagamento}
    Importo pagato: €{importo}

    Metodo di pagamento: Carta di Credito

    Grazie per il tuo pagamento!
    """

    # Salva la ricevuta in un file .txt
    nome_file = f"ricevuta_pagamento_{customer_id}.txt"
    with open(f"documenti_generati/{nome_file}", "w") as file:
        file.write(contenuto_ricevuta)


# Funzione per generare un preventivo
def genera_preventivo(customer_id):
    nome = random.choice(nomi)
    azienda = random.choice(aziende)
    prodotto = random.choice(prodotti)
    quantita = random.randint(1, quantita_max)
    prezzo_unitario = round(random.uniform(importo_min, importo_max), 2)
    totale = round(quantita * prezzo_unitario, 2)

    contenuto_preventivo = f"""
    PREVENTIVO

    Cliente: {nome}
    Azienda: {azienda}

    Prodotto: {prodotto}
    Quantità: {quantita}
    Prezzo unitario: €{prezzo_unitario}
    Totale: €{totale}

    Validità del preventivo: 30 giorni

    Grazie per aver richiesto un preventivo a {azienda}.
    """

    # Salva il preventivo in un file .txt
    nome_file = f"preventivo_{customer_id}.txt"
    with open(f"documenti_generati/{nome_file}", "w") as file:
        file.write(contenuto_preventivo)


# Genera una serie di documenti
def genera_documenti():
    num_documenti = 10  # Numero di documenti di ogni tipo

    for i in range(1, num_documenti + 1):
        genera_contratto_lavoro(i)
        genera_ricevuta_pagamento(i)
        genera_preventivo(i)

    print(f"Generati {num_documenti * 3} documenti nella cartella 'documenti_generati'.")


# Eseguire la generazione dei documenti
genera_documenti()
