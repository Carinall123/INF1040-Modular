"""Programa principal do sistema de avaliação de livros."""


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


def separa_retorno(retorno):
    """Separa o código e os dados retornados por uma função de acesso."""
    if isinstance(retorno, tuple) and len(retorno) == 2:
        return retorno
    if isinstance(retorno, int):
        return retorno, None
    if retorno is None:
        return 1, None
    return 0, retorno


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
    """Converte um registro retornado por um TAD em texto."""
    if isinstance(registro, dict):
        partes = []
        for chave, valor in registro.items():
            partes.append(f"{chave}: {valor}")
        return " | ".join(partes)
    return str(registro)


def mostra_consulta(retorno, saida):
    """Exibe o resultado retornado por uma função de consulta."""
    codigo, dados = separa_retorno(retorno)
    if codigo != 0:
        saida(MENSAGENS_RETORNO[codigo])
        return codigo

    if isinstance(dados, dict):
        dados = [dados]
    for registro in dados or []:
        saida(formata_registro(registro))
    return 0


def cadastra_usuario(cria_usuario, entrada=input, saida=print):
    """Solicita os dados e chama cria_usuario."""
    try:
        email = le_texto(entrada, "E-mail: ")
        senha = le_texto(entrada, "Senha: ")
    except ValueError as erro:
        saida(str(erro))
        return 2

    novo_usuario = {
        "id_user": email,
        "email": email,
        "senha": senha,
    }
    codigo = cria_usuario(novo_usuario)
    saida(MENSAGENS_RETORNO[codigo])
    return codigo


def autentica_usuario(acessa_usuario, entrada=input, saida=print):
    """Autentica um usuário usando acessa_usuario."""
    try:
        id_user = le_texto(entrada, "E-mail ou ID: ")
        senha = le_texto(entrada, "Senha: ")
    except ValueError as erro:
        saida(str(erro))
        return None

    codigo, usuario = separa_retorno(acessa_usuario(id_user))
    if codigo != 0 or not isinstance(usuario, dict):
        saida("E-mail/ID ou senha incorretos.")
        return None
    if usuario.get("senha") != senha:
        saida("E-mail/ID ou senha incorretos.")
        return None
    return usuario.get("id_user", id_user)


def lista_livros(
    acessa_livros,
    acessa_livros_por_tag,
    entrada=input,
    saida=print,
):
    """Consulta todos os livros ou os livros associados a uma tag."""
    tag = entrada("Tag (Enter para listar todos): ").strip()
    if tag == "":
        return mostra_consulta(acessa_livros(), saida)
    return mostra_consulta(acessa_livros_por_tag(tag), saida)


def consulta_livro(acessa_livro, entrada=input, saida=print):
    """Consulta um livro a partir de seu ID."""
    try:
        id_livro = le_texto(entrada, "ID do livro: ")
    except ValueError as erro:
        saida(str(erro))
        return 2
    return mostra_consulta(acessa_livro(id_livro), saida)


def identifica_livro(registro):
    """Retorna o ID armazenado em um registro de livro."""
    if not isinstance(registro, dict):
        return None
    if "id_livro" in registro:
        return registro["id_livro"]
    return None


def seleciona_livro(acessa_livros, entrada=input, saida=print):
    """Permite selecionar um livro sem digitar manualmente seu ID."""
    codigo, livros = separa_retorno(acessa_livros())
    if codigo != 0:
        saida(MENSAGENS_RETORNO[codigo])
        return codigo, None

    if isinstance(livros, dict):
        livros = [livros]
    livros = list(livros or [])
    if len(livros) == 0:
        saida(MENSAGENS_RETORNO[1])
        return 1, None

    for indice, livro in enumerate(livros, start=1):
        saida(f"{indice} - {formata_registro(livro)}")

    try:
        opcao = int(le_texto(entrada, "Escolha o número do livro: "))
        if opcao < 1:
            raise ValueError
        livro = livros[opcao - 1]
    except (ValueError, IndexError):
        saida("Opção de livro inválida.")
        return 2, None

    id_livro = identifica_livro(livro)
    if id_livro is None:
        saida("Dados inválidos.")
        return 2, None
    return 0, id_livro


