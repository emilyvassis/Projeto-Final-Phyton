# ==========================================================
# Sistema de Cadastro de Biblioteca
# Projeto final do curso de Python
# ==========================================================

import json
import os
from datetime import date

# Nome do arquivo onde os dados ficam salvos (Etapa 5)
ARQUIVO_DADOS = "biblioteca.json"

# Lista global com os livros (cada livro é um dicionário) (Etapa 2)
livros = []


# ----------------------------------------------------------
# Funções auxiliares de entrada (Tratam entradas incorretas)
# ----------------------------------------------------------

def ler_texto(mensagem):
    """Pede um texto ao usuário e não aceita resposta vazia."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo não pode ficar vazio. Tente novamente.")


def ler_inteiro(mensagem, minimo, maximo):
    """Pede um número inteiro dentro de um intervalo válido."""
    while True:
        valor = input(mensagem).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Digite um número entre {minimo} e {maximo}.")


def encontrar_livro_por_titulo(titulo):
    """Procura um livro pelo título exato (sem diferenciar maiúsculas).
    Retorna o dicionário do livro ou None se não encontrar."""
    for livro in livros:
        if livro["titulo"].lower() == titulo.lower():
            return livro
    return None


def exibir_livro(numero, livro):
    """Mostra os dados de um livro de forma organizada."""
    print(f"{numero}. {livro['titulo']} | Autor: {livro['autor']} | "
          f"Ano: {livro['ano']} | Disponível: {livro['disponivel']}")


# ----------------------------------------------------------
# Etapa 5: Persistência com JSON
# ----------------------------------------------------------

def carregar_dados():
    """Lê o arquivo JSON e preenche a lista de livros."""
    global livros
    if not os.path.exists(ARQUIVO_DADOS):
        livros = []
        return
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            livros = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível ler o arquivo de dados. "
              "O acervo começará vazio.")
        livros = []


def salvar_dados():
    """Grava a lista de livros no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(livros, arquivo, ensure_ascii=False, indent=4)


# ----------------------------------------------------------
# Etapa 2: Cadastro de livros
# ----------------------------------------------------------

def cadastrar_livro():
    """Cadastra um novo livro e salva no arquivo."""
    print("\n--- Cadastro de Livro ---")
    titulo = ler_texto("Título: ")

    if encontrar_livro_por_titulo(titulo):
        print("Já existe um livro com esse título cadastrado.")
        return

    autor = ler_texto("Autor: ")
    ano = ler_inteiro("Ano de publicação: ", 1, date.today().year)

    livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "disponivel": "Sim"
    }
    livros.append(livro)
    salvar_dados()
    print(f"Livro '{titulo}' cadastrado com sucesso!")


# ----------------------------------------------------------
# Etapa 3: Consulta e busca
# ----------------------------------------------------------

def listar_livros(lista=None):
    """Exibe todos os livros (ou uma lista específica, ex.: ordenada)."""
    if lista is None:
        lista = livros
    print("\n--- Acervo ---")
    if not lista:
        print("Nenhum livro cadastrado.")
        return
    for numero, livro in enumerate(lista, start=1):
        exibir_livro(numero, livro)


def buscar_livros():
    """Busca livros por parte do título ou do autor."""
    print("\n--- Buscar Livro ---")
    print("1 - Buscar por título")
    print("2 - Buscar por autor")
    opcao = ler_inteiro("Escolha: ", 1, 2)

    campo = "titulo" if opcao == 1 else "autor"
    termo = ler_texto("Digite o termo de busca: ").lower()

    resultados = [livro for livro in livros if termo in livro[campo].lower()]

    if not resultados:
        print("Nenhum livro encontrado com esse termo.")
        return
    for numero, livro in enumerate(resultados, start=1):
        exibir_livro(numero, livro)


# ----------------------------------------------------------
# Etapa 4: Empréstimos e devoluções
# ----------------------------------------------------------

def emprestar_livro():
    """Marca um livro como emprestado (disponivel = 'Não')."""
    print("\n--- Empréstimo ---")
    livro = encontrar_livro_por_titulo(ler_texto("Título do livro: "))
    if livro is None:
        print("Livro não encontrado.")
    elif livro["disponivel"] == "Não":
        print("Este livro já está emprestado.")
    else:
        livro["disponivel"] = "Não"
        salvar_dados()
        print(f"Empréstimo de '{livro['titulo']}' realizado!")


def devolver_livro():
    """Marca um livro como devolvido (disponivel = 'Sim')."""
    print("\n--- Devolução ---")
    livro = encontrar_livro_por_titulo(ler_texto("Título do livro: "))
    if livro is None:
        print("Livro não encontrado.")
    elif livro["disponivel"] == "Sim":
        print("Este livro não está emprestado.")
    else:
        livro["disponivel"] = "Sim"
        salvar_dados()
        print(f"Devolução de '{livro['titulo']}' registrada!")


# ----------------------------------------------------------
# Etapa 6: Funcionalidades extras
# ----------------------------------------------------------

def mostrar_contador():
    """Extra 1: mostra total, disponíveis e emprestados."""
    total = len(livros)
    disponiveis = sum(1 for livro in livros if livro["disponivel"] == "Sim")
    emprestados = total - disponiveis
    print("\n--- Contador de Acervo ---")
    print(f"Total de livros: {total}")
    print(f"Disponíveis: {disponiveis}")
    print(f"Emprestados: {emprestados}")


def ordenar_livros():
    """Extra 2: exibe os livros ordenados por título ou por ano."""
    print("\n--- Ordenar Livros ---")
    print("1 - Ordem alfabética (título)")
    print("2 - Ordem cronológica (ano)")
    opcao = ler_inteiro("Escolha: ", 1, 2)

    if opcao == 1:
        ordenados = sorted(livros, key=lambda livro: livro["titulo"].lower())
    else:
        ordenados = sorted(livros, key=lambda livro: livro["ano"])
    listar_livros(ordenados)


def remover_livro():
    """Extra 3: remove um livro do sistema após confirmação."""
    print("\n--- Remover Livro ---")
    livro = encontrar_livro_por_titulo(ler_texto("Título do livro: "))
    if livro is None:
        print("Livro não encontrado.")
        return
    confirmacao = input(f"Remover '{livro['titulo']}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        livros.remove(livro)
        salvar_dados()
        print("Livro removido com sucesso.")
    else:
        print("Remoção cancelada.")


# ----------------------------------------------------------
# Etapa 1: Menu principal
# ----------------------------------------------------------

def exibir_menu():
    print("\n===== BIBLIOTECA =====")
    print("1 - Cadastrar livro")
    print("2 - Listar livros")
    print("3 - Buscar livro")
    print("4 - Emprestar livro")
    print("5 - Devolver livro")
    print("6 - Contador de acervo")
    print("7 - Listar ordenado")
    print("8 - Remover livro")
    print("0 - Sair")


def main():
    carregar_dados()
    while True:
        exibir_menu()
        opcao = ler_inteiro("Escolha uma opção: ", 0, 8)

        if opcao == 1:
            cadastrar_livro()
        elif opcao == 2:
            listar_livros()
        elif opcao == 3:
            buscar_livros()
        elif opcao == 4:
            emprestar_livro()
        elif opcao == 5:
            devolver_livro()
        elif opcao == 6:
            mostrar_contador()
        elif opcao == 7:
            ordenar_livros()
        elif opcao == 8:
            remover_livro()
        elif opcao == 0:
            salvar_dados()
            print("Dados salvos. Até logo!")
            break


# Só executa o programa se o arquivo for rodado diretamente
if __name__ == "__main__":
    main()
