"""Módulo para gerenciamento de usuários."""

from copy import deepcopy
import json
import os


_usuarios = []
_ARQUIVO_DADOS = os.path.join("dados", "usuarios.json")

__all__ = [
    "acessa_usuario",
    "cria_usuario",
    "modifica_usuario",
    "deleta_usuario",
    "carrega_dados",
    "salva_dados",
]


def _eh_usuario_valido(usuario):
    """Valida se um dicionário representa um usuário."""
    campos_obrigatorios = ["id_user", "email", "senha"]

    if not isinstance(usuario, dict):
        return False

    if not all(campo in usuario for campo in campos_obrigatorios):
        return False

    for campo in campos_obrigatorios:
        valor = usuario[campo]
        if valor is None:
            return False
        if isinstance(valor, str) and valor.strip() == "":
            return False

    return True


def acessa_usuario(id_user):
    """Retorna os dados de um usuário a partir do ID ou e-mail.

    Retorna:
        (0, usuário): usuário encontrado.
        (1, None): usuário não encontrado.
    """
    for usuario in _usuarios:
        if usuario["id_user"] == id_user or usuario["email"] == id_user:
            return 0, deepcopy(usuario)

    return 1, None


def cria_usuario(novo_usuario):
    """Cadastra um novo usuário.

    Retorna:
        0: usuário cadastrado.
        2: dados inválidos.
        3: ID ou e-mail já cadastrado.
    """
    if not _eh_usuario_valido(novo_usuario):
        return 2

    for usuario in _usuarios:
        if (
            usuario["id_user"] == novo_usuario["id_user"]
            or usuario["email"] == novo_usuario["email"]
        ):
            return 3

    _usuarios.append(deepcopy(novo_usuario))
    return 0


def modifica_usuario(id_user, novo_usuario):
    """Modifica um usuário já cadastrado.

    Retorna:
        0: usuário modificado.
        1: usuário não encontrado.
        2: dados inválidos ou tentativa de alterar o ID.
        3: novo e-mail já cadastrado.
    """
    if not _eh_usuario_valido(novo_usuario):
        return 2

    usuario_encontrado = None
    for usuario in _usuarios:
        if usuario["id_user"] == id_user or usuario["email"] == id_user:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
        return 1

    if novo_usuario["id_user"] != usuario_encontrado["id_user"]:
        return 2

    for usuario in _usuarios:
        if (
            usuario is not usuario_encontrado
            and usuario["email"] == novo_usuario["email"]
        ):
            return 3

    usuario_encontrado["email"] = novo_usuario["email"]
    usuario_encontrado["senha"] = novo_usuario["senha"]
    return 0


def deleta_usuario(id_user):
    """Remove um usuário cadastrado.

    Retorna:
        0: usuário removido.
        1: usuário não encontrado.
    """
    for usuario in _usuarios:
        if usuario["id_user"] == id_user or usuario["email"] == id_user:
            _usuarios.remove(usuario)
            return 0

    return 1


def carrega_dados():
    """Carrega os usuários do arquivo para a estrutura encapsulada.

    Retorna:
        0: dados carregados ou arquivo ainda inexistente.
        2: conteúdo do arquivo inválido.
    """
    _usuarios.clear()

    if not os.path.exists(_ARQUIVO_DADOS):
        return 0

    with open(_ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        return 2

    for usuario in dados:
        if not _eh_usuario_valido(usuario):
            _usuarios.clear()
            return 2
        _usuarios.append(deepcopy(usuario))

    return 0


def salva_dados():
    """Grava os usuários encapsulados no arquivo e retorna 0."""
    os.makedirs(os.path.dirname(_ARQUIVO_DADOS), exist_ok=True)
    with open(_ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(_usuarios, arquivo, ensure_ascii=False, indent=2)
    return 0
