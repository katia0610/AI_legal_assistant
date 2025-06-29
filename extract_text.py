import fitz  # PyMuPDF

def extract_from_page_9(pdf_path, output_txt_path):
    """
    Extrait le texte à partir de la page 9 jusqu'à la fin du PDF et le sauvegarde dans un fichier texte.
    :param pdf_path: chemin vers le fichier PDF
    :param output_txt_path: chemin vers le fichier texte de sortie
    """
    with fitz.open(pdf_path) as doc:
        start_page = 1  # page 9 en index Python
        total_pages = 154

        with open(output_txt_path, "w", encoding="utf-8") as f_out:
            for page_num in range(start_page, total_pages):
                page = doc[page_num]
                text = page.get_text("text")

                # Sauvegarde du texte avec indication de la page
                f_out.write(text)
                f_out.write("\n\n")

    print(f"✅ Texte extrait et sauvegardé dans {output_txt_path}")

# 🔎 Exemple d'utilisation
if __name__ == "__main__":
    pdf_path = "ressources/code_penal.pdf"
    output_txt_path = "output/code_penal_extrait.txt"
    extract_from_page_9(pdf_path, output_txt_path)
