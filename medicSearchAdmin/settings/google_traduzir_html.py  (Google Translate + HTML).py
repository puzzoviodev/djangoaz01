from bs4 import BeautifulSoup
from googletrans import Translator
import time

translator = Translator()

def traduzir_html_google(entrada, saida_html, saida_pdf, origem='en', destino='pt'):
    with open(entrada, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for texto in soup.find_all(string=True):
        if texto.parent.name in ['script', 'style', 'code', 'pre']:
            continue
        limpo = texto.strip()
        if limpo:
            try:
                trad = translator.translate(limpo, src=origem, dest=destino).text
                texto.replace_with(trad)
                time.sleep(0.5)
            except Exception as e:
                print(f"Erro: {e}")

    with open(saida_html, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    # PDF com weasyprint (opcional)
    try:
        from weasyprint import HTML
        HTML(saida_html).write_pdf(saida_pdf)
    except:
        print("Instale weasyprint para PDF: pip install weasyprint")

    print("Concluído! HTML:", saida_html)

# EXEMPLO

pip install deepl-python pymupdf beautifulsoup4 googletrans==4.0.0-rc1 weasyprint
traduzir_html_google("pagina.html", "pagina_traduzida_google.html", "pagina_google.pdf")