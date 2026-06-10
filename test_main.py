"""Testes automatizados do módulo main com unittest."""

import os
import tempfile
import unittest
from unittest.mock import patch

from avaliacoes import (
    acessa_avaliacoes_usuario,
    carrega_dados as carrega_avaliacoes,
    cria_avaliacao,
)
from livro import (
    carrega_dados as carrega_livros,
    cria_livro,
)
from main import (
    autentica_usuario,
    avalia_livro,
    cadastra_usuario,
    consulta_avaliacoes_livro,
    consulta_livro,
    consulta_nota_livro,
    executa_aplicacao,
    lista_livros,
    menu_usuario,
)
from usuarios import (
    acessa_usuario,
    carrega_dados as carrega_usuarios,
    cria_usuario,
)


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
    """Testes da interação da main com as funções públicas dos TADs."""

    def setUp(self):
        self.diretorio_original = os.getcwd()
        self.tempdir = tempfile.TemporaryDirectory()
        os.chdir(self.tempdir.name)
        carrega_usuarios()
        carrega_livros()
        carrega_avaliacoes()
        cria_usuario({"id_user": 5, "email": "cinco", "senha": "123"})
        cria_usuario({"id_user": "jpt", "email": "jpt", "senha": "jpt"})
        self.pausa = patch("main.time.sleep", return_value=None)
        self.pausa.start()

    def tearDown(self):
        self.pausa.stop()
        os.chdir(self.diretorio_original)
        self.tempdir.cleanup()

    def test_01_cadastra_usuario_com_sucesso(self):
        print("Caso de Teste 01 - Cadastrar usuário com sucesso")

        codigo = cadastra_usuario(
            entrada_com("leitor@email.com", "segredo"),
            lambda _mensagem: None,
        )
        codigo_consulta, usuario = acessa_usuario("leitor@email.com")

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(usuario["email"], "leitor@email.com")

    def test_02_cadastra_usuario_com_dados_invalidos(self):
        print("Caso de Teste 02 - Impedir cadastro com dados inválidos")

        codigo = cadastra_usuario(
            entrada_com("", "segredo"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 2)

    def test_03_autentica_usuario_com_sucesso(self):
        print("Caso de Teste 03 - Autenticar usuário com sucesso")

        id_user = autentica_usuario(
            entrada_com("jpt", "jpt"),
            lambda _mensagem: None,
        )

        self.assertEqual(id_user, "jpt")

    def test_04_autenticacao_rejeita_senha_incorreta(self):
        print("Caso de Teste 04 - Rejeitar autenticação com senha incorreta")

        id_user = autentica_usuario(
            entrada_com("jpt", "errada"),
            lambda _mensagem: None,
        )

        self.assertIsNone(id_user)

    def test_05_lista_todos_os_livros(self):
        print("Caso de Teste 05 - Listar todos os livros")
        mensagens = []
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = lista_livros(entrada_com(""), saida_em(mensagens))

        self.assertEqual(codigo, 0)
        self.assertTrue(any("nome: Livro" in mensagem for mensagem in mensagens))

    def test_06_lista_livros_por_tag(self):
        print("Caso de Teste 06 - Listar livros por tag")
        mensagens = []
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": ["ficção"],
        })

        codigo = lista_livros(entrada_com("ficção"), saida_em(mensagens))

        self.assertEqual(codigo, 0)
        self.assertTrue(any("ficção" in mensagem for mensagem in mensagens))

    def test_07_consulta_livro_inexistente(self):
        print("Caso de Teste 07 - Exibir retorno de livro inexistente")
        mensagens = []

        codigo = consulta_livro(
            entrada_com("Livro inexistente"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 1)
        self.assertIn("Registro não encontrado.", mensagens[-1])

    def test_08_cria_avaliacao_com_livro_selecionado(self):
        print("Caso de Teste 08 - Criar avaliação escolhendo livro")
        mensagens = []
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = avalia_livro(
            "jpt",
            entrada_com("Livro", "5"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 0)
        self.assertIn(
            "ID: 10 | Livro: Livro | Autor: Autor",
            mensagens,
        )

    def test_09_avaliacao_do_mesmo_usuario_sobrescreve_anterior(self):
        print("Caso de Teste 09 - Sobrescrever avaliação do mesmo usuário")
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        avalia_livro("jpt", entrada_com("Livro", "4"), lambda _mensagem: None)
        codigo = avalia_livro(
            "jpt",
            entrada_com("livro", "5"),
            lambda _mensagem: None,
        )
        codigo_consulta, lista = acessa_avaliacoes_usuario("jpt")

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["id_avaliacao"], 1)
        self.assertEqual(lista[0]["nota"], 5)
        self.assertEqual(lista[0]["id_livro"], 10)

    def test_10_cria_avaliacao_rejeita_nota_invalida(self):
        print("Caso de Teste 10 - Rejeitar avaliação com nota inválida")
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = avalia_livro(
            "jpt",
            entrada_com("Livro", "6"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 6)

    def test_11_consulta_avaliacoes_do_livro(self):
        print("Caso de Teste 11 - Consultar avaliações de um livro")
        mensagens = []
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })
        cria_avaliacao({
            "nota": 4,
            "id_livro": 10,
            "id_user": 5,
        })

        codigo = consulta_avaliacoes_livro(
            entrada_com("Livro"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 0)
        self.assertTrue(any("id_user: 5" in mensagem for mensagem in mensagens))

    def test_12_consulta_nota_calculada_do_livro(self):
        print("Caso de Teste 12 - Consultar nota calculada de um livro")
        mensagens = []
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })
        cria_avaliacao({
            "nota": 4,
            "id_livro": 10,
            "id_user": 5,
        })

        codigo = consulta_nota_livro(
            entrada_com("Livro"),
            saida_em(mensagens),
        )

        self.assertEqual(codigo, 0)
        self.assertTrue(
            any("Nota do livro: 4.00" in mensagem for mensagem in mensagens)
        )

    def test_13_aplicacao_carrega_no_inicio_e_salva_no_fim(self):
        print("Caso de Teste 13 - Carregar no início e salvar no fim")

        executa_aplicacao(
            entrada_com("0"),
            lambda _mensagem: None,
        )

        self.assertTrue(os.path.exists("dados/usuarios.json"))
        self.assertTrue(os.path.exists("dados/livros.json"))
        self.assertTrue(os.path.exists("dados/avaliacoes.json"))

    def test_14_aplicacao_salva_dados_mesmo_se_ocorrer_erro(self):
        print("Caso de Teste 14 - Salvar dados mesmo após erro")

        def entrada_com_erro(_mensagem):
            raise RuntimeError("erro durante a execução")

        with self.assertRaises(RuntimeError):
            executa_aplicacao(
                entrada_com_erro,
                lambda _mensagem: None,
            )

        self.assertTrue(os.path.exists("dados/usuarios.json"))

    def test_15_avaliacao_rejeita_usuario_inexistente(self):
        print("Caso de Teste 15 - Rejeitar usuário inexistente")

        codigo = avalia_livro(
            "inexistente",
            entrada_com(),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 5)

    def test_16_consulta_avaliacoes_livro_inexistente(self):
        print("Caso de Teste 16 - Consultar avaliações de livro inexistente")

        codigo = consulta_avaliacoes_livro(
            entrada_com("Livro inexistente"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 4)

    def test_17_consulta_nota_livro_inexistente(self):
        print("Caso de Teste 17 - Consultar nota de livro inexistente")

        codigo = consulta_nota_livro(
            entrada_com("Livro inexistente"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 4)

    def test_18_consulta_livro_rejeita_nome_vazio(self):
        print("Caso de Teste 18 - Rejeitar nome de livro vazio")

        codigo = consulta_livro(
            entrada_com(""),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 2)

    def test_19_lista_livros_sem_resultados(self):
        print("Caso de Teste 19 - Tag sem livros")

        codigo = lista_livros(
            entrada_com("terror"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 1)

    def test_20_consulta_avaliacoes_livro_sem_avaliacoes(self):
        print("Caso de Teste 20 - Livro sem avaliações")
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = consulta_avaliacoes_livro(
            entrada_com("Livro"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 1)

    def test_21_consulta_nota_livro_sem_avaliacoes(self):
        print("Caso de Teste 21 - Livro sem nota")
        cria_livro({
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = consulta_nota_livro(
            entrada_com("Livro"),
            lambda _mensagem: None,
        )

        self.assertEqual(codigo, 1)

    def test_22_menu_usuario_rejeita_opcao_invalida(self):
        print("Caso de Teste 22 - Opção inválida no menu do usuário")
        mensagens = []

        menu_usuario(
            "jpt",
            entrada_com("9", "0"),
            saida_em(mensagens),
        )

        self.assertTrue(any("Opção inválida." in mensagem for mensagem in mensagens))

    def test_23_menu_principal_rejeita_opcao_invalida(self):
        print("Caso de Teste 23 - Opção inválida no menu principal")
        mensagens = []

        executa_aplicacao(
            entrada_com("9", "0"),
            saida_em(mensagens),
        )

        self.assertTrue(any("Opção inválida." in mensagem for mensagem in mensagens))


if __name__ == "__main__":
    unittest.main()
