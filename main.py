import os
import shutil
import pytesseract
from PIL import Image
import google.generativeai as genai
from tkinter import Tk, filedialog, messagebox
import json
import PyPDF2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configura la tua chiave API direttamente nel codice
def read_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Leggi la chiave API dal file
API_KEY_PATH = 'API_KEY.txt'
API_KEY = read_api_key(API_KEY_PATH)

# Configurazione della libreria Google Generative AI con la chiave API
genai.configure(api_key=API_KEY)

# Configurazione del modello generativo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Creazione del modello con configurazione specifica
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


def analyze_file_with_gemini(image=None, extracted_text=None, is_image=False):
    """
    Analizza un file utilizzando il modello Gemini e restituisce le informazioni rilevanti.
    """
    prompt = f"""
    Gentile Intelligenza di Gemini,

    Ti prego di analizzare attentamente il file allegato e di identificare le seguenti informazioni:

    Testo estratto dall'immagine: {extracted_text}

    1. Identificazione del Tipo di Documento:
        - Se il file è una carta d'identità, estrai i seguenti dati:
            - Nome
            - Cognome
            - Data di nascita (se presente)
        - Se il file è una fattura, estrai i seguenti dati:
            - Numero di fattura
            - Nome dell'emittente della fattura
            - Data della fattura
            - Prezzo unitario
            - Quantita'
        - Se il file è una ricevuta, estrai i seguenti dati:
            - Numero di ricevuta
            - Nome del cliente
            - Data del pagamento
            - Importo pagato
        - Se il file è un contratto, estrai i seguenti dati:
            - ID Contratto
            - Nome del dipendente
            - Posizione lavorativa
            - Data di inizio e durata del contratto
            - Stipendio annuale
            
    2. Rinomina del File:
        - Se il file è una carta d'identità, rinomina il file nel formato: 'cid_Nome_Cognome'.
        - Se il file è una fattura, rinomina il file nel formato: 'fattura_Numero'.
        - Se il file è un contratto, rinomina il file nel formato: 'contratto_Numero'.
        - Se il file è una ricevuta, rinomina il file nel formato: 'ricevuta_Numero'.
        
    3. Struttura dei Dati Utente:
        - Restituisci le informazioni sull'utente (nome, cognome e altri dati rilevanti) in un formato JSON, che includa anche il nuovo nome del file.

    Grazie per la tua assistenza.
    """

    try:
        # Se è un'immagine, passiamo l'immagine come oggetto Image, altrimenti solo il contenuto di testo
        if is_image and image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content([prompt, extracted_text])

        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                content_text = candidate.content.parts[0].text

                try:
                    json_data = json.loads(content_text.split('```json')[1].split('```')[0])

                    if json_data:
                        # Determina il tipo di documento e aggiungilo al JSON
                        return json_data

                except json.JSONDecodeError as json_error:
                    print(f"Errore nel parsing del JSON: {json_error}")
                    return None
            else:
                print("Il candidato non contiene parti di testo.")
                return None
        else:
            print("Nessun candidato trovato nella risposta.")
            return None

    except Exception as e:
        print(f"Errore durante l'analisi con Gemini: {str(e)}")
        return None



def extract_text_from_image(file_path):
    """
    Estrae il testo da un'immagine utilizzando pytesseract.
    """
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text, img  # Ritorna sia il testo che l'immagine come oggetto PIL
    except Exception as e:
        print(f"Errore nell'estrazione del testo: {str(e)}")
        return "", None


def extract_text_from_txt(file_path):
    """
    Estrae il testo da un file .txt.
    """
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except Exception as e:
        print(f"Errore durante la lettura del file txt: {str(e)}")
        return ""



