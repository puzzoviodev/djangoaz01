pip install beautifulsoup4 deepl-python googletrans==4.0.0-rc1 libretranslatepy

from bs4 import BeautifulSoup
import deepl
import os

# Sua chave gratuita do DeepL (cadastre em www.deepl.com/pro-api)
AUTH_KEY = "sua-chave-deepl-aqui"
translator = deepl.Translator(AUTH_KEY)

LIMITE_CARACTERES = 450000  # Margem de segurança para o limite mensal


def traduzir_html_deepl(entrada, pasta_saida="html_traduzido_deepl", origem='EN', destino='PT'):
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
            with open(nome_html, "w", encoding="utf-8") as f:
                f.write(soup_parte.prettify())
            print(f"Parte {parte_num} salva (~{caracteres_acumulados} chars): {nome_html}")

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
            print(f"Erro ao traduzir: {e}")

        caracteres_acumulados += len(limpo)

    # Salva última parte
    if caracteres_acumulados > 0:
        nome_html = f"{pasta_saida}/parte_{parte_num}.html"
        with open(nome_html, "w", encoding="utf-8") as f:
            f.write(soup_parte.prettify())
        print(f"Última parte salva: {nome_html}")

    print("Tradução concluída! Junte as partes manualmente se precisar de um HTML único.")


# Exemplo de uso (forneça seu livro em HTML)
traduzir_html_deepl("livro_django4.html")
