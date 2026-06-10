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


def _normaliza_nome(nome):
    """Normaliza um nome de livro para comparação."""
    return nome.strip().casefold()


def acessa_livro(nome_livro):
    """Consulta um livro pelo nome.

    Parâmetros:
        nome_livro: Texto com o nome procurado. A comparação ignora espaços
            no início e no fim e diferenças entre maiúsculas e minúsculas.

    Retorna:
        (0, livro): Livro encontrado. O registro retornado é uma cópia.
        (1, None): Livro não encontrado.
        (2, None): Nome não textual, vazio ou formado somente por espaços.

    Efeito no TAD:
        Não altera os livros armazenados.
    """
    if not isinstance(nome_livro, str) or nome_livro.strip() == "":
        return 2, None

    nome_procurado = _normaliza_nome(nome_livro)
    for livro in _livros:
        if _normaliza_nome(livro["nome"]) == nome_procurado:
            return 0, deepcopy(livro)

    return 1, None


def acessa_livros():
    """Consulta todos os livros cadastrados.

    Parâmetros:
        Nenhum.

    Retorna:
        (0, livros): Lista com cópias de todos os livros.
        (1, []): Não existem livros cadastrados.

    Efeito no TAD:
        Não altera os livros armazenados.
    """
    if len(_livros) == 0:
        return 1, []

    return 0, deepcopy(_livros)


def acessa_livros_por_tag(tag):
    """Consulta os livros que possuem uma tag.

    Parâmetros:
        tag: Texto comparado de forma exata com os elementos da lista ``tags``
            de cada livro.

    Retorna:
        (0, livros): Lista com cópias dos livros encontrados.
        (1, []): Nenhum livro possui a tag.
        (2, []): Tag não textual, vazia ou formada somente por espaços.

    Efeito no TAD:
        Não altera os livros armazenados.
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
    """Cadastra um livro.

    Parâmetros:
        novo_livro: Dicionário completo com ``id_livro``, ``nome``, ``autor``
            e ``tags``. O ID deve ser inteiro positivo; nome e autor devem ser
            textos não vazios; tags deve ser uma lista.

    Retorna:
        0: Livro cadastrado.
        2: Registro ausente, incompleto ou com algum campo inválido.
        3: Já existe livro com o mesmo ``id_livro`` ou nome. A comparação dos
            nomes ignora espaços externos e diferenças entre maiúsculas e
            minúsculas.

    Efeito no TAD:
        Em caso de sucesso, armazena uma cópia de ``novo_livro``.
    """
    if not _eh_livro_valido(novo_livro):
        return 2

    for livro in _livros:
        if (
            livro["id_livro"] == novo_livro["id_livro"]
            or _normaliza_nome(livro["nome"])
            == _normaliza_nome(novo_livro["nome"])
        ):
            return 3

    _livros.append(deepcopy(novo_livro))
    return 0


def modifica_livro(id_livro, novo_livro):
    """Substitui os dados de um livro preservando seu identificador.

    Parâmetros:
        id_livro: Identificador do livro que será modificado.
        novo_livro: Registro completo com os novos dados do livro.

    Retorna:
        0: Livro modificado.
        1: Livro não encontrado.
        2: Novos dados inválidos ou tentativa de alterar ``id_livro``.
        3: O novo nome pertence a outro livro.

    Efeito no TAD:
        Em caso de sucesso, substitui o registro por uma cópia de
        ``novo_livro``.
    """
    if not _eh_livro_valido(novo_livro):
        return 2

    for indice, livro in enumerate(_livros):
        if livro["id_livro"] == id_livro:
            if novo_livro["id_livro"] != id_livro:
                return 2

            for outro_livro in _livros:
                if (
                    outro_livro["id_livro"] != id_livro
                    and _normaliza_nome(outro_livro["nome"])
                    == _normaliza_nome(novo_livro["nome"])
                ):
                    return 3

            _livros[indice] = deepcopy(novo_livro)
            return 0

    return 1


def deleta_livro(id_livro):
    """Remove um livro por seu identificador.

    Parâmetros:
        id_livro: Identificador usado para localizar o livro.

    Retorna:
        0: Livro removido.
        1: Livro não encontrado.

    Efeito no TAD:
        Remove o registro encontrado.
    """
    for livro in _livros:
        if livro["id_livro"] == id_livro:
            _livros.remove(livro)
            return 0

    return 1


def carrega_dados():
    """Inicializa o TAD com o conteúdo de ``dados/livros.json``.

    Parâmetros:
        Nenhum.

    Retorna:
        0: Arquivo carregado ou arquivo ainda inexistente.
        2: O conteúdo JSON não é uma lista válida, contém livro inválido ou
            contém IDs ou nomes duplicados.

    Efeito no TAD:
        Limpa os dados atuais antes da leitura. Se o conteúdo estrutural for
        inválido, o TAD permanece vazio.

    Exceções:
        Erros de leitura e JSON malformado são propagados ao módulo cliente.
    """
    _livros.clear()

    if not os.path.exists(_ARQUIVO_DADOS):
        return 0

    with open(_ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        return 2

    ids_carregados = set()
    nomes_carregados = set()

    for livro in dados:
        if not _eh_livro_valido(livro):
            _livros.clear()
            return 2

        id_livro = livro["id_livro"]
        nome_livro = _normaliza_nome(livro["nome"])
        if id_livro in ids_carregados or nome_livro in nomes_carregados:
            _livros.clear()
            return 2

        ids_carregados.add(id_livro)
        nomes_carregados.add(nome_livro)
        _livros.append(deepcopy(livro))

    return 0


def salva_dados():
    """Persiste os livros encapsulados em ``dados/livros.json``.

    Parâmetros:
        Nenhum.

    Retorna:
        0: Dados gravados.

    Efeito externo:
        Cria o diretório ``dados``, quando necessário, e substitui o conteúdo
        do arquivo pelo estado atual do TAD.

    Exceções:
        Erros do sistema de arquivos são propagados ao módulo cliente.
    """
    os.makedirs(os.path.dirname(_ARQUIVO_DADOS), exist_ok=True)
    with open(_ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(_livros, arquivo, ensure_ascii=False, indent=2)
    return 0