def avalia_livro(
    acessa_livros,
    cria_avaliacao,
    id_user,
    entrada=input,
    saida=print,
):
    """Seleciona um livro e chama cria_avaliacao."""
    codigo, id_livro = seleciona_livro(acessa_livros, entrada, saida)
    if codigo != 0:
        return codigo

    try:
        nota = le_nota(entrada)
    except ValueError as erro:
        saida(str(erro))
        return 6

    nova_avaliacao = {
        "id_avaliacao": nota,
        "id_livro": id_livro,
        "id_user": id_user,
    }
    codigo = cria_avaliacao(nova_avaliacao)
    saida(MENSAGENS_RETORNO[codigo])
    return codigo


def consulta_avaliacoes_livro(
    acessa_avaliacoes_livro,
    entrada=input,
    saida=print,
):
    """Consulta as avaliações associadas a um livro."""
    try:
        id_livro = le_texto(entrada, "ID do livro: ")
    except ValueError as erro:
        saida(str(erro))
        return 2
    return mostra_consulta(acessa_avaliacoes_livro(id_livro), saida)


def consulta_nota_livro(calculaNotas, entrada=input, saida=print):
    """Consulta a nota calculada para um livro."""
    try:
        id_livro = le_texto(entrada, "ID do livro: ")
    except ValueError as erro:
        saida(str(erro))
        return 2

    codigo, nota = separa_retorno(calculaNotas(id_livro))
    if codigo == 0:
        saida(f"Nota do livro: {nota}")
    else:
        saida(MENSAGENS_RETORNO[codigo])
    return codigo


def menu_usuario(funcoes, id_user, entrada=input, saida=print):
    """Executa as funcionalidades disponíveis após a autenticação."""
    while True:
        saida(
            "\n1 - Listar livros\n"
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
            lista_livros(
                funcoes["acessa_livros"],
                funcoes["acessa_livros_por_tag"],
                entrada,
                saida,
            )
        elif opcao == "2":
            consulta_livro(funcoes["acessa_livro"], entrada, saida)
        elif opcao == "3":
            avalia_livro(
                funcoes["acessa_livros"],
                funcoes["cria_avaliacao"],
                id_user,
                entrada,
                saida,
            )
        elif opcao == "4":
            consulta_avaliacoes_livro(
                funcoes["acessa_avaliacoes_livro"],
                entrada,
                saida,
            )
        elif opcao == "5":
            consulta_nota_livro(funcoes["calculaNotas"], entrada, saida)
        else:
            saida("Opção inválida.")


def executa_aplicacao(funcoes, entrada=input, saida=print):
    """Carrega os dados, executa os menus e salva os dados ao encerrar."""
    funcoes["carrega_usuarios"]()
    funcoes["carrega_livros"]()
    funcoes["carrega_avaliacoes"]()

    try:
        while True:
            saida("\n1 - Cadastrar usuário\n2 - Entrar\n0 - Encerrar")
            opcao = entrada("Opção: ").strip()
            if opcao == "0":
                return
            if opcao == "1":
                cadastra_usuario(funcoes["cria_usuario"], entrada, saida)
            elif opcao == "2":
                id_user = autentica_usuario(
                    funcoes["acessa_usuario"],
                    entrada,
                    saida,
                )
                if id_user is not None:
                    menu_usuario(funcoes, id_user, entrada, saida)
            else:
                saida("Opção inválida.")
    finally:
        funcoes["salva_usuarios"]()
        funcoes["salva_livros"]()
        funcoes["salva_avaliacoes"]()


def main():
    """Importa os TADs e inicia a aplicação."""
    import avaliacoes
    import livro
    import usuarios

    funcoes = {
        "carrega_usuarios": usuarios.carrega_dados,
        "salva_usuarios": usuarios.salva_dados,
        "acessa_usuario": usuarios.acessa_usuario,
        "cria_usuario": usuarios.cria_usuario,
        "carrega_livros": livro.carrega_dados,
        "salva_livros": livro.salva_dados,
        "acessa_livro": livro.acessa_livro,
        "acessa_livros": livro.acessa_livros,
        "acessa_livros_por_tag": livro.acessa_livros_por_tag,
        "carrega_avaliacoes": avaliacoes.carrega_dados,
        "salva_avaliacoes": avaliacoes.salva_dados,
        "cria_avaliacao": avaliacoes.cria_avaliacao,
        "acessa_avaliacoes_livro": avaliacoes.acessa_avaliacoes_livro,
        "calculaNotas": avaliacoes.calculaNotas,
    }
    executa_aplicacao(funcoes)


if __name__ == "__main__":
    main()
