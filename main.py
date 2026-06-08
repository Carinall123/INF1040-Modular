"""Programa principal do sistema de avaliação de livros."""

import time

import avaliacoes
import livro
import usuarios


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
    usuarios.carrega_dados()
    livro.carrega_dados()
    avaliacoes.carrega_dados()
    sincroniza_referencias_avaliacoes()
    return 0


def salva_dados():
    """Salva os dados encapsulados nos módulos da aplicação."""
    usuarios.salva_dados()
    livro.salva_dados()
    avaliacoes.salva_dados()
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


def sincroniza_referencias_avaliacoes():
    """Atualiza os IDs válidos de livros e usuários no módulo de avaliações."""
    avaliacoes.define_livros(livro.retorna_livros())
    avaliacoes.define_usuarios(usuarios.retorna_usuarios())
    return 0


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
    codigo = usuarios.cria_usuario(novo_usuario)
    sincroniza_referencias_avaliacoes()
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

    retorno = usuarios.acessa_usuario(id_user)
    if isinstance(retorno, tuple):
        codigo, usuario = retorno
    else:
        codigo, usuario = retorno, None

    if codigo != 0 or not isinstance(usuario, dict):
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
        codigo = livro.acessa_livros()
        livros = livro.retorna_livros()
    else:
        codigo = livro.acessa_livros_por_tag(tag)
        livros = []
        if codigo == 0:
            for livro_atual in livro.retorna_livros():
                if tag in livro_atual["tags"]:
                    livros.append(livro_atual)

    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo

    saida("\n=== Livros ===")
    for livro_atual in livros:
        saida(formata_registro(livro_atual))
    pausa()
    return 0


def consulta_livro(entrada=input, saida=print):
    """Consulta e exibe um livro a partir de seu ID."""
    try:
        id_livro = int(le_texto(entrada, "ID do livro: "))
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    codigo = livro.acessa_livro(id_livro)
    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo

    for livro_atual in livro.retorna_livros():
        if livro_atual["id_livro"] == id_livro:
            saida("\n=== Livro encontrado ===")
            saida(formata_registro(livro_atual))
            pausa()
            return 0

    exibe_retorno(1, saida)
    return 1


def seleciona_livro(entrada=input, saida=print):
    """Permite escolher um livro pelo ID exibido no terminal."""
    codigo = livro.acessa_livros()
    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo, None

    livros = livro.retorna_livros()
    saida("\n=== Escolha um livro ===")
    for livro_atual in livros:
        saida(
            f"ID: {livro_atual['id_livro']} | "
            f"{livro_atual['nome']} | "
            f"{livro_atual['autor']}"
        )

    try:
        id_livro = int(le_texto(entrada, "Digite o ID do livro: "))
        if id_livro < 1:
            raise ValueError
    except ValueError:
        saida("\n>>> ID de livro inválido.\n")
        pausa()
        return 2, None

    codigo = livro.acessa_livro(id_livro)
    if codigo != 0:
        exibe_retorno(codigo, saida)
        return codigo, None

    return 0, id_livro


def avalia_livro(id_user, entrada=input, saida=print):
    """Seleciona um livro e cadastra uma avaliação."""
    sincroniza_referencias_avaliacoes()
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
        "id_avaliacao": nota,
        "id_livro": id_livro,
        "id_user": id_user,
    }
    codigo = avaliacoes.cria_avaliacao(nova_avaliacao)
    exibe_retorno(codigo, saida)
    return codigo


def consulta_avaliacoes_livro(entrada=input, saida=print):
    """Consulta as avaliações associadas a um livro."""
    sincroniza_referencias_avaliacoes()
    try:
        id_livro = int(le_texto(entrada, "ID do livro: "))
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    codigo, avaliacoes_livro = avaliacoes.acessa_avaliacoes_livro(id_livro)
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
    sincroniza_referencias_avaliacoes()
    try:
        id_livro = int(le_texto(entrada, "ID do livro: "))
    except ValueError as erro:
        saida(f"\n>>> {erro}\n")
        pausa()
        return 2

    codigo, nota = avaliacoes.calculaNotas(id_livro)
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
