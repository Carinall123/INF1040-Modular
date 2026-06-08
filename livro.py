# livro.py - Módulo para gerenciamento de livros
from copy import deepcopy
import json
import os

# Lista interna que armazena os livros cadastrados
livros = []
ARQUIVO_DADOS = os.path.join("dados", "livros.json")


def eh_livro_valido(livro):
    """Valida se um dicionário tem a estrutura mínima de um livro.

    Regras compatíveis com validação pré-existente:
    - deve ser dict
    - conter chaves: id_livro, nome, autor, tags
    - `id_livro`, `nome` e `autor` não podem ser None ou string vazia
    - `tags` deve ser lista
    """
    campos_obrigatorios = ["id_livro", "nome", "autor", "tags"]

    if not isinstance(livro, dict):
        return False

    if not all(campo in livro for campo in campos_obrigatorios):
        return False

    # Mantém similaridade com checagem anterior: rejeita None ou ""
    # `id_livro` deve ser inteiro positivo
    if not isinstance(livro["id_livro"], int) or livro["id_livro"] <= 0:
        return False

    if livro["nome"] is None or (isinstance(livro["nome"], str) and livro["nome"] == ""):
        return False

    if livro["autor"] is None or (isinstance(livro["autor"], str) and livro["autor"] == ""):
        return False

    if not isinstance(livro["tags"], list):
        return False

    return True


def acessa_livro(id_livro):
    """Retorna 0 se o livro existir e 1 caso contrário."""

    for livro in livros:
        # Procura o livro pelo ID informado
        if livro["id_livro"] == id_livro:
            return 0

    return 1


def acessa_livros():
    """Retorna 0 se houver livros cadastrados e 1 caso contrário."""

    if len(livros) == 0:
        return 1

    return 0


def acessa_livros_por_tag(tag):
    """Retorna 0 se houver livros com a tag, 1 se não houver e 2 se inválida."""
    if tag is None or not isinstance(tag, str) or tag.strip() == "":
        return 2

    for livro in livros:
        # Verifica se a tag pertence ao livro
        if tag in livro["tags"]:
            return 0

    return 1


def cria_livro(novo_livro):
    """Cadastra um novo livro no sistema."""
    if not eh_livro_valido(novo_livro):
        return 2

    # Verifica ID duplicado
    if any(livro["id_livro"] == novo_livro["id_livro"] for livro in livros):
        return 3

    livros.append(deepcopy(novo_livro))
    return 0


def modifica_livro(id_livro, novo_livro):
    """Modifica os dados de um livro já cadastrado."""
    # Validação básica
    if not eh_livro_valido(novo_livro):
        return 2

    livro_encontrado = None
    for livro in livros:
        if livro["id_livro"] == id_livro:
            livro_encontrado = livro
            break

    if livro_encontrado is None:
        return 1

    # Política escolhida: ID é imutável. Rejeita tentativas de alterar o id_livro.
    if novo_livro["id_livro"] != id_livro:
        return 2

    livro_encontrado["nome"] = novo_livro["nome"]
    livro_encontrado["autor"] = novo_livro["autor"]
    livro_encontrado["tags"] = deepcopy(novo_livro["tags"])
    return 0


def deleta_livro(id_livro):
    """Remove um livro cadastrado do sistema e retorna código de resultado."""

    for livro in livros:
        # Procura o livro que será removido
        if livro["id_livro"] == id_livro:
            livros.remove(livro)

            return 0

    return 1


def define_livros(nova_lista):
    """Define a lista de livros carregada pela main.

    A `main.py` deve chamar esta função ao carregar os dados do arquivo.
    """
    global livros
    livros = deepcopy(nova_lista)


def retorna_livros():
    """Retorna uma cópia da lista de livros para persistência.

    A `main.py` deve usar esta função para obter os dados para salvar em arquivo.
    """
    return deepcopy(livros)


def carrega_dados():
    """Carrega os livros do arquivo de dados para a estrutura encapsulada."""
    if not os.path.exists(ARQUIVO_DADOS):
        define_livros([])
        return 0

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        define_livros([])
        return 2

    define_livros(dados)
    return 0


def salva_dados():
    """Grava os livros encapsulados no arquivo de dados."""
    os.makedirs(os.path.dirname(ARQUIVO_DADOS), exist_ok=True)
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(retorna_livros(), arquivo, ensure_ascii=False, indent=2)
    return 0
