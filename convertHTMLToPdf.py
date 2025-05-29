import pdfkit

# Spécifier le chemin vers wkhtmltopdf sous Windows
config = pdfkit.configuration(wkhtmltopdf=r"C:\\Users\bassem.jida\Downloads\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe")

# Options pour préserver CSS et images
options = {
    'enable-local-file-access': None,  # Accès aux fichiers locaux (images, CSS)
    'page-size': 'A4',
    'margin-top': '10mm',
    'margin-right': '10mm',
    'margin-bottom': '10mm',
    'margin-left': '10mm',
    'encoding': 'UTF-8',
    'no-outline': None,  # Empêche l'ajout d'un contour aux liens
    'enable-external-links': None  # Active les liens externes
}
# Convertir le fichier HTML en PDF
pdfkit.from_file('index.html', 'cv_Bassem_JIDA.pdf', configuration=config, options=options)

print("Conversion terminée avec succès sur Windows ! 🎉")

