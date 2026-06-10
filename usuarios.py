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
    campos_obrigatorios = ["email", "senha"]

    if not isinstance(usuario, dict):
        return False

    if not all(campo in usuario for campo in campos_obrigatorios):
        return False

    if not isinstance(usuario["email"], str) or usuario["email"].strip() == "":
        return False

    if not isinstance(usuario["senha"], str) or usuario["senha"].strip() == "":
        return False

    return True


def acessa_usuario(email):
    """Consulta um usuário por seu e-mail.

    Parâmetros:
        email: E-mail usado para localizar o usuário.

    Retorna:
        (0, usuario): Usuário encontrado. O registro retornado é uma cópia.
        (1, None): Nenhum usuário possui o e-mail informado.

    Efeito no TAD:
        Não altera os usuários armazenados.
    """
    for usuario in _usuarios:
        if usuario["email"] == email:
            return 0, deepcopy(usuario)

    return 1, None


def cria_usuario(novo_usuario):
    """Cadastra um usuário.

    Parâmetros:
        novo_usuario: Dicionário completo com ``email`` e ``senha``. Nenhum
            campo pode ser ``None`` e campos textuais não podem ser vazios ou
            conter somente espaços.

    Retorna:
        0: Usuário cadastrado.
        2: Registro ausente, incompleto ou com algum campo inválido.
        3: Já existe usuário com o mesmo ``email``.

    Efeito no TAD:
        Em caso de sucesso, armazena uma cópia de ``novo_usuario``.
    """
    if not _eh_usuario_valido(novo_usuario):
        return 2

    for usuario in _usuarios:
        if usuario["email"] == novo_usuario["email"]:
            return 3

    usuario_cadastrado = {
        "email": novo_usuario["email"],
        "senha": novo_usuario["senha"],
    }
    _usuarios.append(usuario_cadastrado)
    return 0


def modifica_usuario(email, novo_usuario):
    """Substitui os dados de um usuário preservando seu e-mail.

    Parâmetros:
        email: E-mail usado para localizar o usuário.
        novo_usuario: Registro completo com os valores de ``email`` e
            ``senha``.

    Retorna:
        0: Usuário modificado.
        1: Usuário não encontrado.
        2: Novos dados inválidos ou tentativa de alterar ``email``.

    Efeito no TAD:
        Em caso de sucesso, altera ``senha``. O campo ``email`` permanece
        inalterado por ser a chave primária.
    """
    if not _eh_usuario_valido(novo_usuario):
        return 2

    usuario_encontrado = None
    for usuario in _usuarios:
        if usuario["email"] == email:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
        return 1

    if novo_usuario["email"] != usuario_encontrado["email"]:
        return 2

    usuario_encontrado["senha"] = novo_usuario["senha"]
    return 0


def deleta_usuario(email):
    """Remove um usuário por seu e-mail.

    Parâmetros:
        email: E-mail usado para localizar o usuário.

    Retorna:
        0: Usuário removido.
        1: Usuário não encontrado.

    Efeito no TAD:
        Remove o registro encontrado.
    """
    for usuario in _usuarios:
        if usuario["email"] == email:
            _usuarios.remove(usuario)
            return 0

    return 1


def carrega_dados():
    """Inicializa o TAD com o conteúdo de ``dados/usuarios.json``.

    Parâmetros:
        Nenhum.

    Retorna:
        0: Arquivo carregado ou arquivo ainda inexistente.
        2: O conteúdo JSON não é uma lista de usuários válidos.

    Efeito no TAD:
        Limpa os dados atuais antes da leitura. Se o conteúdo estrutural for
        inválido, o TAD permanece vazio.

    Exceções:
        Erros de leitura e JSON malformado são propagados ao módulo cliente.
    """
    _usuarios.clear()

    if not os.path.exists(_ARQUIVO_DADOS):
        return 0

    with open(_ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        return 2

    emails_encontrados = set()
    for usuario in dados:
        if not isinstance(usuario, dict):
            _usuarios.clear()
            return 2

        if not _eh_usuario_valido(usuario):
            _usuarios.clear()
            return 2

        email = usuario["email"]
        if email in emails_encontrados:
            _usuarios.clear()
            return 2

        emails_encontrados.add(email)
        _usuarios.append({
            "email": usuario["email"],
            "senha": usuario["senha"],
        })

    return 0


def salva_dados():
    """Persiste os usuários encapsulados em ``dados/usuarios.json``.

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
        json.dump(_usuarios, arquivo, ensure_ascii=False, indent=2)
    return 0
