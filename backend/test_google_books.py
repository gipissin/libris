import requests

url = "https://openlibrary.org/search.json"
params = {
    "title": "The Hobbit",
    "fields": "key,title,author_name,first_publish_year,edition_count,cover_i,isbn",
    "limit": 5
}

#Requisição da API
try:
    resposta_api = requests.get(
        url,
        params=params,
        headers={"User-Agent": "Libris/0.1"}
    )
    resposta_api.raise_for_status()
    #Converte o json em um dicionario python
    dados_json = resposta_api.json()

    biblioteca = []

    for livro_api in dados_json["docs"]:
        autores = livro_api.get("author_name")

        # Tratamento do título
        titulo = livro_api.get("title")
        titulo_sem_espaco = ""

        if isinstance(titulo, str):
            titulo_sem_espaco = titulo.strip()

        # Tratamento do ISBN
        isbn = livro_api.get("isbn") or []

        # Verificação de duplicidade
        duplicado = False

        for livro_existente in biblioteca:
            isbns_cadastrados = livro_existente["isbn"]

            for isbn_novo in isbn:
                if isbn_novo in isbns_cadastrados:
                    duplicado = True
                    break

            if duplicado:
                break

        # Cadastro do livro
        if duplicado:
            print("Livro já cadastrado!")
        else:
            livro = {
                "titulo": titulo_sem_espaco or "Titulo desconhecido",
                "autor": autores[0] if autores else "Autor desconhecido",
                "ano": livro_api.get("first_publish_year") or "Ano de publicação desconhecido",
                "quantidade_edicoes": livro_api.get("edition_count") or "Quantidade de edições desconhecidas",
                "isbn": isbn or "ISBN inexistente"
            }

            biblioteca.append(livro)

    print(f"Quantidade de livros: {len(biblioteca)}")
    print(biblioteca)
except requests.exceptions.ConnectionError:
    print("Não foi possível conectar à API.")
except requests.exceptions.HTTPError:
    print(f"Erro HTTP: código {resposta_api.status_code}")





