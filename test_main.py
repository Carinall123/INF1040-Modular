"""Testes funcionais do módulo main com pytest."""

import main


def entrada_com(*respostas):
    """Retorna uma função de entrada com respostas predeterminadas."""
    respostas = iter(respostas)

    def entrada(_mensagem):
        return next(respostas)

    return entrada


def saida_em(lista):
    """Retorna uma função que armazena as mensagens exibidas."""
    def saida(mensagem):
        lista.append(mensagem)

    return saida


def test_cadastra_usuario_com_sucesso():
    chamadas = []
    mensagens = []

    def cria_usuario(novo_usuario):
        chamadas.append(novo_usuario)
        return 0

    codigo = main.cadastra_usuario(
        cria_usuario,
        entrada_com("leitor@email.com", "segredo"),
        saida_em(mensagens),
    )

    assert codigo == 0
    assert chamadas == [
        {
            "id_user": "leitor@email.com",
            "email": "leitor@email.com",
            "senha": "segredo",
        }
    ]


def test_cadastra_usuario_com_dados_invalidos():
    chamadas = []

    def cria_usuario(novo_usuario):
        chamadas.append(novo_usuario)
        return 0

    codigo = main.cadastra_usuario(
        cria_usuario,
        entrada_com("", "segredo"),
        lambda _mensagem: None,
    )

    assert codigo == 2
    assert chamadas == []


def test_autentica_usuario_com_sucesso():
    def acessa_usuario(id_user):
        assert id_user == "u1"
        return 0, {"id_user": "u1", "senha": "segredo"}

    id_user = main.autentica_usuario(
        acessa_usuario,
        entrada_com("u1", "segredo"),
        lambda _mensagem: None,
    )

    assert id_user == "u1"


def test_autenticacao_rejeita_senha_incorreta():
    def acessa_usuario(_id_user):
        return 0, {"id_user": "u1", "senha": "correta"}

    id_user = main.autentica_usuario(
        acessa_usuario,
        entrada_com("u1", "errada"),
        lambda _mensagem: None,
    )

    assert id_user is None


def test_menu_encaminha_consulta_de_todos_os_livros():
    mensagens = []

    def acessa_livros():
        return 0, [{"id_livro": "l1", "nome": "Livro"}]

    def acessa_livros_por_tag(_tag):
        raise AssertionError("A busca por tag não deveria ser chamada")

    codigo = main.lista_livros(
        acessa_livros,
        acessa_livros_por_tag,
        entrada_com(""),
        saida_em(mensagens),
    )

    assert codigo == 0
    assert "nome: Livro" in mensagens[0]


def test_menu_encaminha_consulta_de_livros_por_tag():
    tags = []

    def acessa_livros():
        raise AssertionError("A busca geral não deveria ser chamada")

    def acessa_livros_por_tag(tag):
        tags.append(tag)
        return 0, [{"id_livro": "l1", "tags": ["ficção"]}]

    codigo = main.lista_livros(
        acessa_livros,
        acessa_livros_por_tag,
        entrada_com("ficção"),
        lambda _mensagem: None,
    )

    assert codigo == 0
    assert tags == ["ficção"]


def test_menu_exibe_retorno_de_livro_inexistente():
    mensagens = []

    def acessa_livro(id_livro):
        assert id_livro == "inexistente"
        return 1, None

    codigo = main.consulta_livro(
        acessa_livro,
        entrada_com("inexistente"),
        saida_em(mensagens),
    )

    assert codigo == 1
    assert mensagens[-1] == "Registro não encontrado."


def test_cria_avaliacao_com_livro_selecionado():
    avaliacoes_criadas = []

    def acessa_livros():
        return 0, [
            {"id_livro": "l1", "nome": "Primeiro"},
            {"id_livro": "l2", "nome": "Segundo"},
        ]

    def cria_avaliacao(nova_avaliacao):
        avaliacoes_criadas.append(nova_avaliacao)
        return 0

    codigo = main.avalia_livro(
        acessa_livros,
        cria_avaliacao,
        "u1",
        entrada_com("2", "5"),
        lambda _mensagem: None,
    )

    assert codigo == 0
    assert avaliacoes_criadas == [
        {"id_livro": "l2", "id_user": "u1", "nota": 5}
    ]


def test_cria_avaliacao_rejeita_nota_invalida():
    avaliacoes_criadas = []

    def acessa_livros():
        return 0, [{"id_livro": "l1", "nome": "Livro"}]

    def cria_avaliacao(nova_avaliacao):
        avaliacoes_criadas.append(nova_avaliacao)
        return 0

    codigo = main.avalia_livro(
        acessa_livros,
        cria_avaliacao,
        "u1",
        entrada_com("1", "6"),
        lambda _mensagem: None,
    )

    assert codigo == 6
    assert avaliacoes_criadas == []


def test_menu_encaminha_consulta_de_avaliacoes_do_livro():
    livros_consultados = []

    def acessa_avaliacoes_livro(id_livro):
        livros_consultados.append(id_livro)
        return 0, [{"id_avaliacao": "a1", "nota": 5}]

    codigo = main.consulta_avaliacoes_livro(
        acessa_avaliacoes_livro,
        entrada_com("l1"),
        lambda _mensagem: None,
    )

    assert codigo == 0
    assert livros_consultados == ["l1"]


def test_menu_exibe_nota_calculada_do_livro():
    mensagens = []

    def calcula_notas(id_livro):
        assert id_livro == "l1"
        return 0, 4.25

    codigo = main.consulta_nota_livro(
        calcula_notas,
        entrada_com("l1"),
        saida_em(mensagens),
    )

    assert codigo == 0
    assert mensagens == ["Nota do livro: 4.25"]


def test_aplicacao_carrega_no_inicio_e_salva_no_fim():
    eventos = []

    def registra(evento):
        def funcao():
            eventos.append(evento)
            return 0

        return funcao

    funcoes = {
        "carrega_usuarios": registra("carrega usuários"),
        "carrega_livros": registra("carrega livros"),
        "carrega_avaliacoes": registra("carrega avaliações"),
        "salva_usuarios": registra("salva usuários"),
        "salva_livros": registra("salva livros"),
        "salva_avaliacoes": registra("salva avaliações"),
    }

    main.executa_aplicacao(
        funcoes,
        entrada_com("0"),
        lambda _mensagem: None,
    )

    assert eventos == [
        "carrega usuários",
        "carrega livros",
        "carrega avaliações",
        "salva usuários",
        "salva livros",
        "salva avaliações",
    ]


def test_aplicacao_salva_dados_mesmo_se_ocorrer_erro():
    eventos = []

    def registra(evento):
        def funcao():
            eventos.append(evento)
            return 0

        return funcao

    def entrada_com_erro(_mensagem):
        raise RuntimeError("erro durante a execução")

    funcoes = {
        "carrega_usuarios": registra("carrega usuários"),
        "carrega_livros": registra("carrega livros"),
        "carrega_avaliacoes": registra("carrega avaliações"),
        "salva_usuarios": registra("salva usuários"),
        "salva_livros": registra("salva livros"),
        "salva_avaliacoes": registra("salva avaliações"),
    }

    try:
        main.executa_aplicacao(
            funcoes,
            entrada_com_erro,
            lambda _mensagem: None,
        )
    except RuntimeError:
        pass

    assert eventos[-3:] == [
        "salva usuários",
        "salva livros",
        "salva avaliações",
    ]
