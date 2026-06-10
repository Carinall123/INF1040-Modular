"""Programa principal do sistema de avaliação de livros."""

import time

from avaliacoes import (
    acessa_avaliacoes_livro,
    calculaNotas,
    carrega_dados as carrega_avaliacoes,
    cria_avaliacao,
    salva_dados as salva_avaliacoes,
)
from livro import (
    acessa_livro,
    acessa_livros,
    acessa_livros_por_tag,
    carrega_dados as carrega_livros,
    salva_dados as salva_livros,
)
from usuarios import (
    acessa_usuario,
    carrega_dados as carrega_usuarios,
    cria_usuario,
    salva_dados as salva_usuarios,
)


TEMPO_PAUSA = 1

MENSAGENS_RETORNO = {
    0: "Operação realizada com sucesso.",
    1: "Registro não encontrado.",
    2: "Dados inválidos.",
    3: "Identificador já cadastrado.",
    4: "Livro inexistente.",
    5: "Usuário inexistente.",
    6: "Nota inválida. Informe uma nota entre 0 e 5.",
    7: "Operação não permitida.",
}


def pausa():
    """Pausa a interface para melhorar a leitura das mensagens."""
    time.sleep(TEMPO_PAUSA)


def exibe_retorno(codigo, saida=print):
    """Exibe uma mensagem de retorno padronizada e aguarda um segundo."""
    saida(f"\n>>> {MENSAGENS_RETORNO[codigo]}\n")
    pausa()


def carrega_dados():
    """Carrega os dados encapsulados nos módulos da aplicação."""
    carrega_usuarios()
    carrega_livros()
    carrega_avaliacoes()
    return 0


def salva_dados():
    """Salva os dados encapsulados nos módulos da aplicação."""
    salva_usuarios()
    salva_livros()
    salva_avaliacoes()
    return 0


def le_texto(entrada, mensagem):
    """Lê um campo textual obrigatório."""
    valor = entrada(mensagem).strip()
    if valor == "":
        raise ValueError("O campo não pode ficar vazio.")
    return valor


def le_nota(entrada):
    """Lê uma nota numérica entre 0 e 5."""
    texto = le_texto(entrada, "Nota (0 a 5): ")
    try:
        nota = float(texto)
    except ValueError as erro:
        raise ValueError("A nota deve ser numérica.") from erro

    if nota < 0 or nota > 5:
        raise ValueError("A nota deve estar entre 0 e 5.")

    if nota.is_integer():
        return int(nota)
    return nota


def formata_registro(registro):
    """Converte um dicionário de dados em texto para exibição."""
    partes = []
    for chave, valor in registro.items():
        partes.append(f"{chave}: {valor}")
    return " | ".join(partes)


def cadastra_usuario(entrada=input, saida=print):
    """Solicita os dados de usuário e chama cria_usuario."""
    try:
        email = le_texto(entrada, "E-mail: ")
        senha = le_texto(entrada, "Senha: ")
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    novo_usuario = {
        "id_user": email,
        "email": email,
        "senha": senha,
    }
    codigo = cria_usuario(novo_usuario)
    exibe_retorno(codigo, saida)
    return codigo


def autentica_usuario(entrada=input, saida=print):
    """Autentica um usuário usando acessa_usuario."""
    try:
        id_user = le_texto(entrada, "E-mail: ")
        senha = le_texto(entrada, "Senha: ")
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return None

    codigo, usuario = acessa_usuario(id_user)
    if codigo != 0:
        saida("\n>>> E-mail ou senha incorretos.\n")
        pausa()
        return None

    if usuario.get("senha") != senha:
        saida("\n>>> E-mail ou senha incorretos.\n")
        pausa()
        return None

    saida("\n>>> Login realizado com sucesso.\n")
    pausa()
    return usuario.get("id_user", id_user)


def lista_livros(entrada=input, saida=print):
    """Lista todos os livros ou os livros associados a uma tag."""
    tag = entrada("Tag (Enter para listar todos): ").strip()
    if tag == "":
        codigo, livros = acessa_livros()
    else:
        codigo, livros = acessa_livros_por_tag(tag)

    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo

    saida("\n=== Livros ===")
    for livro_atual in livros:
        saida(formata_registro(livro_atual))
    pausa()
    return 0


def consulta_livro(entrada=input, saida=print):
    """Consulta e exibe um livro a partir de seu nome."""
    try:
        nome_livro = le_texto(entrada, "Nome do livro: ")
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    codigo, livro_encontrado = acessa_livro(nome_livro)
    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo

    saida("\n=== Livro encontrado ===")
    saida(formata_registro(livro_encontrado))
    pausa()
    return 0


