from PIL import Image, ImageEnhance
import pytesseract
import ollama
# pour l'export de pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import os
import re
import random

# Spécifier le chemin de Tesseract sur Windows
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# OCR sur image PNG
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    # Améliorer contraste pour OCR
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    texte = pytesseract.image_to_string(image, lang="eng")
    return texte

# Analyse avec LLaMA 3.2 local via Ollama
def analyze_with_llama(texte):
    prompt = f"""
    Voici un bilan de santé extrait par OCR :
    context = {texte}
    
    Réponds toujours en français, quelle que soit la langue du context.
    Met en forme ce résumé avec des titres, des sous titres, etc...
    Génère un résumé médical clair basé sur le contexte donné. Ce résumé dois être assez court. Ce résumé dois se calquer sur ces informations :
    - Les resultat anormaux :
        - l'anomalie trouvé
        - et le resultat attendu si ça devais être normal
    - Les risques possible
    - Une conclusion :
        - Courte conclusion sur la situation global en la vulgarisant
        - Un score sur /10 sur le risque de complication pour le patient
    """
    response = ollama.chat(
        model="llama3",  # modèle que tu as téléchargé
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# export en pdf du résumé
def export_text(txt):
    out_dir = "./data/output"
    os.makedirs(out_dir, exist_ok=True)
    id_path_name = random.randint(0, 1000)
    name_path = f"rapport-assurance_" + str(id_path_name) + ".pdf"
    file_path = os.path.join(out_dir, name_path)

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    title = styles["Heading2"]

    story = []

    html_text = txt
    html_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html_text)  # **gras**
    html_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", html_text)  # *italique*

    for para in html_text.split("\n"):
        para = para.strip()
        if not para:
            continue
        # Si le paragraphe commence par <b>…</b> on le traite comme un titre
        if re.match(r"^<b>.*</b>$", para):
            story.append(Paragraph(para, title))
        else:
            story.append(Paragraph(para, normal))
        story.append(Spacer(1, 0.5 * cm))

    doc.build(story)
    print(f"Rapport PDF exporté : {file_path}")
    return file_path

# Pipeline complet
if __name__ == "__main__":
    # changer ici le chemin pour l'image du rapport
    image_path = r"./data/inputs/report.png"

    # extraction OCR
    print("Extraction OCR...")
    texte = extract_text_from_image(image_path)
    print("Fin extraction par l'OCR")

    # Analyse par la LLM
    print("Analyse avec la LLM ...")
    avis = analyze_with_llama(texte)
    print("Fin analyse par la LLM")

    # export en PDF
    export_text(avis)
