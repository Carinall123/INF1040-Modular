"""Testes automatizados do módulo main com unittest."""

import unittest

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


class TestMain(unittest.TestCase):
    """Testes da interação do main com as funções de acesso dos TADs."""

    def test_01_cadastra_usuario_com_sucesso(self):
        print("Caso de Teste 01 - Cadastrar usuário com sucesso")
        chamadas = []

        def cria_usuario(novo_usuario):
            chamadas.append(novo_usuario)
            return 0

        codigo = main.cadastra_usuario(
            cria_usuario,
            entrada_com("leitor@email.com", "segredo"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 0)
        self.assertEqual(
            chamadas,
            [
                {
                    "id_user": "leitor@email.com",
                    "email": "leitor@email.com",
                    "senha": "segredo",
                }
            ],
        )

    def test_02_cadastra_usuario_com_dados_invalidos(self):
        print("Caso de Teste 02 - Impedir cadastro com dados inválidos")
        chamadas = []

        def cria_usuario(novo_usuario):
            chamadas.append(novo_usuario)
            return 0

        codigo = main.cadastra_usuario(
            cria_usuario,
            entrada_com("", "segredo"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 2)
        self.assertEqual(chamadas, [])

    def test_03_autentica_usuario_com_sucesso(self):
        print("Caso de Teste 03 - Autenticar usuário com sucesso")

        def acessa_usuario(id_user):
            self.assertEqual(id_user, "u1")
            return 0, {"id_user": "u1", "senha": "segredo"}

        id_user = main.autentica_usuario(
            acessa_usuario,
            entrada_com("u1", "segredo"),
            lambda _mensagem: None,
        )

        self.assertEqual(id_user, "u1")

    def test_04_autenticacao_rejeita_senha_incorreta(self):
        print("Caso de Teste 04 - Rejeitar autenticação com senha incorreta")

        def acessa_usuario(_id_user):
            return 0, {"id_user": "u1", "senha": "correta"}

        id_user = main.autentica_usuario(
            acessa_usuario,
            entrada_com("u1", "errada"),
            lambda _mensagem: None,
        )

        self.assertIsNone(id_user)

    def test_05_menu_encaminha_consulta_de_todos_os_livros(self):
        print("Caso de Teste 05 - Consultar todos os livros")
        mensagens = []

        def acessa_livros():
            return 0, [{"id_livro": "l1", "nome": "Livro"}]

        def acessa_livros_por_tag(_tag):
            self.fail("A busca por tag não deveria ser chamada")

        codigo = main.lista_livros(
            acessa_livros,
            acessa_livros_por_tag,
            entrada_com(""),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 0)
        self.assertIn("nome: Livro", mensagens[0])

    def test_06_menu_encaminha_consulta_de_livros_por_tag(self):
        print("Caso de Teste 06 - Consultar livros por tag")
        tags = []

        def acessa_livros():
            self.fail("A busca geral não deveria ser chamada")

        def acessa_livros_por_tag(tag):
            tags.append(tag)
            return 0, [{"id_livro": "l1", "tags": ["ficção"]}]

        codigo = main.lista_livros(
            acessa_livros,
            acessa_livros_por_tag,
            entrada_com("ficção"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 0)
        self.assertEqual(tags, ["ficção"])

    def test_07_menu_exibe_retorno_de_livro_inexistente(self):
        print("Caso de Teste 07 - Exibir retorno de livro inexistente")
        mensagens = []

        def acessa_livro(id_livro):
            self.assertEqual(id_livro, "inexistente")
            return 1, None

        codigo = main.consulta_livro(
            acessa_livro,
            entrada_com("inexistente"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 1)
        self.assertEqual(mensagens[-1], "Registro não encontrado.")

    def test_08_cria_avaliacao_com_livro_selecionado(self):
        print("Caso de Teste 08 - Criar avaliação escolhendo livro pelo menu")
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

        self.assertEqual(codigo, 0)
        self.assertEqual(
            avaliacoes_criadas,
            [
                {
                    "id_avaliacao": 5,
                    "id_livro": "l2",
                    "id_user": "u1",
                }
            ],
        )

    def test_09_cria_avaliacao_rejeita_nota_invalida(self):
        print("Caso de Teste 09 - Rejeitar avaliação com nota inválida")
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

        self.assertEqual(codigo, 6)
        self.assertEqual(avaliacoes_criadas, [])

    def test_10_menu_encaminha_consulta_de_avaliacoes_do_livro(self):
        print("Caso de Teste 10 - Consultar avaliações de um livro")
        livros_consultados = []

        def acessa_avaliacoes_livro(id_livro):
            livros_consultados.append(id_livro)
            return 0, [{"id_avaliacao": "a1", "nota": 5}]

        codigo = main.consulta_avaliacoes_livro(
            acessa_avaliacoes_livro,
            entrada_com("l1"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 0)
        self.assertEqual(livros_consultados, ["l1"])

    def test_11_menu_exibe_nota_calculada_do_livro(self):
        print("Caso de Teste 11 - Exibir nota calculada de um livro")
        mensagens = []

        def calculaNotas(id_livro):
            self.assertEqual(id_livro, "l1")
            return 0, 4.25

        codigo = main.consulta_nota_livro(
            calculaNotas,
            entrada_com("l1"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 0)
        self.assertEqual(mensagens, ["Nota do livro: 4.25"])

    def test_12_aplicacao_carrega_no_inicio_e_salva_no_fim(self):
        print("Caso de Teste 12 - Carregar no início e salvar no fim")
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

        self.assertEqual(
            eventos,
            [
                "carrega usuários",
                "carrega livros",
                "carrega avaliações",
                "salva usuários",
                "salva livros",
                "salva avaliações",
            ],
        )

    def test_13_aplicacao_salva_dados_mesmo_se_ocorrer_erro(self):
        print("Caso de Teste 13 - Salvar dados mesmo após erro")
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

        self.assertEqual(
            eventos[-3:],
            ["salva usuários", "salva livros", "salva avaliações"],
        )


if __name__ == "__main__":
    unittest.main()
