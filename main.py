from PIL import Image, ImageEnhance
import pytesseract
import ollama  # client Python pour Ollama

# Spécifier le chemin de Tesseract sur Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
    {texte}

    Génère un résumé médical clair :
    - Résultats normaux et anormaux
    - Risques détectés
    - Recommandations de suivi ou traitement (à valider par un médecin)
    """
    response = ollama.chat(
        model="llama3.2",  # modèle que tu as téléchargé
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# Pipeline complet
if __name__ == "__main__":
    image_path = r"./data/bilan_sante.png"

    print("Extraction OCR...")
    texte = extract_text_from_image(image_path)
    print("Texte extrait :", texte[:500], "...\n")

    print("Analyse avec LLaMA 3.2 (local via Ollama)...")
    avis = analyze_with_llama(texte)
    print("Avis médical généré :\n", avis)
