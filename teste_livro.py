# teste_livro.py - Testes para as funções do módulo livro.py

import unittest
from livro import *


# Convenção dos códigos de teste
# 0 - Operação realizada com sucesso
# 1 - Registro não encontrado
# 2 - Dados inválidos
# 3 - Identificador já cadastrado


def imprime_codigo(codigo):
    mensagens = {
        0: "Operação realizada com sucesso",
        1: "Registro não encontrado",
        2: "Dados inválidos",
        3: "Identificador já cadastrado"
    }

    print(f"Código {codigo}: {mensagens[codigo]}")


class TesteLivro(unittest.TestCase):

    def test_acessa_livro(self):
        print("\nTeste acessa_livro")

        define_livros([])

        livro = {
            "id_livro": 1,
            "nome": "Dom Casmurro",
            "autor": "Machado de Assis",
            "tags": ["romance", "classico"]
        }

        cria_livro(livro)

        resultado = acessa_livro(1)
        imprime_codigo(0)
        self.assertIsNotNone(resultado)

        resultado = acessa_livro(99)
        imprime_codigo(1)
        self.assertIsNone(resultado)

    def test_acessa_livros(self):
        print("\nTeste acessa_livros")

        define_livros([])

        resultado = acessa_livros()
        imprime_codigo(1)
        self.assertEqual(resultado, [])

        livro = {
            "id_livro": 2,
            "nome": "O Cortico",
            "autor": "Aluisio Azevedo",
            "tags": ["romance"]
        }

        cria_livro(livro)

        resultado = acessa_livros()
        imprime_codigo(0)
        self.assertNotEqual(resultado, [])

    def test_acessa_livros_por_tag(self):
        print("\nTeste acessa_livros_por_tag")

        define_livros([])

        livro = {
            "id_livro": 3,
            "nome": "Iracema",
            "autor": "Jose de Alencar",
            "tags": ["romance", "brasileiro"]
        }

        cria_livro(livro)

        resultado = acessa_livros_por_tag("romance")
        imprime_codigo(0)
        self.assertNotEqual(resultado, [])

        resultado = acessa_livros_por_tag("terror")
        imprime_codigo(1)
        self.assertEqual(resultado, [])

        resultado = acessa_livros_por_tag("")
        imprime_codigo(1)
        self.assertEqual(resultado, [])

    def test_cria_livro(self):
        print("\nTeste cria_livro")

        define_livros([])

        livro = {
            "id_livro": 4,
            "nome": "Memorias Postumas",
            "autor": "Machado de Assis",
            "tags": ["classico"]
        }

        resultado = cria_livro(livro)
        imprime_codigo(0)
        self.assertIsNotNone(resultado)

        resultado = cria_livro(livro)
        imprime_codigo(3)
        self.assertIsNone(resultado)

        livro_invalido = {
            "id_livro": "",
            "nome": "",
            "autor": "",
            "tags": []
        }

        resultado = cria_livro(livro_invalido)
        imprime_codigo(2)
        self.assertIsNone(resultado)

    def test_modifica_livro(self):
        print("\nTeste modifica_livro")

        define_livros([])

        livro = {
            "id_livro": 5,
            "nome": "Livro Antigo",
            "autor": "Autor Antigo",
            "tags": ["antigo"]
        }

        novo_livro = {
            "id_livro": 5,
            "nome": "Livro Novo",
            "autor": "Autor Novo",
            "tags": ["novo"]
        }

        cria_livro(livro)

        resultado = modifica_livro(5, novo_livro)
        imprime_codigo(0)
        self.assertIsNotNone(resultado)

        resultado = modifica_livro(99, novo_livro)
        imprime_codigo(1)
        self.assertIsNone(resultado)

        livro_invalido = {
            "id_livro": "",
            "nome": "",
            "autor": "",
            "tags": []
        }

        resultado = modifica_livro(5, livro_invalido)
        imprime_codigo(2)
        self.assertIsNone(resultado)

    def test_deleta_livro(self):
        print("\nTeste deleta_livro")

        define_livros([])

        livro = {
            "id_livro": 6,
            "nome": "Livro para Remover",
            "autor": "Autor",
            "tags": ["remover"]
        }

        cria_livro(livro)

        resultado = deleta_livro(6)
        imprime_codigo(0)
        self.assertIsNotNone(resultado)

        resultado = deleta_livro(99)
        imprime_codigo(1)
        self.assertIsNone(resultado)


unittest.main()