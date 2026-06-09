"""Testes automatizados do módulo avaliacoes com unittest."""

import json
import os
import tempfile
import unittest

from avaliacoes import (
    acessa_avaliacao,
    acessa_avaliacoes_livro,
    acessa_avaliacoes_usuario,
    calculaNotas,
    carrega_dados,
    cria_avaliacao,
    deleta_avaliacao,
    modifica_avaliacao,
    salva_dados,
)


class TesteAvaliacoes(unittest.TestCase):
    """Testes das funções de acesso do módulo avaliacoes."""

    def setUp(self):
        self.diretorio_original = os.getcwd()
        self.tempdir = tempfile.TemporaryDirectory()
        os.chdir(self.tempdir.name)
        carrega_dados()
        cria_avaliacao({
            "nota": 4,
            "id_livro": 10,
            "id_user": 5,
        })

    def tearDown(self):
        os.chdir(self.diretorio_original)
        self.tempdir.cleanup()

    def test_01_acessa_avaliacao_encontrada(self):
        print("\nCaso de Teste 01 - Acessar avaliação encontrada")

        codigo, avaliacao = acessa_avaliacao(1)

        self.assertEqual(codigo, 0)
        self.assertEqual(avaliacao["id_avaliacao"], 1)
        self.assertEqual(avaliacao["nota"], 4)

    def test_02_acessa_avaliacao_nao_encontrada(self):
        print("\nCaso de Teste 02 - Acessar avaliação inexistente")

        codigo, avaliacao = acessa_avaliacao(999)

        self.assertEqual(codigo, 1)
        self.assertIsNone(avaliacao)

    def test_03_acessa_avaliacoes_livro_encontradas(self):
        print("\nCaso de Teste 03 - Acessar avaliações de livro")

        codigo, lista = acessa_avaliacoes_livro(10)

        self.assertEqual(codigo, 0)
        self.assertEqual(len(lista), 1)

    def test_04_acessa_avaliacoes_livro_sem_avaliacoes(self):
        print("\nCaso de Teste 04 - Livro sem avaliações")

        codigo, lista = acessa_avaliacoes_livro(11)

        self.assertEqual(codigo, 1)
        self.assertEqual(lista, [])

    def test_05_acessa_avaliacoes_usuario_encontradas(self):
        print("\nCaso de Teste 05 - Acessar avaliações de usuário")

        codigo, lista = acessa_avaliacoes_usuario(5)

        self.assertEqual(codigo, 0)
        self.assertEqual(len(lista), 1)

    def test_06_acessa_avaliacoes_usuario_sem_avaliacoes(self):
        print("\nCaso de Teste 06 - Usuário sem avaliações")

        codigo, lista = acessa_avaliacoes_usuario("jpt")

        self.assertEqual(codigo, 1)
        self.assertEqual(lista, [])

    def test_07_cria_avaliacao_gera_id(self):
        print("\nCaso de Teste 07 - Criar avaliação gera ID")

        codigo = cria_avaliacao({
            "nota": 5,
            "id_livro": 10,
            "id_user": "jpt",
        })
        codigo_consulta, avaliacao = acessa_avaliacao(2)

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(avaliacao["nota"], 5)

    def test_08_cria_avaliacao_sobrescreve_e_preserva_id(self):
        print("\nCaso de Teste 08 - Sobrescrever preserva ID")

        codigo = cria_avaliacao({
            "nota": 2,
            "id_livro": 11,
            "id_user": 5,
        })
        codigo_consulta, lista = acessa_avaliacoes_usuario(5)

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["id_avaliacao"], 1)
        self.assertEqual(lista[0]["nota"], 2)
        self.assertEqual(lista[0]["id_livro"], 11)

    def test_09_cria_avaliacao_dados_invalidos(self):
        print("\nCaso de Teste 09 - Criar avaliação com dados inválidos")

        codigo = cria_avaliacao({
            "nota": 8,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 2)

    def test_10_modifica_avaliacao_com_sucesso(self):
        print("\nCaso de Teste 10 - Modificar avaliação")

        codigo = modifica_avaliacao(1, {
            "nota": 3,
            "id_livro": 10,
            "id_user": 5,
        })
        _codigo, avaliacao = acessa_avaliacao(1)

        self.assertEqual(codigo, 0)
        self.assertEqual(avaliacao["nota"], 3)

    def test_11_modifica_avaliacao_nao_encontrada(self):
        print("\nCaso de Teste 11 - Modificar avaliação inexistente")

        codigo = modifica_avaliacao(999, {
            "nota": 3,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 1)

    def test_12_modifica_avaliacao_dados_invalidos(self):
        print("\nCaso de Teste 12 - Modificar com dados inválidos")

        codigo = modifica_avaliacao(1, {
            "nota": 8,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 2)

    def test_13_deleta_avaliacao_com_sucesso(self):
        print("\nCaso de Teste 13 - Deletar avaliação")

        codigo = deleta_avaliacao(1)

        self.assertEqual(codigo, 0)

    def test_14_deleta_avaliacao_nao_encontrada(self):
        print("\nCaso de Teste 14 - Deletar avaliação inexistente")

        codigo = deleta_avaliacao(999)

        self.assertEqual(codigo, 1)

    def test_15_calcula_notas_com_sucesso(self):
        print("\nCaso de Teste 15 - Calcular média")
        cria_avaliacao({
            "nota": 2,
            "id_livro": 10,
            "id_user": "jpt",
        })

        codigo, nota = calculaNotas(10)

        self.assertEqual(codigo, 0)
        self.assertEqual(nota, 3)

    def test_16_calcula_notas_sem_avaliacoes(self):
        print("\nCaso de Teste 16 - Calcular livro sem avaliações")

        codigo, nota = calculaNotas(11)

        self.assertEqual(codigo, 1)
        self.assertIsNone(nota)

    def test_17_persistencia_de_dados(self):
        print("\nCaso de Teste 17 - Persistência de avaliações")

        codigo_salva = salva_dados()
        codigo_carrega = carrega_dados()
        codigo_consulta, avaliacao = acessa_avaliacao(1)

        self.assertEqual(codigo_salva, 0)
        self.assertEqual(codigo_carrega, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(avaliacao["nota"], 4)

    def test_18_consulta_retorna_copia(self):
        print("\nCaso de Teste 18 - Encapsulamento")

        _codigo, avaliacao = acessa_avaliacao(1)
        avaliacao["nota"] = 0
        _codigo, avaliacao_armazenada = acessa_avaliacao(1)

        self.assertEqual(avaliacao_armazenada["nota"], 4)

    def test_19_carrega_dados_invalidos(self):
        print("\nCaso de Teste 19 - Arquivo de avaliações inválido")
        os.makedirs("dados", exist_ok=True)
        with open("dados/avaliacoes.json", "w", encoding="utf-8") as arquivo:
            json.dump({"conteudo": "invalido"}, arquivo)

        codigo = carrega_dados()

        self.assertEqual(codigo, 2)

    def test_20_migra_formato_antigo(self):
        print("\nCaso de Teste 20 - Migrar avaliação sem campo nota")
        os.makedirs("dados", exist_ok=True)
        with open("dados/avaliacoes.json", "w", encoding="utf-8") as arquivo:
            json.dump(
                [{"id_avaliacao": 4, "id_livro": 10, "id_user": "antigo"}],
                arquivo,
            )

        codigo = carrega_dados()
        codigo_consulta, lista = acessa_avaliacoes_usuario("antigo")

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(lista[0]["id_avaliacao"], 1)
        self.assertEqual(lista[0]["nota"], 4)

    def test_21_novo_id_continua_apos_recarregar(self):
        print("\nCaso de Teste 21 - Continuar geração de IDs")
        cria_avaliacao({
            "nota": 3,
            "id_livro": 10,
            "id_user": "u2",
        })
        salva_dados()
        carrega_dados()

        codigo = cria_avaliacao({
            "nota": 5,
            "id_livro": 10,
            "id_user": "u3",
        })
        codigo_consulta, avaliacao = acessa_avaliacao(3)

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(avaliacao["nota"], 5)

    def test_22_modifica_rejeita_usuario_duplicado(self):
        print("\nCaso de Teste 22 - Rejeitar usuário duplicado na modificação")
        cria_avaliacao({
            "nota": 3,
            "id_livro": 10,
            "id_user": "u2",
        })

        codigo = modifica_avaliacao(2, {
            "nota": 5,
            "id_livro": 10,
            "id_user": 5,
        })

        self.assertEqual(codigo, 7)


if __name__ == "__main__":
    unittest.main()