def seleciona_livro(entrada=input, saida=print):
    """Permite escolher um livro pelo nome exibido no terminal."""
    codigo, livros = acessa_livros()
    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo, None

    saida("\n=== Escolha um livro ===")
    for livro_atual in livros:
        saida(
            f"ID: {livro_atual['id_livro']} | "
            f"Livro: {livro_atual['nome']} | "
            f"Autor: {livro_atual['autor']}"
        )

    try:
        nome_livro = le_texto(entrada, "Digite o nome do livro: ")
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2, None

    codigo, livro_encontrado = acessa_livro(nome_livro)
    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo, None

    return 0, livro_encontrado["id_livro"]


def avalia_livro(id_user, entrada=input, saida=print):
    """Seleciona um livro e cadastra uma avaliação."""
    codigo, _usuario = acessa_usuario(id_user)
    if codigo != 0:
        exibe_retorno(5, saida)
        return 5

    codigo, id_livro = seleciona_livro(entrada, saida)
    if codigo != 0:
        return codigo

    try:
        nota = le_nota(entrada)
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 6

    nova_avaliacao = {
        "nota": nota,
        "id_livro": id_livro,
        "id_user": id_user,
    }
    codigo = cria_avaliacao(nova_avaliacao)
    exibe_retorno(codigo, saida)
    return codigo


def consulta_avaliacoes_livro(entrada=input, saida=print):
    """Consulta as avaliações associadas a um livro."""
    try:
        nome_livro = le_texto(entrada, "Nome do livro: ")
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    codigo_livro, livro_encontrado = acessa_livro(nome_livro)
    if codigo_livro != 0:
        exibe_retorno(4, saida)
        return 4

    id_livro = livro_encontrado["id_livro"]
    codigo, avaliacoes_livro = acessa_avaliacoes_livro(id_livro)
    if codigo == 0:
        saida("\n=== Avaliações do livro ===")
        for avaliacao in avaliacoes_livro:
            saida(formata_registro(avaliacao))
        pausa()
        return 0

    exibe_retorno(codigo, saida)
    return codigo


def consulta_nota_livro(entrada=input, saida=print):
    """Consulta a nota calculada para um livro."""
    try:
        nome_livro = le_texto(entrada, "Nome do livro: ")
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    codigo_livro, livro_encontrado = acessa_livro(nome_livro)
    if codigo_livro != 0:
        exibe_retorno(4, saida)
        return 4

    id_livro = livro_encontrado["id_livro"]
    codigo, nota = calculaNotas(id_livro)
    if codigo == 0:
        saida(f"\n>>> Nota do livro: {nota:.2f}\n")
        pausa()
        return 0

    exibe_retorno(codigo, saida)
    return codigo


def menu_usuario(id_user, entrada=input, saida=print):
    """Executa o menu disponível após autenticação."""
    while True:
        saida(
            "\n1 - Listar livros por tag\n"
            "2 - Consultar livro\n"
            "3 - Avaliar livro\n"
            "4 - Consultar avaliações de um livro\n"
            "5 - Consultar nota de um livro\n"
            "0 - Sair da conta"
        )
        opcao = entrada("Opção: ").strip()

        if opcao == "0":
            return
        if opcao == "1":
            lista_livros(entrada, saida)
        elif opcao == "2":
            consulta_livro(entrada, saida)
        elif opcao == "3":
            avalia_livro(id_user, entrada, saida)
        elif opcao == "4":
            consulta_avaliacoes_livro(entrada, saida)
        elif opcao == "5":
            consulta_nota_livro(entrada, saida)
        else:
            saida("\n>>> Opção inválida.\n")
            pausa()


def executa_aplicacao(entrada=input, saida=print):
    """Executa a aplicação pelo terminal."""
    carrega_dados()

    try:
        while True:
            saida("\n1 - Cadastrar usuário\n2 - Entrar\n0 - Encerrar")
            opcao = entrada("Opção: ").strip()

            if opcao == "0":
                return
            if opcao == "1":
                cadastra_usuario(entrada, saida)
            elif opcao == "2":
                id_user = autentica_usuario(entrada, saida)
                if id_user is not None:
                    menu_usuario(id_user, entrada, saida)
            else:
                saida("\n>>> Opção inválida.\n")
                pausa()
    finally:
        salva_dados()


def main():
    """Inicia a aplicação."""
    executa_aplicacao()


if __name__ == "__main__":
    main()
