# health-report-analyzer
L’objectif de ce TP est de développer une application capable de lire automatiquement des bilans de santé (au format PDF ou image), d’en extraire le texte via un moteur OCR, puis d’utiliser un modèle de langage médical (LLM) pour analyser les résultats et générer un avis médical automatisé.

## Installation
### 1. Installation de OLLAMA, et LLAMA 3
- RDV sur ce site : https://ollama.com/download pour installer ollama.
- Lancer l'éxecutable, ou l'installation de ollama (ajouter au PATH Windows si nécessaire)
- Via une invite de commande, installez et lancer le modèle "LLAMA 3" :
```bash 
ollama run llama3
```
- Fin de l'installation de la LLM

### 2. Lancement du programme
- Installer les librairies nécessaires python pour le projet
- Dans un dossier ```/data/inputs/```, insérez des exemples de rapport médicaux (par défaut : report.png)
- Lancez main.py

### 3. Résultats
Voir dans le dossier ``/data/output/`` les résultats générés