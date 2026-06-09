"""Módulo para gerenciamento de avaliações de livros."""

from copy import deepcopy
import json
import os


_avaliacoes = []
_proximo_id = 1
_ARQUIVO_DADOS = os.path.join("dados", "avaliacoes.json")

__all__ = [
    "acessa_avaliacao",
    "acessa_avaliacoes_livro",
    "acessa_avaliacoes_usuario",
    "cria_avaliacao",
    "modifica_avaliacao",
    "deleta_avaliacao",
    "calculaNotas",
    "carrega_dados",
    "salva_dados",
]


def _eh_dados_avaliacao_validos(avaliacao):
    """Valida os dados recebidos para criar ou modificar uma avaliação."""
    campos_obrigatorios = ["nota", "id_livro", "id_user"]

    if not isinstance(avaliacao, dict):
        return False

    if not all(campo in avaliacao for campo in campos_obrigatorios):
        return False

    nota = avaliacao["nota"]
    if not isinstance(nota, (int, float)) or nota < 0 or nota > 5:
        return False

    if not isinstance(avaliacao["id_livro"], int) or avaliacao["id_livro"] <= 0:
        return False

    id_user = avaliacao["id_user"]
    if id_user is None or (isinstance(id_user, str) and id_user.strip() == ""):
        return False

    return True


def _eh_avaliacao_armazenada_valida(avaliacao):
    """Valida uma avaliação completa armazenada pelo módulo."""
    if not _eh_dados_avaliacao_validos(avaliacao):
        return False

    return (
        isinstance(avaliacao.get("id_avaliacao"), int)
        and avaliacao["id_avaliacao"] > 0
    )


def _gera_id_avaliacao():
    """Gera o próximo identificador de avaliação."""
    global _proximo_id
    id_avaliacao = _proximo_id
    _proximo_id = _proximo_id + 1
    return id_avaliacao


def acessa_avaliacao(id_avaliacao):
    """Retorna a primeira avaliação que possui o ID informado.

    Retorna:
        (0, avaliação): avaliação encontrada.
        (1, None): avaliação não encontrada.
    """
    for avaliacao in _avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            return 0, deepcopy(avaliacao)

    return 1, None


def acessa_avaliacoes_livro(id_livro):
    """Retorna as avaliações associadas a um livro.

    Retorna:
        (0, avaliações): existem avaliações para o livro.
        (1, []): não existem avaliações para o livro.
    """
    avaliacoes_livro = []
    for avaliacao in _avaliacoes:
        if avaliacao["id_livro"] == id_livro:
            avaliacoes_livro.append(deepcopy(avaliacao))

    if len(avaliacoes_livro) == 0:
        return 1, []

    return 0, avaliacoes_livro


def acessa_avaliacoes_usuario(id_user):
    """Retorna as avaliações feitas por um usuário.

    Retorna:
        (0, avaliações): existem avaliações do usuário.
        (1, []): não existem avaliações do usuário.
    """
    avaliacoes_usuario = []
    for avaliacao in _avaliacoes:
        if avaliacao["id_user"] == id_user:
            avaliacoes_usuario.append(deepcopy(avaliacao))

    if len(avaliacoes_usuario) == 0:
        return 1, []

    return 0, avaliacoes_usuario


def cria_avaliacao(nova_avaliacao):
    """Cadastra ou sobrescreve a avaliação feita por um usuário.

    A avaliação recebida deve conter nota, id_livro e id_user. O identificador
    é gerado pelo próprio módulo.

    Retorna:
        0: avaliação cadastrada ou sobrescrita.
        2: dados inválidos.
    """
    if not _eh_dados_avaliacao_validos(nova_avaliacao):
        return 2

    for indice, avaliacao in enumerate(_avaliacoes):
        if avaliacao["id_user"] == nova_avaliacao["id_user"] and avaliacao["id_livro"] == nova_avaliacao["id_livro"]:
            avaliacao_atualizada = deepcopy(nova_avaliacao)
            avaliacao_atualizada["id_avaliacao"] = avaliacao["id_avaliacao"]
            _avaliacoes[indice] = avaliacao_atualizada
            return 0

    avaliacao_cadastrada = deepcopy(nova_avaliacao)
    avaliacao_cadastrada["id_avaliacao"] = _gera_id_avaliacao()
    _avaliacoes.append(avaliacao_cadastrada)
    return 0


