import re
import os

def garder_francais(texte):
    lignes = texte.splitlines()
    lignes_fr = []
    for ligne in lignes:
        # Nettoyage espace
        ligne = ligne.strip()
        # Ignorer lignes vides
        if not ligne:
            continue
        # Regex : conserve si au moins un caractère a-zA-Z (latin)
        if re.search(r'[a-zA-Z]', ligne):
            lignes_fr.append(ligne)
    return '\n'.join(lignes_fr)

# 🔧 Lecture du fichier PDF extrait
input_path = "output/code_penal_extrait.txt"
output_path = "output/code_penal_extrait_clean.txt"

with open(input_path, "r", encoding="utf-8") as f:
    contenu = f.read()

# 🔧 Filtrage français
resultat_fr = garder_francais(contenu)

# ✅ Sauvegarde du résultat
# Créer dossier output/ s'il n'existe pas
os.makedirs("output", exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(resultat_fr)

print(f"✅ Texte français sauvegardé dans : {output_path}")
