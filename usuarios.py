"""Módulo para gerenciamento de usuários."""

from copy import deepcopy
import json
import os


usuarios = []
ARQUIVO_DADOS = os.path.join("dados", "usuarios.json")


def eh_usuario_valido(usuario):
    """Valida se um dicionário tem os campos obrigatórios de usuário."""
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
    """Retorna os dados de um usuário a partir do seu ID."""
    for usuario in usuarios:
        if usuario["id_user"] == id_user or usuario["email"] == id_user:
            return 0, deepcopy(usuario)

    return 1, None


def cria_usuario(novo_usuario):
    """Cadastra um novo usuário no sistema."""
    if not eh_usuario_valido(novo_usuario):
        return 2

    for usuario in usuarios:
        if (
            usuario["id_user"] == novo_usuario["id_user"]
            or usuario["email"] == novo_usuario["email"]
        ):
            return 3

    usuarios.append(deepcopy(novo_usuario))
    return 0


def modifica_usuario(id_user, novo_usuario):
    """Modifica os dados de um usuário já cadastrado."""
    if not eh_usuario_valido(novo_usuario):
        return 2

    usuario_encontrado = None
    for usuario in usuarios:
        if usuario["id_user"] == id_user or usuario["email"] == id_user:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
        return 1

    if novo_usuario["id_user"] != usuario_encontrado["id_user"]:
        return 2

    for usuario in usuarios:
        if usuario is not usuario_encontrado and usuario["email"] == novo_usuario["email"]:
            return 3

    usuario_encontrado["email"] = novo_usuario["email"]
    usuario_encontrado["senha"] = novo_usuario["senha"]
    return 0


def deleta_usuario(id_user):
    """Remove um usuário cadastrado do sistema."""
    for usuario in usuarios:
        if usuario["id_user"] == id_user or usuario["email"] == id_user:
            usuarios.remove(usuario)
            return 0

    return 1


def retorna_usuarios():
    """Retorna uma cópia da lista de usuários cadastrados."""
    return deepcopy(usuarios)


def carrega_dados():
    """Carrega os usuários do arquivo de dados para a estrutura encapsulada."""
    if not os.path.exists(ARQUIVO_DADOS):
        usuarios.clear()
        return 0

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        usuarios.clear()
        return 2

    usuarios.clear()
    usuarios.extend(deepcopy(dados))
    return 0


def salva_dados():
    """Grava os usuários encapsulados no arquivo de dados."""
    os.makedirs(os.path.dirname(ARQUIVO_DADOS), exist_ok=True)
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=2)
    return 0
