from bs4 import BeautifulSoup
import deepl
import os

AUTH_KEY = "sua-chave-deepl-aqui"
translator = deepl.Translator(AUTH_KEY)

LIMITE_CARACTERES = 450000


def traduzir_html_dividido(entrada, pasta_saida="html_partes", origem='EN', destino='PT'):
    os.makedirs(pasta_saida, exist_ok=True)

    with open(entrada, "r", encoding="utf-8") as f:
        soup_original = BeautifulSoup(f, "html.parser")

    textos = [t for t in soup_original.find_all(string=True)
              if t.parent.name not in ['script', 'style', 'code', 'pre'] and t.strip()]

    parte_num = 1
    soup_parte = BeautifulSoup("<html><body></body></html>", "html.parser")
    body = soup_parte.body
    caracteres_acumulados = 0

    for texto in textos:
        limpo = texto.strip()
        if not limpo:
            continue

        if caracteres_acumulados + len(limpo) > LIMITE_CARACTERES:
            # Salva parte atual
            nome_html = f"{pasta_saida}/parte_{parte_num}.html"
            nome_pdf = f"{pasta_saida}/parte_{parte_num}.pdf"
            with open(nome_html, "w", encoding="utf-8") as f:
                f.write(soup_parte.prettify())
            try:
                from weasyprint import HTML
                HTML(nome_html).write_pdf(nome_pdf)
            except:
                print("weasyprint não instalado para PDF")
            print(f"Parte {parte_num} salva (~{caracteres_acumulados} chars)")

            # Nova parte
            parte_num += 1
            soup_parte = BeautifulSoup("<html><body></body></html>", "html.parser")
            body = soup_parte.body
            caracteres_acumulados = 0

        try:
            trad = translator.translate_text(limpo, source_lang=origem, target_lang=destino).text
            novo_tag = soup_parte.new_tag(texto.parent.name)
            novo_tag.string = trad
            for attr, value in texto.parent.attrs.items():
                novo_tag[attr] = value
            body.append(novo_tag)
            body.append(soup_parte.new_string("\n"))
        except Exception as e:
            print(f"Erro: {e}")

        caracteres_acumulados += len(limpo)

    # Salva última parte
    if caracteres_acumulados > 0:
        nome_html = f"{pasta_saida}/parte_{parte_num}.html"
        with open(nome_html, "w", encoding="utf-8") as f:
            f.write(soup_parte.prettify())
        print(f"Última parte salva: {nome_html}")


# USO
traduzir_html_dividido("pagina_grande.html", "partes_html_traduzidas")

Para Google Translate (sem limite, mas com delay para não ser bloqueado)
Os códigos do Google anteriores já funcionam com livros grandes, mas se quiser dividir também (para segurança), use os mesmos com time.sleep(1) entre páginas.
Como juntar os PDFs depois:

Site gratuito: https://www.ilovepdf.com/pt/juntar_pdf (arraste todas as partes em ordem e baixe o completo).
Ou no terminal (Linux/Mac): pdfunite livro_parte_*.pdf livro_completo_traduzido.pdf

Com isso, você traduz o Django 4 By Example inteiro em 3-4 meses usando o DeepL gratuito, com qualidade excelente.
Se quiser que eu adapte mais (ex: dividir por capítulos detectando títulos), é só pedir!
Agora é só rodar o primeiro script e começar a tradução da parte 1. Boa sorte com o Django! 🚀