"""Módulo para gerenciamento de livros."""

from copy import deepcopy
import json
import os


_livros = []
_ARQUIVO_DADOS = os.path.join("dados", "livros.json")

__all__ = [
    "acessa_livro",
    "acessa_livros",
    "acessa_livros_por_tag",
    "cria_livro",
    "modifica_livro",
    "deleta_livro",
    "carrega_dados",
    "salva_dados",
]


def _eh_livro_valido(livro):
    """Valida se um dicionário representa um livro."""
    campos_obrigatorios = ["id_livro", "nome", "autor", "tags"]

    if not isinstance(livro, dict):
        return False

    if not all(campo in livro for campo in campos_obrigatorios):
        return False

    if not isinstance(livro["id_livro"], int) or livro["id_livro"] <= 0:
        return False

    if not isinstance(livro["nome"], str) or livro["nome"].strip() == "":
        return False

    if not isinstance(livro["autor"], str) or livro["autor"].strip() == "":
        return False

    if not isinstance(livro["tags"], list):
        return False

    return True


def acessa_livro(id_livro):
    """Retorna o livro indicado pelo ID.

    Retorna:
        (0, livro): livro encontrado.
        (1, None): livro não encontrado.
    """
    for livro in _livros:
        if livro["id_livro"] == id_livro:
            return 0, deepcopy(livro)

    return 1, None


def acessa_livros():
    """Retorna todos os livros cadastrados.

    Retorna:
        (0, livros): existem livros cadastrados.
        (1, []): não existem livros cadastrados.
    """
    if len(_livros) == 0:
        return 1, []

    return 0, deepcopy(_livros)


def acessa_livros_por_tag(tag):
    """Retorna os livros associados a uma tag.

    Retorna:
        (0, livros): foram encontrados livros com a tag.
        (1, []): nenhum livro possui a tag.
        (2, []): tag inválida.
    """
    if not isinstance(tag, str) or tag.strip() == "":
        return 2, []

    livros_encontrados = []
    for livro in _livros:
        if tag in livro["tags"]:
            livros_encontrados.append(deepcopy(livro))

    if len(livros_encontrados) == 0:
        return 1, []

    return 0, livros_encontrados


def cria_livro(novo_livro):
    """Cadastra um novo livro.

    Retorna:
        0: livro cadastrado.
        2: dados inválidos.
        3: ID já cadastrado.
    """
    if not _eh_livro_valido(novo_livro):
        return 2

    for livro in _livros:
        if livro["id_livro"] == novo_livro["id_livro"]:
            return 3

    _livros.append(deepcopy(novo_livro))
    return 0


def modifica_livro(id_livro, novo_livro):
    """Modifica um livro já cadastrado.

    Retorna:
        0: livro modificado.
        1: livro não encontrado.
        2: dados inválidos ou tentativa de alterar o ID.
    """
    if not _eh_livro_valido(novo_livro):
        return 2

    for indice, livro in enumerate(_livros):
        if livro["id_livro"] == id_livro:
            if novo_livro["id_livro"] != id_livro:
                return 2
            _livros[indice] = deepcopy(novo_livro)
            return 0

    return 1


def deleta_livro(id_livro):
    """Remove um livro cadastrado.

    Retorna:
        0: livro removido.
        1: livro não encontrado.
    """
    for livro in _livros:
        if livro["id_livro"] == id_livro:
            _livros.remove(livro)
            return 0

    return 1


def carrega_dados():
    """Carrega os livros do arquivo para a estrutura encapsulada.

    Retorna:
        0: dados carregados ou arquivo ainda inexistente.
        2: conteúdo do arquivo inválido.
    """
    _livros.clear()

    if not os.path.exists(_ARQUIVO_DADOS):
        return 0

    with open(_ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        return 2

    for livro in dados:
        if not _eh_livro_valido(livro):
            _livros.clear()
            return 2
        _livros.append(deepcopy(livro))

    return 0


def salva_dados():
    """Grava os livros encapsulados no arquivo e retorna 0."""
    os.makedirs(os.path.dirname(_ARQUIVO_DADOS), exist_ok=True)
    with open(_ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(_livros, arquivo, ensure_ascii=False, indent=2)
    return 0
