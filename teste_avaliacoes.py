"""Testes automatizados do módulo avaliacoes com unittest."""

import os
import tempfile
import unittest

import avaliacoes


class TesteAvaliacoes(unittest.TestCase):
    """Testes das funções de acesso do módulo de avaliações."""

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.arquivo_original = avaliacoes.ARQUIVO_DADOS
        avaliacoes.ARQUIVO_DADOS = os.path.join(
            self.tempdir.name,
            "avaliacoes.json",
        )
        avaliacoes.avaliacoes.clear()
        avaliacoes.define_livros([10])
        avaliacoes.define_usuarios([5, "jpt"])
        avaliacoes.cria_avaliacao({
            "id_avaliacao": 4,
            "id_livro": 10,
            "id_user": 5,
        })

    def tearDown(self):
        avaliacoes.ARQUIVO_DADOS = self.arquivo_original
        self.tempdir.cleanup()

    def test_01_acessa_avaliacao_encontrada(self):
        print("\nCaso de Teste 01 acessa_avaliacao - Avaliação encontrada")

        codigo, avaliacao = avaliacoes.acessa_avaliacao(4)

        print("Código 0: Operação realizada com sucesso")
        self.assertEqual(codigo, 0)
        self.assertEqual(avaliacao["id_avaliacao"], 4)

    def test_02_acessa_avaliacao_nao_encontrada(self):
        print("\nCaso de Teste 02 acessa_avaliacao - Avaliação não encontrada")

        codigo, avaliacao = avaliacoes.acessa_avaliacao(999)

        print("Código 1: Registro não encontrado")
        self.assertEqual(codigo, 1)
        self.assertIsNone(avaliacao)

    def test_03_acessa_avaliacoes_livro_encontradas(self):
        print("\nCaso de Teste 03 acessa_avaliacoes_livro - Avaliações encontradas")

        codigo, lista = avaliacoes.acessa_avaliacoes_livro(10)

        print("Código 0: Operação realizada com sucesso")
        self.assertEqual(codigo, 0)
        self.assertEqual(len(lista), 1)

    def test_04_acessa_avaliacoes_livro_sem_avaliacoes(self):
        print("\nCaso de Teste 04 acessa_avaliacoes_livro - Sem avaliações")
        avaliacoes.define_livros([10, 11])

        codigo, lista = avaliacoes.acessa_avaliacoes_livro(11)

        print("Código 1: Registro não encontrado")
        self.assertEqual(codigo, 1)
        self.assertEqual(lista, [])

    def test_05_acessa_avaliacoes_livro_inexistente(self):
        print("\nCaso de Teste 05 acessa_avaliacoes_livro - Livro inexistente")

        codigo, lista = avaliacoes.acessa_avaliacoes_livro(2)

        print("Código 4: Livro inexistente")
        self.assertEqual(codigo, 4)
        self.assertEqual(lista, [])

    def test_06_acessa_avaliacoes_usuario_encontradas(self):
        print("\nCaso de Teste 06 acessa_avaliacoes_usuario - Avaliações encontradas")

        codigo, lista = avaliacoes.acessa_avaliacoes_usuario(5)

        print("Código 0: Operação realizada com sucesso")
        self.assertEqual(codigo, 0)
        self.assertEqual(len(lista), 1)

    def test_07_acessa_avaliacoes_usuario_sem_avaliacoes(self):
        print("\nCaso de Teste 07 acessa_avaliacoes_usuario - Sem avaliações")

        codigo, lista = avaliacoes.acessa_avaliacoes_usuario("jpt")

        print("Código 1: Registro não encontrado")
        self.assertEqual(codigo, 1)
        self.assertEqual(lista, [])

    def test_08_acessa_avaliacoes_usuario_inexistente(self):
        print("\nCaso de Teste 08 acessa_avaliacoes_usuario - Usuário inexistente")

        codigo, lista = avaliacoes.acessa_avaliacoes_usuario(2)

        print("Código 5: Usuário inexistente")
        self.assertEqual(codigo, 5)
        self.assertEqual(lista, [])

    def test_09_cria_avaliacao_com_sucesso(self):
        print("\nCaso de Teste 09 cria_avaliacao - Avaliação criada com sucesso")

        codigo = avaliacoes.cria_avaliacao({
            "id_avaliacao": 5,
            "id_livro": 10,
            "id_user": "jpt",
        })

        print("Código 0: Operação realizada com sucesso")
        self.assertEqual(codigo, 0)
        self.assertEqual(len(avaliacoes.avaliacoes), 2)

    def test_09b_cria_avaliacao_sobrescreve_usuario(self):
        print("\nCaso de Teste 09b cria_avaliacao - Sobrescreve avaliação do usuário")

        codigo = avaliacoes.cria_avaliacao({
            "id_avaliacao": 2,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 0)
        self.assertEqual(len(avaliacoes.avaliacoes), 1)
        self.assertEqual(avaliacoes.avaliacoes[0]["id_avaliacao"], 2)

    def test_10_cria_avaliacao_livro_inexistente(self):
        print("\nCaso de Teste 10 cria_avaliacao - Livro inexistente")

        codigo = avaliacoes.cria_avaliacao({
            "id_avaliacao": 2,
            "id_livro": 1,
            "id_user": 5,
        })

        print("Código 4: Livro inexistente")
        self.assertEqual(codigo, 4)

    def test_11_cria_avaliacao_usuario_inexistente(self):
        print("\nCaso de Teste 11 cria_avaliacao - Usuário inexistente")

        codigo = avaliacoes.cria_avaliacao({
            "id_avaliacao": 2,
            "id_livro": 10,
            "id_user": 1,
        })

        print("Código 5: Usuário inexistente")
        self.assertEqual(codigo, 5)

    def test_12_cria_avaliacao_nota_invalida(self):
        print("\nCaso de Teste 12 cria_avaliacao - Nota inválida")

        codigo = avaliacoes.cria_avaliacao({
            "id_avaliacao": -2,
            "id_livro": 10,
            "id_user": 5,
        })

        print("Código 6: Nota inválida")
        self.assertEqual(codigo, 6)

    def test_13_modifica_avaliacao_com_sucesso(self):
        print("\nCaso de Teste 13 modifica_avaliacao - Avaliação modificada")

        codigo = avaliacoes.modifica_avaliacao(4, {
            "id_avaliacao": 3,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 0)

    def test_14_modifica_avaliacao_nao_encontrada(self):
        print("\nCaso de Teste 14 modifica_avaliacao - Avaliação não encontrada")

        codigo = avaliacoes.modifica_avaliacao(1, {
            "id_avaliacao": 3,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 1)

    def test_15_modifica_avaliacao_dados_invalidos(self):
        print("\nCaso de Teste 15 modifica_avaliacao - Dados inválidos")

        codigo = avaliacoes.modifica_avaliacao(4, {
            "id_avaliacao": 8,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 2)

    def test_16_deleta_avaliacao_com_sucesso(self):
        print("\nCaso de Teste 16 deleta_avaliacao - Avaliação removida")

        codigo = avaliacoes.deleta_avaliacao(4)

        self.assertEqual(codigo, 0)

    def test_17_deleta_avaliacao_nao_encontrada(self):
        print("\nCaso de Teste 17 deleta_avaliacao - Avaliação não encontrada")

        codigo = avaliacoes.deleta_avaliacao(2)

        self.assertEqual(codigo, 1)

    def test_18_calculaNotas_com_sucesso(self):
        print("\nCaso de Teste 18 calculaNotas - Nota calculada com sucesso")
        avaliacoes.cria_avaliacao({
            "id_avaliacao": 2,
            "id_livro": 10,
            "id_user": "jpt",
        })

        codigo, nota = avaliacoes.calculaNotas(10)

        self.assertEqual(codigo, 0)
        self.assertEqual(nota, 3)

    def test_19_calculaNotas_sem_avaliacoes(self):
        print("\nCaso de Teste 19 calculaNotas - Livro sem avaliações")
        avaliacoes.define_livros([10, 11])

        codigo, nota = avaliacoes.calculaNotas(11)

        self.assertEqual(codigo, 1)
        self.assertIsNone(nota)

    def test_20_calculaNotas_livro_inexistente(self):
        print("\nCaso de Teste 20 calculaNotas - Livro inexistente")

        codigo, nota = avaliacoes.calculaNotas(2)

        self.assertEqual(codigo, 4)
        self.assertIsNone(nota)

    def test_21_persistencia_de_dados(self):
        print("\nCaso de Teste 21 avaliações - Persistência de dados")

        avaliacoes.salva_dados()
        avaliacoes.avaliacoes.clear()
        avaliacoes.carrega_dados()

        self.assertEqual(len(avaliacoes.avaliacoes), 1)
        self.assertEqual(avaliacoes.avaliacoes[0]["id_livro"], 10)


if __name__ == "__main__":
    unittest.main()
