import os
import random
from datetime import datetime

# Dati finti per generare i documenti
nomi = [
    "MARIO ROSSI", "LUIGI BIANCHI", "ANNA VERDI", "GIOVANNI NERI", "ELISA GALLI",
    "CARLO FERRI", "MATTEO COMINI", "PASQUALE CROCCO", "PAOLO VERDE", "SARA VIOLA"
]
aziende = [
    "Tech Solutions S.p.A.", "Smart Devices S.r.l.", "Innovative Software Ltd.",
    "Green Energy Co.", "Digital Services Inc.", "BlueTech Enterprises"
]
prodotti = [
    "Laptop", "Smartphone", "Tablet", "Monitor", "Stampante", "Cuffie", "Router", "Televisore"
]
posizioni_lavorative = [
    "Sviluppatore Software", "Analista Dati", "Responsabile Marketing", "Direttore Vendite", "Amministratore"
]

quantita_max = 10
importo_min = 100
importo_max = 2000

# Crea una cartella per salvare i documenti, se non esiste già
os.makedirs("documenti_generati", exist_ok=True)


# Funzione per generare un contratto di lavoro con molti dati
def genera_contratto(customer_id):
    nome = random.choice(nomi)
    azienda = random.choice(aziende)
    posizione = random.choice(posizioni_lavorative)
    id_contratto = f"CT-{random.randint(1000, 9999)}"
    id_dipendente = f"EMP-{random.randint(1000, 9999)}"
    stipendio_annuale = random.randint(25000, 60000)
    data_inizio = datetime.now().strftime("%d/%m/%Y")
    durata_mesi = random.randint(6, 36)

    contenuto_contratto = f"""
    CONTRATTO DI LAVORO

    ID Contratto: {id_contratto}
    ID Dipendente: {id_dipendente}

    Azienda: {azienda}
    Nome: {nome}
    Posizione: {posizione}
    Stipendio annuale: €{stipendio_annuale}
    Data inizio: {data_inizio}
    Durata: {durata_mesi} mesi

    Firma del dipendente: ____________________
    Firma del datore di lavoro: ____________________
    """

    nome_file = f"contratto_{id_contratto}.txt"
    with open(f"documenti_generati/{nome_file}", "w") as file:
        file.write(contenuto_contratto)

    return nome_file, id_contratto


# Funzione per generare una fattura con dati complessi
def genera_fattura(customer_id):
    nome = random.choice(nomi)
    azienda = random.choice(aziende)
    prodotto = random.choice(prodotti)
    quantita = random.randint(1, quantita_max)
    prezzo_unitario = round(random.uniform(importo_min, importo_max), 2)
    totale = round(quantita * prezzo_unitario, 2)
    numero_fattura = f"FT-{random.randint(1000, 9999)}"
    id_cliente = f"CL-{random.randint(1000, 9999)}"
    data_emissione = datetime.now().strftime("%d/%m/%Y")

    contenuto_fattura = f"""
    FATTURA N. {numero_fattura}

    ID Cliente: {id_cliente}
    Nome Cliente: {nome}
    Azienda: {azienda}
    Data di emissione: {data_emissione}

    Prodotto: {prodotto}
    Quantità: {quantita}
    Prezzo unitario: €{prezzo_unitario}
    Totale: €{totale}

    Grazie per aver scelto {azienda}!
    """

    nome_file = f"fattura_{numero_fattura}.txt"
    with open(f"documenti_generati/{nome_file}", "w") as file:
        file.write(contenuto_fattura)

    return nome_file, numero_fattura


# Funzione per generare una ricevuta di pagamento collegata a una fattura
def genera_ricevuta_pagamento(customer_id, numero_fattura):
    nome = random.choice(nomi)
    azienda = random.choice(aziende)
    importo_pagato = round(random.uniform(importo_min, importo_max), 2)
    numero_ricevuta = f"RC-{random.randint(1000, 9999)}"
    data_pagamento = datetime.now().strftime("%d/%m/%Y")

    contenuto_ricevuta = f"""
    RICEVUTA DI PAGAMENTO N. {numero_ricevuta}

    Cliente: {nome}
    Azienda: {azienda}
    Data del pagamento: {data_pagamento}
    Importo pagato: €{importo_pagato}

    Fattura di riferimento: {numero_fattura}

    Grazie per il tuo pagamento!
    """

    nome_file = f"ricevuta_{numero_ricevuta}.txt"
    with open(f"documenti_generati/{nome_file}", "w") as file:
        file.write(contenuto_ricevuta)

    return nome_file, numero_ricevuta


# Funzione per generare tutti i documenti per un cliente
def genera_documenti_per_cliente(customer_id):
    contratto_file, id_contratto = genera_contratto(customer_id)
    fattura_file, numero_fattura = genera_fattura(customer_id)
    ricevuta_file, numero_ricevuta = genera_ricevuta_pagamento(customer_id, numero_fattura)

    print(f"Documenti generati per il cliente {customer_id}:")
    print(f"Contratto: {contratto_file} (ID Contratto: {id_contratto})")
    print(f"Fattura: {fattura_file} (Numero Fattura: {numero_fattura})")
    print(f"Ricevuta: {ricevuta_file} (Numero Ricevuta: {numero_ricevuta})")


# Genera documenti per 5 clienti come esempio
for i in range(1, 6):
    genera_documenti_per_cliente(i)
