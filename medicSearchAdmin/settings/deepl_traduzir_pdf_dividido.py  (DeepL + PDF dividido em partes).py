import fitz  # PyMuPDF
import deepl
import os

# SUA CHAVE GRATUITA DO DEEPL
AUTH_KEY = "sua-chave-deepl-aqui"
translator = deepl.Translator(AUTH_KEY)

LIMITE_CARACTERES = 450000  # Segurança: deixa margem do limite de 500k


def traduzir_pdf_dividido(entrada, pasta_saida="traduzido_partes", origem='EN', destino='PT'):
    os.makedirs(pasta_saida, exist_ok=True)

    doc = fitz.open(entrada)
    parte_num = 1
    doc_parte = fitz.open()
    caracteres_acumulados = 0

    for pag_num in range(len(doc)):
        pag = doc[pag_num]
        blocos = pag.get_text("blocks")
        texto_pagina = "".join([b[4] for b in blocos])
        caracteres_pagina = len(texto_pagina)

        # Se adicionar esta página ultrapassa o limite, salva a parte atual e começa nova
        if caracteres_acumulados + caracteres_pagina > LIMITE_CARACTERES and len(doc_parte) > 0:
            nome_parte = f"{pasta_saida}/livro_parte_{parte_num}.pdf"
            doc_parte.save(nome_parte)
            doc_parte.close()
            print(
                f"Parte {parte_num} salva ({len(doc_parte)} páginas, ~{caracteres_acumulados} caracteres): {nome_parte}")

            parte_num += 1
            doc_parte = fitz.open()
            caracteres_acumulados = 0

        # Adiciona página à parte atual
        nova_pag = doc_parte.new_page(width=pag.rect.width, height=pag.rect.height)
        nova_pag.show_pdf_page(nova_pag.rect, doc, pag_num)

        # Traduz blocos
        for bloco in blocos:
            texto = bloco[4].strip()
            if texto:
                try:
                    trad = translator.translate_text(texto, source_lang=origem, target_lang=destino).text
                    rect = fitz.Rect(bloco[:4])
                    nova_pag.add_redact_annot(rect, fill=(1, 1, 1))
                    nova_pag.apply_redactions()
                    nova_pag.insert_textbox(rect, trad, fontsize=11, fontname="helv")
                except Exception as e:
                    print(f"Erro na página {pag_num + 1}: {e}")

        caracteres_acumulados += caracteres_pagina

    # Salva a última parte
    if len(doc_parte) > 0:
        nome_parte = f"{pasta_saida}/livro_parte_{parte_num}.pdf"
        doc_parte.save(nome_parte)
        print(f"Última parte {parte_num} salva: {nome_parte}")

    doc_parte.close()
    doc.close()
    print("Tradução dividida concluída! Junte os PDFs depois com ilovepdf.com ou similar.")


# USO
traduzir_pdf_dividido("django4_by_example.pdf", "django4_traduzido_partes")