pip install libretranslatepy pymupdf beautifulsoup4 weasyprint

import fitz  # PyMuPDF
from libretranslatepy import LibreTranslateAPI
import time

# Escolha uma instância (mude se precisar)
lt = LibreTranslateAPI("https://translate.terraprint.co/")

def traduzir_pdf_libre(entrada, saida_pdf, saida_html, origem='en', destino='pt'):
    doc = fitz.open(entrada)
    doc_novo = fitz.open()

    for pag_num in range(len(doc)):
        pag = doc[pag_num]
        nova_pag = doc_novo.new_page(width=pag.rect.width, height=pag.rect.height)
        nova_pag.show_pdf_page(nova_pag.rect, doc, pag_num)  # Copia imagens/fundo

        blocos = pag.get_text("blocks")
        for bloco in blocos:
            texto = bloco[4].strip()
            if texto:
                try:
                    trad = lt.translate(texto, origem, destino)
                    rect = fitz.Rect(bloco[:4])
                    nova_pag.add_redact_annot(rect, fill=(1,1,1))
                    nova_pag.apply_redactions()
                    nova_pag.insert_textbox(rect, trad, fontsize=11, fontname="helv")
                    time.sleep(0.5)  # Gentileza com o servidor público
                except Exception as e:
                    print(f"Erro na página {pag_num+1}: {e}")

    doc_novo.save(saida_pdf)
    doc_novo.close()
    doc.close()

    # HTML básico como bônus
    with open(saida_html, "w", encoding="utf-8") as f:
        f.write("<html><body><h1>PDF traduzido com LibreTranslate salvo em: " + saida_pdf + "</h1></body></html>")

    print("Concluído! PDF traduzido:", saida_pdf)

# EXEMPLO DE USO
traduzir_pdf_libre("django4_by_example.pdf", "livro_traduzido_libre.pdf", "livro_libre.html")