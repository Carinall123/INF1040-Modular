"""Testes automatizados do módulo main com unittest."""

import os
import tempfile
import unittest

import avaliacoes
import livro
import main
import usuarios


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
    """Testes da interação do main com os módulos do sistema."""

    def setUp(self):
        self.tempo_pausa_original = main.TEMPO_PAUSA
        main.TEMPO_PAUSA = 0
        self.tempdir = tempfile.TemporaryDirectory()
        self.arquivo_usuarios_original = usuarios.ARQUIVO_DADOS
        self.arquivo_livros_original = livro.ARQUIVO_DADOS
        self.arquivo_avaliacoes_original = avaliacoes.ARQUIVO_DADOS

        usuarios.ARQUIVO_DADOS = os.path.join(self.tempdir.name, "usuarios.json")
        livro.ARQUIVO_DADOS = os.path.join(self.tempdir.name, "livros.json")
        avaliacoes.ARQUIVO_DADOS = os.path.join(
            self.tempdir.name, "avaliacoes.json"
        )

        usuarios.carrega_dados()
        usuarios.cria_usuario({"id_user": 5, "email": "cinco", "senha": "123"})
        usuarios.cria_usuario({"id_user": "jpt", "email": "jpt", "senha": "jpt"})
        livro.define_livros([])
        avaliacoes.define_livros([10])
        avaliacoes.define_usuarios([5, "jpt"])
        avaliacoes.avaliacoes.clear()
        avaliacoes.avaliacoes.append({
            "id_avaliacao": 4,
            "id_livro": 10,
            "id_user": 5,
        })

    def tearDown(self):
        main.TEMPO_PAUSA = self.tempo_pausa_original
        usuarios.ARQUIVO_DADOS = self.arquivo_usuarios_original
        livro.ARQUIVO_DADOS = self.arquivo_livros_original
        avaliacoes.ARQUIVO_DADOS = self.arquivo_avaliacoes_original
        self.tempdir.cleanup()

    def test_01_cadastra_usuario_com_sucesso(self):
        print("Caso de Teste 01 - Cadastrar usuário com sucesso")

        codigo = main.cadastra_usuario(
            entrada_com("leitor@email.com", "segredo"),
            lambda _mensagem: None,
        )

        codigo_consulta, usuario = usuarios.acessa_usuario("leitor@email.com")
        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(usuario["email"], "leitor@email.com")

    def test_02_cadastra_usuario_com_dados_invalidos(self):
        print("Caso de Teste 02 - Impedir cadastro com dados inválidos")

        codigo = main.cadastra_usuario(
            entrada_com("", "segredo"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 2)

    def test_03_autentica_usuario_com_sucesso(self):
        print("Caso de Teste 03 - Autenticar usuário com sucesso")
        usuarios.cria_usuario(
            {"id_user": "5", "email": "u@u.com", "senha": "123"}
        )

        id_user = main.autentica_usuario(
            entrada_com("5", "123"),
            lambda _mensagem: None,
        )

        self.assertEqual(id_user, "5")

    def test_04_autenticacao_rejeita_senha_incorreta(self):
        print("Caso de Teste 04 - Rejeitar autenticação com senha incorreta")
        usuarios.cria_usuario(
            {"id_user": "5", "email": "u@u.com", "senha": "123"}
        )

        id_user = main.autentica_usuario(
            entrada_com("5", "errada"),
            lambda _mensagem: None,
        )

        self.assertIsNone(id_user)

    def test_05_lista_todos_os_livros(self):
        print("Caso de Teste 05 - Listar todos os livros")
        mensagens = []
        livro.define_livros(
            [{"id_livro": 10, "nome": "Livro", "autor": "Autor", "tags": []}]
        )

        codigo = main.lista_livros(entrada_com(""), saida_em(mensagens))

        self.assertEqual(codigo, 0)
        self.assertTrue(any("nome: Livro" in mensagem for mensagem in mensagens))

    def test_06_lista_livros_por_tag(self):
        print("Caso de Teste 06 - Listar livros por tag")
        mensagens = []
        livro.define_livros(
            [
                {
                    "id_livro": 10,
                    "nome": "Livro",
                    "autor": "Autor",
                    "tags": ["ficção"],
                }
            ]
        )

        codigo = main.lista_livros(entrada_com("ficção"), saida_em(mensagens))

        self.assertEqual(codigo, 0)
        self.assertTrue(any("ficção" in mensagem for mensagem in mensagens))

    def test_07_consulta_livro_inexistente(self):
        print("Caso de Teste 07 - Exibir retorno de livro inexistente")
        mensagens = []

        codigo = main.consulta_livro(entrada_com("99"), saida_em(mensagens))

        self.assertEqual(codigo, 1)
        self.assertIn("Registro não encontrado.", mensagens[-1])

    def test_08_cria_avaliacao_com_livro_selecionado(self):
        print("Caso de Teste 08 - Criar avaliação escolhendo livro pelo menu")
        livro.define_livros(
            [{"id_livro": 10, "nome": "Livro", "autor": "Autor", "tags": []}]
        )

        codigo = main.avalia_livro(
            "jpt",
            entrada_com("10", "5"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 0)

    def test_08b_avaliacao_do_mesmo_usuario_sobrescreve_anterior(self):
        print("Caso de Teste 08b - Sobrescrever avaliação do mesmo usuário")
        livro.define_livros(
            [{"id_livro": 10, "nome": "Livro", "autor": "Autor", "tags": []}]
        )

        primeiro_codigo = main.avalia_livro(
            "jpt",
            entrada_com("10", "4"),
            lambda _mensagem: None,
        )
        segundo_codigo = main.avalia_livro(
            "jpt",
            entrada_com("10", "5"),
            lambda _mensagem: None,
        )
        codigo_consulta, lista = avaliacoes.acessa_avaliacoes_usuario("jpt")

        self.assertEqual(primeiro_codigo, 0)
        self.assertEqual(segundo_codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["id_avaliacao"], 5)

    def test_09_cria_avaliacao_rejeita_nota_invalida(self):
        print("Caso de Teste 09 - Rejeitar avaliação com nota inválida")
        livro.define_livros(
            [{"id_livro": 10, "nome": "Livro", "autor": "Autor", "tags": []}]
        )

        codigo = main.avalia_livro(
            5,
            entrada_com("10", "6"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 6)

    def test_10_consulta_avaliacoes_do_livro(self):
        print("Caso de Teste 10 - Consultar avaliações de um livro")
        mensagens = []
        livro.define_livros(
            [{"id_livro": 10, "nome": "Livro", "autor": "Autor", "tags": []}]
        )

        codigo = main.consulta_avaliacoes_livro(
            entrada_com("10"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 0)
        self.assertTrue(any("id_user: 5" in mensagem for mensagem in mensagens))

    def test_11_consulta_nota_calculada_do_livro(self):
        print("Caso de Teste 11 - Consultar nota calculada de um livro")
        mensagens = []
        livro.define_livros(
            [{"id_livro": 10, "nome": "Livro", "autor": "Autor", "tags": []}]
        )

        codigo = main.consulta_nota_livro(entrada_com("10"), saida_em(mensagens))

        self.assertEqual(codigo, 0)
        self.assertTrue(any("Nota do livro: 4.00" in mensagem for mensagem in mensagens))

    def test_12_aplicacao_carrega_no_inicio_e_salva_no_fim(self):
        print("Caso de Teste 12 - Carregar no início e salvar no fim")
        usuarios.cria_usuario(
            {"id_user": "5", "email": "u@u.com", "senha": "123"}
        )

        main.executa_aplicacao(
            entrada_com("0"),
            lambda _mensagem: None,
        )

        self.assertTrue(os.path.exists(usuarios.ARQUIVO_DADOS))
        self.assertTrue(os.path.exists(livro.ARQUIVO_DADOS))
        self.assertTrue(os.path.exists(avaliacoes.ARQUIVO_DADOS))

    def test_13_aplicacao_salva_dados_mesmo_se_ocorrer_erro(self):
        print("Caso de Teste 13 - Salvar dados mesmo após erro")

        def entrada_com_erro(_mensagem):
            raise RuntimeError("erro durante a execução")

        try:
            main.executa_aplicacao(
                entrada_com_erro,
                lambda _mensagem: None,
            )
        except RuntimeError:
            pass

        self.assertTrue(os.path.exists(usuarios.ARQUIVO_DADOS))


if __name__ == "__main__":
    unittest.main()
