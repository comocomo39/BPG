import os
import shutil
import pytesseract
from PIL import Image
import google.generativeai as genai
from tkinter import Tk, filedialog, messagebox
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Funzione per leggere la chiave API dal file API_KEY.txt
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

# Prompt aggiornato per diversi tipi di documenti
def analyze_file_with_gemini(file_content, extracted_text):
    """
    Analizza un file utilizzando il modello Gemini e restituisce le informazioni rilevanti.
    """
    prompt = f"""
    Gentile Intelligenza di Gemini,

    Ti prego di analizzare attentamente il file allegato e di identificare le seguenti informazioni:

    Testo estratto dal file: {extracted_text}

    1. Identificazione del Tipo di Documento:
        - Se il file è una carta d'identità, estrai i seguenti dati:
            - Nome
            - Cognome
            - Data di nascita (se presente)
        - Se il file è una fattura, estrai i seguenti dati:
            - Numero di fattura
            - Nome dell'emittente della fattura
            - Data della fattura
        - Se il file è un contratto di lavoro, estrai i seguenti dati:
            - Nome del dipendente
            - Posizione lavorativa
            - Stipendio annuale
            - Data di inizio del contratto
        - Se il file è una ricevuta di pagamento, estrai i seguenti dati:
            - Nome del cliente
            - Azienda emittente
            - Importo pagato
            - Data del pagamento
        - Se il file è un preventivo, estrai i seguenti dati:
            - Nome del cliente
            - Nome dell'azienda emittente
            - Prodotto o servizio quotato
            - Quantità
            - Prezzo unitario
            - Totale

    2. Rinomina del File:
        - Se il file è una carta d'identità, rinomina il file nel formato: 'cid_Nome_Cognome'.
        - Se il file è una fattura, rinomina il file nel formato: 'fattura_Numero'.
        - Se il file è un contratto di lavoro, rinomina il file nel formato: 'contratto_Nome_Cognome'.
        - Se il file è una ricevuta di pagamento, rinomina il file nel formato: 'ricevuta_Nome_Cognome'.
        - Se il file è un preventivo, rinomina il file nel formato: 'preventivo_Nome_Cognome'.

    3. Struttura dei Dati Utente:
        - Restituisci le informazioni sull'utente (nome, cognome e altri dati rilevanti) in un formato JSON, che includa anche il nuovo nome del file.

    Grazie per la tua assistenza.
    """

    try:
        # Se è un'immagine, passiamo l'immagine come oggetto Image, altrimenti solo il contenuto di testo
        response = model.generate_content([prompt, extracted_text])

        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                content_text = candidate.content.parts[0].text

                try:
                    json_data = json.loads(content_text.split('```json')[1].split('```')[0])
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


def process_file(file_path):
    """
    Gestisce l'intero processo: analisi del file, rinomina e organizzazione.
    """
    try:
        if file_path.endswith('.txt'):
            extracted_text = extract_text_from_txt(file_path)
        else:
            extracted_text, img = extract_text_from_image(file_path)

        # Analizza il file con il modello Gemini
        analysis_response = analyze_file_with_gemini(file_content=None, extracted_text=extracted_text)

        # Rinomina e organizza il file basato sull'analisi
        new_file_path = rename_and_organize_file(file_path, analysis_response)

        print(f"File rinominato e spostato in: {new_file_path}")
        messagebox.showinfo("Successo", f"File rinominato e spostato in: {new_file_path}")

    except Exception as e:
        print(f"Errore durante l'elaborazione del file: {str(e)}")
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")


def rename_and_organize_file(file_path, analysis_result):
    """
    Rinomina e organizza il file analizzato in base al risultato dell'analisi.
    """
    if analysis_result is None:
        print("Analisi del file fallita. Impossibile rinominare il file.")
        return None

    new_file_name = analysis_result.get('nuovo_nome_file', 'documento_sconosciuto')
    user_info = f"{analysis_result.get('nome', 'utente')}_{analysis_result.get('cognome', 'sconosciuto')}"

    user_folder = f"./documenti/{user_info}"
    os.makedirs(user_folder, exist_ok=True)

    ext = os.path.splitext(file_path)[1]
    new_file_path = os.path.join(user_folder, f"{new_file_name}{ext}")
    shutil.move(file_path, new_file_path)

    return new_file_path


def open_file_dialog():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleziona un file",
                                           filetypes=[("Immagini e file di testo", "*.png;*.jpg;*.jpeg;*.tiff;*.txt")])

    if file_path:
        process_file(file_path)


if __name__ == "__main__":
    open_file_dialog()
