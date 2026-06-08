"""Testes para as funções do módulo usuarios.py."""

import os
import tempfile
import unittest

from usuarios import *
import usuarios as modulo_usuarios


def imprime_codigo(codigo):
    mensagens = {
        0: "Operação realizada com sucesso",
        1: "Registro não encontrado",
        2: "Dados inválidos",
        3: "Identificador já cadastrado",
    }

    print(f"Código {codigo}: {mensagens[codigo]}")


class TesteUsuarios(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.arquivo_original = modulo_usuarios.ARQUIVO_DADOS
        modulo_usuarios.ARQUIVO_DADOS = os.path.join(
            self.tempdir.name, "usuarios.json"
        )
        modulo_usuarios.usuarios.clear()

    def tearDown(self):
        modulo_usuarios.ARQUIVO_DADOS = self.arquivo_original
        modulo_usuarios.usuarios.clear()
        self.tempdir.cleanup()

    def test_01_acessa_usuario_encontrado(self):
        print("\nCaso de Teste 01 acessa_usuario - Usuário encontrado")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo, usuario = acessa_usuario("u1")

        imprime_codigo(codigo)
        self.assertEqual(codigo, 0)
        self.assertEqual(usuario["email"], "u1@email.com")

    def test_02_acessa_usuario_nao_encontrado(self):
        print("\nCaso de Teste 02 acessa_usuario - Usuário não encontrado")

        codigo, usuario = acessa_usuario("inexistente")

        imprime_codigo(codigo)
        self.assertEqual(codigo, 1)
        self.assertIsNone(usuario)

    def test_03_cria_usuario_com_sucesso(self):
        print("\nCaso de Teste 03 cria_usuario - Usuário criado com sucesso")

        codigo = cria_usuario(
            {"id_user": "u1", "email": "u1@email.com", "senha": "123"}
        )

        imprime_codigo(codigo)
        self.assertEqual(codigo, 0)

    def test_04_cria_usuario_duplicado(self):
        print("\nCaso de Teste 04 cria_usuario - Identificador já cadastrado")
        usuario = {"id_user": "u1", "email": "u1@email.com", "senha": "123"}
        cria_usuario(usuario)

        codigo = cria_usuario(usuario)

        imprime_codigo(codigo)
        self.assertEqual(codigo, 3)

    def test_05_cria_usuario_dados_invalidos(self):
        print("\nCaso de Teste 05 cria_usuario - Dados inválidos")

        codigo = cria_usuario({"id_user": "", "email": "", "senha": ""})

        imprime_codigo(codigo)
        self.assertEqual(codigo, 2)

    def test_06_modifica_usuario_com_sucesso(self):
        print("\nCaso de Teste 06 modifica_usuario - Usuário modificado")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo = modifica_usuario(
            "u1", {"id_user": "u1", "email": "novo@email.com", "senha": "456"}
        )
        codigo_consulta, usuario = acessa_usuario("u1")

        imprime_codigo(codigo)
        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(usuario["email"], "novo@email.com")

    def test_07_modifica_usuario_nao_encontrado(self):
        print("\nCaso de Teste 07 modifica_usuario - Usuário não encontrado")

        codigo = modifica_usuario(
            "u1", {"id_user": "u1", "email": "u1@email.com", "senha": "123"}
        )

        imprime_codigo(codigo)
        self.assertEqual(codigo, 1)

    def test_08_modifica_usuario_dados_invalidos(self):
        print("\nCaso de Teste 08 modifica_usuario - Dados inválidos")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo = modifica_usuario(
            "u1", {"id_user": "", "email": "", "senha": ""}
        )

        imprime_codigo(codigo)
        self.assertEqual(codigo, 2)

    def test_09_deleta_usuario_com_sucesso(self):
        print("\nCaso de Teste 09 deleta_usuario - Usuário removido")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo = deleta_usuario("u1")

        imprime_codigo(codigo)
        self.assertEqual(codigo, 0)

    def test_10_deleta_usuario_nao_encontrado(self):
        print("\nCaso de Teste 10 deleta_usuario - Usuário não encontrado")

        codigo = deleta_usuario("u1")

        imprime_codigo(codigo)
        self.assertEqual(codigo, 1)

    def test_11_persistencia_de_dados(self):
        print("\nCaso de Teste 11 usuários - Persistência de dados")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo_salva = salva_dados()
        modulo_usuarios.usuarios.clear()
        codigo_carrega = carrega_dados()
        codigo_consulta, usuario = acessa_usuario("u1")

        self.assertEqual(codigo_salva, 0)
        self.assertEqual(codigo_carrega, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(usuario["email"], "u1@email.com")

    def test_12_retorna_usuarios(self):
        print("\nCaso de Teste 12 retorna_usuarios - Usuários cadastrados")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        lista = retorna_usuarios()

        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["id_user"], "u1")


if __name__ == "__main__":
    unittest.main()
