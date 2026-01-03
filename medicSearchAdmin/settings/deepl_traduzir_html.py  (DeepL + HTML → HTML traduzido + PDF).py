from bs4 import BeautifulSoup
import deepl

AUTH_KEY = "sua-chave-deepl-aqui"
translator = deepl.Translator(AUTH_KEY)

def traduzir_html_deepl(entrada, saida_html, saida_pdf, origem='EN', destino='PT'):
    with open(entrada, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for texto in soup.find_all(string=True):
        if texto.parent.name in ['script', 'style', 'code', 'pre']:
            continue
        limpo = texto.strip()
        if limpo:
            try:
                trad = translator.translate_text(limpo, source_lang=origem, target_lang=destino).text
                texto.replace_with(trad)
            except Exception as e:
                print(f"Erro: {e}")

    with open(saida_html, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    # PDF simples (instale weasyprint para melhor layout: pip install weasyprint)
    try:
        from weasyprint import HTML
        HTML(saida_html).write_pdf(saida_pdf)
    except:
        print("Instale weasyprint para gerar PDF do HTML: pip install weasyprint")

    print("Concluído! HTML:", saida_html, "PDF:", saida_pdf)

# EXEMPLO
traduzir_html_deepl("pagina.html", "pagina_traduzida_deepl.html", "pagina_traduzida_deepl.pdf")