"""Módulo para gerenciamento de avaliações de livros."""

from copy import deepcopy
import json
import os


# Convenção dos Códigos de Retorno
# 0: operação realizada com sucesso
# 1: registro não encontrado
# 2: dados inválidos
# 3: identificador já cadastrado
# 4: livro inexistente
# 5: usuário inexistente
# 6: nota inválida
# 7: operação não permitida

ARQUIVO_DADOS = os.path.join("dados", "avaliacoes.json")

avaliacoes = []
livros = set()
usuarios = set()


def define_livros(novos_livros):
    """Define os IDs dos livros existentes para validação das avaliações."""
    livros.clear()
    for livro in novos_livros:
        if isinstance(livro, dict) and "id_livro" in livro:
            livros.add(livro["id_livro"])
        else:
            livros.add(livro)
    return 0


def define_usuarios(novos_usuarios):
    """Define os IDs dos usuários existentes para validação das avaliações."""
    usuarios.clear()
    for usuario in novos_usuarios:
        if isinstance(usuario, dict) and "id_user" in usuario:
            usuarios.add(usuario["id_user"])
        else:
            usuarios.add(usuario)
    return 0


def eh_avaliacao_valida(avaliacao):
    """Valida se uma avaliação possui livro, usuário e nota."""
    campos_obrigatorios = ["id_avaliacao", "id_livro", "id_user"]

    if not isinstance(avaliacao, dict):
        return False

    if not all(campo in avaliacao for campo in campos_obrigatorios):
        return False

    return isinstance(avaliacao["id_avaliacao"], (int, float))


def acessa_avaliacao(id_avaliacao):
    """Retorna uma avaliação a partir do seu ID."""
    for avaliacao in avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            return 0, deepcopy(avaliacao)

    return 1, None


def acessa_avaliacoes_livro(id_livro):
    """Retorna todas as avaliações associadas a um livro."""
    if id_livro not in livros:
        return 4, []

    avaliacoes_livro = []
    for avaliacao in avaliacoes:
        if avaliacao["id_livro"] == id_livro:
            avaliacoes_livro.append(deepcopy(avaliacao))

    if len(avaliacoes_livro) == 0:
        return 1, []

    return 0, avaliacoes_livro


def acessa_avaliacoes_usuario(id_user):
    """Retorna todas as avaliações feitas por um usuário."""
    if id_user not in usuarios:
        return 5, []

    avaliacoes_usuario = []
    for avaliacao in avaliacoes:
        if avaliacao["id_user"] == id_user:
            avaliacoes_usuario.append(deepcopy(avaliacao))

    if len(avaliacoes_usuario) == 0:
        return 1, []

    return 0, avaliacoes_usuario


def cria_avaliacao(nova_avaliacao):
    """Cadastra uma nova avaliação para um livro."""
    if not eh_avaliacao_valida(nova_avaliacao):
        return 2

    if nova_avaliacao["id_livro"] not in livros:
        return 4

    if nova_avaliacao["id_user"] not in usuarios:
        return 5

    if nova_avaliacao["id_avaliacao"] < 0 or nova_avaliacao["id_avaliacao"] > 5:
        return 6

    for avaliacao in avaliacoes:
        if avaliacao["id_user"] == nova_avaliacao["id_user"] and avaliacao["id_livro"] == nova_avaliacao["id_livro"]:
            avaliacao["id_avaliacao"] = nova_avaliacao["id_avaliacao"]
            avaliacao["id_livro"] = nova_avaliacao["id_livro"]
            return 0

    avaliacoes.append(deepcopy(nova_avaliacao))
    return 0


def modifica_avaliacao(id_avaliacao, nova_avaliacao):
    """Modifica uma avaliação já cadastrada."""
    if not eh_avaliacao_valida(nova_avaliacao):
        return 2

    if nova_avaliacao["id_avaliacao"] < 0 or nova_avaliacao["id_avaliacao"] > 5:
        return 2

    for avaliacao in avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            avaliacao["id_avaliacao"] = nova_avaliacao["id_avaliacao"]
            avaliacao["id_livro"] = nova_avaliacao["id_livro"]
            avaliacao["id_user"] = nova_avaliacao["id_user"]
            return 0

    return 1


def deleta_avaliacao(id_avaliacao):
    """Remove uma avaliação cadastrada."""
    for avaliacao in avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            avaliacoes.remove(avaliacao)
            return 0

    return 1


def calculaNotas(id_livro):
    """Calcula a nota de um livro a partir das avaliações cadastradas."""
    codigo, avaliacoes_livro = acessa_avaliacoes_livro(id_livro)
    if codigo != 0:
        return codigo, None

    soma = 0
    for avaliacao in avaliacoes_livro:
        soma = soma + avaliacao["id_avaliacao"]

    return 0, soma / len(avaliacoes_livro)


def carrega_dados():
    """Carrega os dados de avaliações do arquivo do módulo."""
    if not os.path.exists(ARQUIVO_DADOS):
        avaliacoes.clear()
        return 0

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    avaliacoes.clear()
    if isinstance(dados, list):
        for avaliacao_nova in dados:
            if not isinstance(avaliacao_nova, dict) or "id_user" not in avaliacao_nova:
                continue

            substituiu = False
            for indice, avaliacao in enumerate(avaliacoes):
                if avaliacao["id_user"] == avaliacao_nova["id_user"]:
                    avaliacoes[indice] = deepcopy(avaliacao_nova)
                    substituiu = True
                    break

            if not substituiu:
                avaliacoes.append(deepcopy(avaliacao_nova))
        return 0

    if isinstance(dados, dict):
        avaliacoes.append(deepcopy(dados))
        return 0

    return 2


def salva_dados():
    """Grava os dados de avaliações no arquivo do módulo."""
    os.makedirs(os.path.dirname(ARQUIVO_DADOS), exist_ok=True)
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(avaliacoes, arquivo, ensure_ascii=False, indent=2)
    return 0
