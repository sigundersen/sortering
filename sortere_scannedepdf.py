import os
import shutil

# Angi kilde- og destinasjonsmapper
source_dir = r'C:\ZIP_Output_lokasjon\Skannede_PDFer'  # Mappen der skannede PDF-er er
tegninger_dir = r'C:\ZIP_Output_lokasjon\Skannede_PDFer\Tegninger'  # Mappen der tegninger skal lagres
notater_dir = r'C:\ZIP_Output_lokasjon\Skannede_PDFer\Notater'  # Mappen der notater skal lagres

# Opprett mapper hvis de ikke eksisterer
os.makedirs(tegninger_dir, exist_ok=True)
os.makedirs(notater_dir, exist_ok=True)

# Liste over søkeord som indikerer at en fil er en tegning
tegning_keywords = ['plan', 'Plan', 'tegning', 'Tegning', 'etg', 'Etg', 'etasje', 'Etasje']

def is_drawing_based_on_filename(filename):
    """
    Sjekker om filnavnet inneholder ord som indikerer at det er en tegning.
    """
    for keyword in tegning_keywords:
        if keyword in filename:
            return True
    return False

def sort_pdfs(source_dir):
    """
    Går gjennom alle PDF-er i kildemappen og sorterer dem i 'Tegninger' eller 'Notater' basert på filnavn.
    """
    for filename in os.listdir(source_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(source_dir, filename)
            
            print(f"Behandler {filename}...")

            # Bestem om filen er en tegning basert på filnavnet
            if is_drawing_based_on_filename(filename):
                # Flytt til "Tegninger"
                shutil.move(file_path, os.path.join(tegninger_dir, filename))
                print(f"{filename} er flyttet til Tegninger.")
            else:
                # Flytt til "Notater"
                shutil.move(file_path, os.path.join(notater_dir, filename))
                print(f"{filename} er flyttet til Notater.")

# Kjør sorteringen
sort_pdfs(source_dir)
