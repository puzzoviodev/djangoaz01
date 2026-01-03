from bs4 import BeautifulSoup
from libretranslatepy import LibreTranslateAPI
import time
import os

# Instância pública (mude para "http://localhost:5000" se hospedar localmente)
lt = LibreTranslateAPI("https://translate.terraprint.co/")


def traduzir_html_libre(entrada, saida_html="livro_traduzido_libre.html", origem='en', destino='pt'):
    with open(entrada, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    textos = soup.find_all(string=True)

    for texto in textos:
        if texto.parent.name in ['script', 'style', 'code', 'pre']:
            continue
        limpo = texto.strip()
        if limpo:
            try:
                trad = lt.translate(limpo, origem, destino)
                texto.replace_with(trad)
                time.sleep(0.3)  # Delay para instâncias públicas
            except Exception as e:
                print(f"Erro ao traduzir: {e}")

    with open(saida_html, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"Tradução concluída! HTML traduzido salvo em: {saida_html}")


# Exemplo de uso
traduzir_html_libre("livro_django4.html")
Dicas finais:

Para livros grandes em HTML, o código do DeepL divide automaticamente para caber no limite. Para os outros, se for muito grande, adicione divisão manual (copie o loop do DeepL).
Hospede LibreTranslate localmente para velocidade e privacidade: docker run -it --rm -p 5000:5000 libretranslate/libretranslate.
Teste com um HTML pequeno primeiro. Quando fornecer o livro em HTML, basta mudar o nome do arquivo na chamada da função.

Se precisar de mais ajustes (ex: juntar partes ou melhorar preservação de layout), avise! 😊