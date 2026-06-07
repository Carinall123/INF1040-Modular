# livro.py - Módulo para gerenciamento de livros
from copy import deepcopy

# Lista interna que armazena os livros cadastrados
livros = []


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
    """Retorna os dados de um livro a partir do seu ID."""

    for livro in livros:
        # Procura o livro pelo ID informado
        if livro["id_livro"] == id_livro:
            return deepcopy(livro)

    return None


def acessa_livros():
    """Retorna todos os livros cadastrados."""

    # Retorna cópia para proteger a lista interna
    return deepcopy(livros)


def acessa_livros_por_tag(tag):
    """Retorna os livros associados a uma determinada tag."""

    livros_encontrados = []

    for livro in livros:
        # Verifica se a tag pertence ao livro
        if tag in livro["tags"]:
            livros_encontrados.append(deepcopy(livro))

    return livros_encontrados


def cria_livro(novo_livro):
    """Cadastra um novo livro no sistema."""
    if not eh_livro_valido(novo_livro):
        return None

    # Verifica ID duplicado
    if any(livro["id_livro"] == novo_livro["id_livro"] for livro in livros):
        return None

    livros.append(deepcopy(novo_livro))
    return deepcopy(novo_livro)


def modifica_livro(id_livro, novo_livro):
    """Modifica os dados de um livro já cadastrado."""
    # Validação básica
    if not eh_livro_valido(novo_livro):
        return None

    # Política escolhida: ID é imutável. Rejeita tentativas de alterar o id_livro.
    if novo_livro["id_livro"] != id_livro:
        return None

    for livro in livros:
        if livro["id_livro"] == id_livro:
            livro["nome"] = novo_livro["nome"]
            livro["autor"] = novo_livro["autor"]
            livro["tags"] = deepcopy(novo_livro["tags"])
            return deepcopy(livro)

    return None


def deleta_livro(id_livro):
    """Remove um livro cadastrado do sistema."""

    for livro in livros:
        # Procura o livro que será removido
        if livro["id_livro"] == id_livro:
            livro_removido = deepcopy(livro)
            livros.remove(livro)

            return livro_removido

    return None


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