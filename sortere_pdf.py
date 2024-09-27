import os
import shutil
from PyPDF2 import PdfReader

# Definer mapper for kategorisering
source_dir = r'C:\ZIP_Output_lokasjon\PDF'  # Mappen der PDF-filene er lagret
brann_dir = r'C:\ZIP_Output_lokasjon\PDF\Brann'
elektro_dir = r'C:\ZIP_Output_lokasjon\PDF\Elektro'
tegninger_dir = r'C:\ZIP_Output_lokasjon\PDF\Tegninger'
ovrig_dir = r'C:\ZIP_Output_lokasjon\PDF\Ovrig'

# Opprett mapper hvis de ikke eksisterer
os.makedirs(brann_dir, exist_ok=True)
os.makedirs(elektro_dir, exist_ok=True)
os.makedirs(tegninger_dir, exist_ok=True)
os.makedirs(ovrig_dir, exist_ok=True)

# Nøkkelord for hver kategori (i prioritert rekkefølge)
keywords = {
    'Brann': ['brann', 'rømning', 'orientering', 'brannkonsept'],
    'Elektro': ['elektro', 'samsvarserklæring'],
    'Tegninger': ['tegning', 'plan', 'etg']
}

# Funksjon for å lese tekst fra en PDF (tekstbasert PDF)
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Feil ved lesing av {file_path}: {e}")
    return text.lower()

# Funksjon for å bestemme hvilket tema PDF-en tilhører
def categorize_pdf(file_name, file_text):
    # Søk gjennom temaer i prioritert rekkefølge
    for category, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in file_name.lower() or keyword in file_text:
                return category
    return 'Øvrig'

# Funksjon for å flytte PDF-en til riktig mappe
def move_to_category(file_path, category):
    if category == 'Brann':
        shutil.move(file_path, os.path.join(brann_dir, os.path.basename(file_path)))
    elif category == 'Elektro':
        shutil.move(file_path, os.path.join(elektro_dir, os.path.basename(file_path)))
    elif category == 'Tegninger':
        shutil.move(file_path, os.path.join(tegninger_dir, os.path.basename(file_path)))
    else:
        shutil.move(file_path, os.path.join(ovrig_dir, os.path.basename(file_path)))

# Funksjon for å sortere alle PDF-er
def sort_pdfs(source_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(source_dir, filename)
            
            print(f"Behandler {filename}...")

            # Trekk ut tekst fra PDF-en
            file_text = extract_text_from_pdf(file_path)

            # Bestem kategori basert på filnavn og tekst
            category = categorize_pdf(filename, file_text)

            # Flytt filen til riktig mappe
            move_to_category(file_path, category)
            print(f"{filename} er flyttet til {category}.")

# Kjør sorteringen
sort_pdfs(source_dir)
