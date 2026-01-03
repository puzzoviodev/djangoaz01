import fitz
from googletrans import Translator
import time

translator = Translator()

def traduzir_pdf_google(entrada, saida_pdf, saida_html, origem='en', destino='pt'):
    doc = fitz.open(entrada)
    doc_novo = fitz.open()

    for pag_num in range(len(doc)):
        pag = doc[pag_num]
        nova_pag = doc_novo.new_page(width=pag.rect.width, height=pag.rect.height)
        nova_pag.show_pdf_page(nova_pag.rect, doc, pag_num)

        blocos = pag.get_text("blocks")
        for bloco in blocos:
            texto = bloco[4].strip()
            if texto:
                try:
                    trad = translator.translate(texto, src=origem, dest=destino).text
                    rect = fitz.Rect(bloco[:4])
                    nova_pag.add_redact_annot(rect, fill=(1,1,1))
                    nova_pag.apply_redactions()
                    nova_pag.insert_textbox(rect, trad, fontsize=11, fontname="helv")
                    time.sleep(1)  # Evita bloqueio
                except Exception as e:
                    print(f"Erro: {e}")

    doc_novo.save(saida_pdf)
    doc_novo.close()
    doc.close()

    with open(saida_html, "w", encoding="utf-8") as f:
        f.write("<html><body><h1>PDF traduzido com Google salvo!</h1></body></html>")

    print("Concluído! PDF:", saida_pdf)

# EXEMPLO
traduzir_pdf_google("seu_livro.pdf", "livro_traduzido_google.pdf", "livro_google.html")