def extract_text_from_pdf(file_path):
    """
    Estrae il testo da un file PDF.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
        return text
    except Exception as e:
        print(f"Errore durante l'estrazione del testo dal PDF: {str(e)}")
        return ""


def process_file(file_path):
    """
    Gestisce l'intero processo: analisi del file, rinomina e organizzazione.
    """
    try:
        is_image = False
        if file_path.endswith('.txt'):
            extracted_text = extract_text_from_txt(file_path)
            file_content = None  # I file di testo non necessitano di essere passati come contenuto
        elif file_path.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
            file_content = None  # I file PDF non necessitano di contenuto immagine
        else:
            extracted_text, img = extract_text_from_image(file_path)
            file_content = img  # Passiamo l'immagine come oggetto PIL
            is_image = True

        # Analizza il file con il modello Gemini
        analysis_response = analyze_file_with_gemini(image=file_content, extracted_text=extracted_text, is_image=is_image)

        # Rinomina e organizza il file basato sull'analisi
        new_file_path = rename_and_organize_file(file_path, analysis_response)

        print(f"File rinominato e spostato in: {new_file_path}")
        messagebox.showinfo("Successo", f"File rinominato e spostato in: {new_file_path}")

        if analysis_response:
            analysis_response['percorso_file'] = new_file_path  # Imposta il percorso del file rinominato

        update_json_file_based_on_rename(analysis_response, new_file_path)
        return new_file_path, analysis_response

    except Exception as e:
        print(f"Errore durante l'elaborazione del file: {str(e)}")
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")

def extract_name_and_surname(full_name):
    # Prova a dividere il nome completo se è presente
    if full_name:
        parts = full_name.split()
        if len(parts) == 2:
            return parts[0], parts[1]  # nome, cognome
    return full_name, None

def update_json_file_based_on_rename(analysis_data, new_file_name):
    # Determina il file JSON in base alla rinominazione
    if "fattura" in new_file_name:
        json_file = 'fatture.json'
    elif "ricevuta" in new_file_name:
        json_file = 'ricevute.json'
    elif "contratto" in new_file_name:
        json_file = 'contratti.json'
    else:
        json_file = 'altri_documenti.json'

    # Verifica se il file JSON esiste già
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Imposta il numero di protocollo (incrementa rispetto al massimo esistente)
    if data:
        max_protocollo = max([doc.get('protocollo', 0) for doc in data])
    else:
        max_protocollo = 0

    # Aggiungi il numero di protocollo al nuovo documento
    analysis_data['protocollo'] = max_protocollo + 1


    # Aggiungi i nuovi dati al JSON esistente
    data.append(analysis_data)

    # Salva nuovamente nel file JSON
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Dati aggiornati nel file {json_file}")


def rename_and_organize_file(file_path, analysis_result):
    """
    Rinomina e organizza il file analizzato in base al risultato dell'analisi.
    """
    if analysis_result is None:
        print("Analisi del file fallita. Impossibile rinominare il file.")
        return None

    # Controllo sui dati di 'nome' e 'cognome'
    nome = analysis_result.get('nome')
    cognome = analysis_result.get('cognome')

    # Se nome è presente ma cognome è assente, proviamo a dividere il nome completo
    if nome and not cognome:
        nome, cognome = extract_name_and_surname(nome)

    if nome is None or cognome is None:
        print(f"Attenzione: Nome o cognome mancanti nell'analisi del file {file_path}.")

    new_file_name = analysis_result.get('nuovo_nome_file', 'documento_sconosciuto')
    user_info = f"{nome if nome else 'utente'}_{cognome if cognome else 'sconosciuto'}"

    user_folder = f"./documenti/{user_info}"
    os.makedirs(user_folder, exist_ok=True)

    ext = os.path.splitext(file_path)[1]
    new_file_path = os.path.join(user_folder, f"{new_file_name}{ext}")
    shutil.move(file_path, new_file_path)

    return new_file_path

#######################
#######################
#######################

from tkinter import Tk, filedialog, messagebox, ttk, StringVar
import threading
import os


# Aggiungiamo una nuova finestra con tabella e barra di progresso
def create_gui():
    root = Tk()
    root.title("Gestione Documenti")
    root.geometry("800x500")

    # Aggiungi una label per il titolo
    title_label = ttk.Label(root, text="Processamento Documenti", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Aggiungiamo la tabella per visualizzare i risultati
    columns = ("Nome File", "Stato", "Dettagli", "Nuovo Nome File")
    table = ttk.Treeview(root, columns=columns, show="headings")
    table.heading("Nome File", text="Nome File")
    table.heading("Stato", text="Stato")
    table.heading("Dettagli", text="Dettagli")
    table.heading("Nuovo Nome File", text="Nuovo Nome File")
    table.pack(expand=True, fill="both", padx=10, pady=10)

    # Aggiungiamo una barra di progresso
    progress_var = StringVar()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    progress_label = ttk.Label(root, textvariable=progress_var)
    progress_label.pack(pady=5)

    # Aggiungi un pulsante per avviare il caricamento dei file
    load_button = ttk.Button(root, text="Seleziona File",
                             command=lambda: select_file(table, progress_bar, progress_var))
    load_button.pack(pady=10)

    root.mainloop()


def process_file_with_progress(file_path, table, progress_bar, progress_var):
    progress_var.set("Elaborazione in corso...")
    progress_bar.start()

    # Aggiungi un log del file in fase di elaborazione
    print(f"Elaborazione del file: {file_path}")

    # Processa il file e ottieni l'analisi
    new_file_path, analysis_response = process_file(file_path)

    # Aggiorna la tabella con lo stato di successo e il percorso del file
    if new_file_path:
        new_file_name = os.path.basename(new_file_path)  # Prende solo il nome del file dal percorso completo
        file_dir = new_file_path
        status = "Completato"
    else:
        new_file_name = 'Analisi fallita: Nessun nome estratto'
        file_dir = "Percorso non disponibile"
        status = "Errore"

    table.insert("", "end", values=(
        os.path.basename(file_path),  # Nome file originale
        status,
        file_dir,  # Mostra il percorso completo dove il file è stato spostato
        new_file_name  # Mostra il nuovo nome del file
    ))

    progress_bar.stop()
    progress_var.set("Elaborazione completata.")

    # Stampa il percorso corretto del file rinominato
    print(f"File spostato e rinominato come: {new_file_name}")
    print(f"Percorso file: {file_dir}")


# Selezione file con gestione della UI
def select_file(table, progress_bar, progress_var):
    file_path = filedialog.askopenfilename(
        title="Seleziona un file",
        filetypes=[("Documenti", "*.png;*.jpg;*.jpeg;*.tiff;*.txt;*.pdf")]
    )

    if file_path:
        # Usa thread per evitare il blocco della UI durante l'elaborazione
        threading.Thread(target=process_file_with_progress, args=(file_path, table, progress_bar, progress_var)).start()


# Modifica il metodo di apertura del file dialog nel main
def open_file_dialog():
    create_gui()


#######################
#######################
#######################


if __name__ == "__main__":
    open_file_dialog()