from bs4 import BeautifulSoup
from googletrans import Translator
import time
import os

translator = Translator()


def traduzir_html_google(entrada, saida_html="livro_traduzido_google.html", origem='en', destino='pt'):
    with open(entrada, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    textos = soup.find_all(string=True)

    for texto in textos:
        if texto.parent.name in ['script', 'style', 'code', 'pre']:
            continue
        limpo = texto.strip()
        if limpo:
            try:
                trad = translator.translate(limpo, src=origem, dest=destino).text
                texto.replace_with(trad)
                time.sleep(0.5)  # Delay para evitar bloqueio em arquivos grandes
            except Exception as e:
                print(f"Erro ao traduzir: {e}")

    with open(saida_html, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"Tradução concluída! HTML traduzido salvo em: {saida_html}")


# Exemplo de uso
traduzir_html_google("livro_django4.html")
