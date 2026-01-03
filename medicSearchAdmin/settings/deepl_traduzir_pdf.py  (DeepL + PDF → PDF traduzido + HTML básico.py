import fitz  # PyMuPDF
import deepl

# SUBSTITUA PELA SUA CHAVE GRATUITA DO DEEPL (cadastre em www.deepl.com/pro-api)
AUTH_KEY = "sua-chave-deepl-aqui"
translator = deepl.Translator(AUTH_KEY)

def traduzir_pdf_deepl(entrada, saida_pdf, saida_html, origem='EN', destino='PT'):
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
                    trad = translator.translate_text(texto, source_lang=origem, target_lang=destino).text
                    rect = fitz.Rect(bloco[:4])
                    nova_pag.add_redact_annot(rect, fill=(1,1,1))  # Apaga original
                    nova_pag.apply_redactions()
                    nova_pag.insert_textbox(rect, trad, fontsize=11, fontname="helv")
                except Exception as e:
                    print(f"Erro: {e}")

    doc_novo.save(saida_pdf)
    doc_novo.close()
    doc.close()

    # HTML básico como bônus
    with open(saida_html, "w", encoding="utf-8") as f:
        f.write("<html><body><h1>PDF traduzido salvo em: " + saida_pdf + "</h1></body></html>")

    print("Concluído! PDF:", saida_pdf)

# EXEMPLO DE USO
traduzir_pdf_deepl("seu_livro.pdf", "livro_traduzido_deepl.pdf", "livro_traduzido_deepl.html")