import os
import shutil

# Definer kildemappen
source_dir = r'C:\ZIP_Output_lokasjon'  # Sett inn din mappebane her

# Definer filtypene og deres respektive mapper
file_types = {
    'Tekstfiler': ['.txt', '.csv', '.md', '.log'],
    'Word_dokumenter': ['.doc', '.docx', '.odt', '.rtf'],
    'PDF': ['.pdf'],
    'Excel_og_regneark': ['.xls', '.xlsx', '.xlsm', '.ods'],
    'Presentasjoner': ['.ppt', '.pptx', '.odp'],
    '3D_filer': ['.ifc', '.rvt', '.pln', '.dwg', '.dxf', '.stl', '.obj', '.fbx', '.dae', '.3ds', '.blend'],
    'Bilder': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.heic', '.ico', '.webp'],
    'Videoer': ['.mp4', '.mkv', '.mov', '.avi', '.flv', '.wmv', '.webm', '.m4v', '.3gp'],
    'Lyd': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.aiff'],
    'Arkivfiler': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Programfiler': ['.exe', '.msi', '.bat', '.sh', '.bin', '.cmd'],
    'Skriptfiler': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.c', '.sh', '.bat', '.go', '.rb'],
    'Konfigurasjonsfiler': ['.ini', '.cfg', '.conf', '.env', '.json', '.xml', '.yaml', '.yml'],
    'Databaser': ['.sql', '.db', '.sqlite', '.mdb', '.accdb'],
    'Sprettbrettdokumenter': ['.epub', '.mobi'],
    'Skannede_PDFer': ['.pdf'],  # Trenger ekstra logikk for å skille skannede PDFer fra vanlige
    'Andre': ['.iso', '.dll', '.sys', '.log', '.bak']  # For andre filtyper som ikke er spesifisert
}

# Funksjon for å sjekke om en PDF er skannet (inneholder hovedsakelig bilder)
def is_scanned_pdf(file_path):
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(file_path)
        return len(text.strip()) == 0
    except Exception as e:
        print(f"Feil ved sjekking av skannet PDF: {e}")
        return False

# Opprett undermappene hvis de ikke eksisterer
for folder in file_types.keys():
    os.makedirs(os.path.join(source_dir, folder), exist_ok=True)

# Gå gjennom alle filer i kildemappen
for filename in os.listdir(source_dir):
    file_path = os.path.join(source_dir, filename)
    if os.path.isfile(file_path):
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        moved = False
        for folder, extensions in file_types.items():
            if ext in extensions:
                if folder == 'Skannede_PDFer' and ext == '.pdf':
                    if is_scanned_pdf(file_path):
                        shutil.move(file_path, os.path.join(source_dir, folder, filename))
                        moved = True
                        break
                elif folder == 'PDF' and ext == '.pdf':
                    if not is_scanned_pdf(file_path):
                        shutil.move(file_path, os.path.join(source_dir, folder, filename))
                        moved = True
                        break
                else:
                    shutil.move(file_path, os.path.join(source_dir, folder, filename))
                    moved = True
                    break

        if not moved:
            # Hvis filen ikke passer inn i noen kategori, flytt den til "Andre"-mappen
            other_folder = os.path.join(source_dir, 'Andre')
            os.makedirs(other_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(other_folder, filename))

print("Sortering fullført!")
