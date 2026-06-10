"""Testes automatizados do módulo livro com unittest."""

import json
import os
import tempfile
import unittest

from livro import (
    acessa_livro,
    acessa_livros,
    acessa_livros_por_tag,
    carrega_dados,
    cria_livro,
    deleta_livro,
    modifica_livro,
    salva_dados,
)


class TesteLivro(unittest.TestCase):
    """Testes das funções de acesso do módulo livro."""

    def setUp(self):
        self.diretorio_original = os.getcwd()
        self.tempdir = tempfile.TemporaryDirectory()
        os.chdir(self.tempdir.name)
        carrega_dados()

    def tearDown(self):
        os.chdir(self.diretorio_original)
        self.tempdir.cleanup()

    def test_acessa_livro(self):
        print("\nTeste acessa_livro")
        cria_livro({
            "id_livro": 1,
            "nome": "Dom Casmurro",
            "autor": "Machado de Assis",
            "tags": ["romance", "classico"],
        })

        codigo, livro = acessa_livro("  dom casmurro  ")
        codigo_inexistente, livro_inexistente = acessa_livro("Inexistente")
        codigo_invalido, livro_invalido = acessa_livro("")

        self.assertEqual(codigo, 0)
        self.assertEqual(livro["nome"], "Dom Casmurro")
        self.assertEqual(codigo_inexistente, 1)
        self.assertIsNone(livro_inexistente)
        self.assertEqual(codigo_invalido, 2)
        self.assertIsNone(livro_invalido)

    def test_acessa_livros(self):
        print("\nTeste acessa_livros")

        codigo_vazio, lista_vazia = acessa_livros()
        cria_livro({
            "id_livro": 2,
            "nome": "O Cortico",
            "autor": "Aluisio Azevedo",
            "tags": ["romance"],
        })
        codigo, livros = acessa_livros()

        self.assertEqual(codigo_vazio, 1)
        self.assertEqual(lista_vazia, [])
        self.assertEqual(codigo, 0)
        self.assertEqual(len(livros), 1)

    def test_acessa_livros_por_tag(self):
        print("\nTeste acessa_livros_por_tag")
        cria_livro({
            "id_livro": 3,
            "nome": "Iracema",
            "autor": "Jose de Alencar",
            "tags": ["romance", "brasileiro"],
        })

        codigo, livros = acessa_livros_por_tag("romance")
        codigo_ausente, lista_ausente = acessa_livros_por_tag("terror")
        codigo_invalido, lista_invalida = acessa_livros_por_tag("")

        self.assertEqual(codigo, 0)
        self.assertEqual(len(livros), 1)
        self.assertEqual(codigo_ausente, 1)
        self.assertEqual(lista_ausente, [])
        self.assertEqual(codigo_invalido, 2)
        self.assertEqual(lista_invalida, [])

    def test_cria_livro(self):
        print("\nTeste cria_livro")
        livro = {
            "id_livro": 4,
            "nome": "Memorias Postumas",
            "autor": "Machado de Assis",
            "tags": ["classico"],
        }

        codigo = cria_livro(livro)
        codigo_duplicado = cria_livro(livro)
        codigo_nome_duplicado = cria_livro({
            "id_livro": 40,
            "nome": "  MEMORIAS POSTUMAS ",
            "autor": "Outro Autor",
            "tags": [],
        })
        codigo_invalido = cria_livro({
            "id_livro": "",
            "nome": "",
            "autor": "",
            "tags": [],
        })

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_duplicado, 3)
        self.assertEqual(codigo_nome_duplicado, 3)
        self.assertEqual(codigo_invalido, 2)

    def test_modifica_livro(self):
        print("\nTeste modifica_livro")
        cria_livro({
            "id_livro": 5,
            "nome": "Livro Antigo",
            "autor": "Autor Antigo",
            "tags": ["antigo"],
        })
        novo_livro = {
            "id_livro": 5,
            "nome": "Livro Novo",
            "autor": "Autor Novo",
            "tags": ["novo"],
        }

        codigo = modifica_livro(5, novo_livro)
        codigo_inexistente = modifica_livro(99, novo_livro)
        codigo_invalido = modifica_livro(5, {
            "id_livro": "",
            "nome": "",
            "autor": "",
            "tags": [],
        })

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_inexistente, 1)
        self.assertEqual(codigo_invalido, 2)

    def test_deleta_livro(self):
        print("\nTeste deleta_livro")
        cria_livro({
            "id_livro": 6,
            "nome": "Livro para Remover",
            "autor": "Autor",
            "tags": ["remover"],
        })

        codigo = deleta_livro(6)
        codigo_inexistente = deleta_livro(99)

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_inexistente, 1)

    def test_consulta_retorna_copia(self):
        print("\nTeste encapsulamento dos livros")
        cria_livro({
            "id_livro": 7,
            "nome": "Original",
            "autor": "Autor",
            "tags": [],
        })

        _codigo, livro = acessa_livro("Original")
        livro["nome"] = "Alterado externamente"
        _codigo, livro_armazenado = acessa_livro("Original")

        self.assertEqual(livro_armazenado["nome"], "Original")

    def test_persistencia_de_dados(self):
        print("\nTeste persistência dos livros")
        cria_livro({
            "id_livro": 8,
            "nome": "Persistente",
            "autor": "Autor",
            "tags": [],
        })

        codigo_salva = salva_dados()
        carrega_dados()
        codigo_consulta, livro = acessa_livro("Persistente")

        self.assertEqual(codigo_salva, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(livro["nome"], "Persistente")

    def test_modifica_livro_rejeita_alteracao_de_id(self):
        print("\nTeste alteração do ID do livro")
        cria_livro({
            "id_livro": 9,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = modifica_livro(9, {
            "id_livro": 10,
            "nome": "Livro",
            "autor": "Autor",
            "tags": [],
        })

        self.assertEqual(codigo, 2)

    def test_modifica_livro_rejeita_nome_duplicado(self):
        print("\nTeste alteração para nome já cadastrado")
        cria_livro({
            "id_livro": 11,
            "nome": "Primeiro Livro",
            "autor": "Autor",
            "tags": [],
        })
        cria_livro({
            "id_livro": 12,
            "nome": "Segundo Livro",
            "autor": "Autor",
            "tags": [],
        })

        codigo = modifica_livro(12, {
            "id_livro": 12,
            "nome": " primeiro livro ",
            "autor": "Outro Autor",
            "tags": [],
        })

        self.assertEqual(codigo, 3)

    def test_carrega_dados_invalidos(self):
        print("\nTeste arquivo de livros inválido")
        os.makedirs("dados", exist_ok=True)
        with open("dados/livros.json", "w", encoding="utf-8") as arquivo:
            json.dump({"conteudo": "invalido"}, arquivo)

        codigo = carrega_dados()

        self.assertEqual(codigo, 2)

    def test_carrega_dados_rejeita_nomes_duplicados(self):
        print("\nTeste nomes duplicados no arquivo de livros")
        os.makedirs("dados", exist_ok=True)
        with open("dados/livros.json", "w", encoding="utf-8") as arquivo:
            json.dump([
                {
                    "id_livro": 1,
                    "nome": "Livro",
                    "autor": "Autor",
                    "tags": [],
                },
                {
                    "id_livro": 2,
                    "nome": "  LIVRO ",
                    "autor": "Outro Autor",
                    "tags": [],
                },
            ], arquivo)

        codigo = carrega_dados()
        codigo_consulta, livros = acessa_livros()

        self.assertEqual(codigo, 2)
        self.assertEqual(codigo_consulta, 1)
        self.assertEqual(livros, [])


if __name__ == "__main__":
    unittest.main()