def modifica_avaliacao(id_avaliacao, nova_avaliacao):
    """Modifica uma avaliação já cadastrada.

    A avaliação recebida deve conter nota, id_livro e id_user. O identificador
    informado é preservado.

    Retorna:
        0: avaliação modificada.
        1: avaliação não encontrada.
        2: dados inválidos.
        7: o usuário já possui outra avaliação.
    """
    if not _eh_dados_avaliacao_validos(nova_avaliacao):
        return 2

    for indice, avaliacao in enumerate(_avaliacoes):
        if avaliacao["id_avaliacao"] == id_avaliacao:
            for outra_avaliacao in _avaliacoes:
                if (
                    outra_avaliacao["id_avaliacao"] != id_avaliacao
                    and outra_avaliacao["id_user"] == nova_avaliacao["id_user"]
                ):
                    return 7

            avaliacao_atualizada = deepcopy(nova_avaliacao)
            avaliacao_atualizada["id_avaliacao"] = id_avaliacao
            _avaliacoes[indice] = avaliacao_atualizada
            return 0

    return 1


def deleta_avaliacao(id_avaliacao):
    """Remove uma avaliação cadastrada.

    Retorna:
        0: avaliação removida.
        1: avaliação não encontrada.
    """
    for avaliacao in _avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            _avaliacoes.remove(avaliacao)
            return 0

    return 1


def calculaNotas(id_livro):
    """Calcula a média das avaliações de um livro.

    Retorna:
        (0, nota): média calculada.
        (1, None): livro sem avaliações.
    """
    codigo, avaliacoes_livro = acessa_avaliacoes_livro(id_livro)
    if codigo != 0:
        return codigo, None

    soma = 0
    for avaliacao in avaliacoes_livro:
        soma = soma + avaliacao["nota"]

    return 0, soma / len(avaliacoes_livro)


def carrega_dados():
    """Carrega as avaliações do arquivo para a estrutura encapsulada.

    Retorna:
        0: dados carregados ou arquivo ainda inexistente.
        2: conteúdo do arquivo inválido.
    """
    global _proximo_id
    _avaliacoes.clear()
    _proximo_id = 1

    if not os.path.exists(_ARQUIVO_DADOS):
        return 0

    with open(_ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if isinstance(dados, dict):
        dados = [dados]

    if not isinstance(dados, list):
        return 2

    ids_encontrados = set()
    for avaliacao in dados:
        if not isinstance(avaliacao, dict):
            _avaliacoes.clear()
            return 2

        avaliacao_carregada = deepcopy(avaliacao)
        if "nota" not in avaliacao_carregada:
            avaliacao_carregada["nota"] = avaliacao_carregada.get("id_avaliacao")
            avaliacao_carregada["id_avaliacao"] = _proximo_id

        if not _eh_avaliacao_armazenada_valida(avaliacao_carregada):
            _avaliacoes.clear()
            return 2

        id_avaliacao = avaliacao_carregada["id_avaliacao"]
        if id_avaliacao in ids_encontrados:
            _avaliacoes.clear()
            return 2

        ids_encontrados.add(id_avaliacao)

        substituiu = False
        for indice, avaliacao_atual in enumerate(_avaliacoes):
            if avaliacao_atual["id_user"] == avaliacao_carregada["id_user"]:
                _avaliacoes[indice] = avaliacao_carregada
                substituiu = True
                break

        if not substituiu:
            _avaliacoes.append(avaliacao_carregada)

        if id_avaliacao >= _proximo_id:
            _proximo_id = id_avaliacao + 1

    return 0


def salva_dados():
    """Grava as avaliações encapsuladas no arquivo e retorna 0."""
    os.makedirs(os.path.dirname(_ARQUIVO_DADOS), exist_ok=True)
    with open(_ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(_avaliacoes, arquivo, ensure_ascii=False, indent=2)
    return 0
