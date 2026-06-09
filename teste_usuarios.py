"""Testes automatizados do módulo usuarios com unittest."""

import json
import os
import tempfile
import unittest

from usuarios import (
    acessa_usuario,
    carrega_dados,
    cria_usuario,
    deleta_usuario,
    modifica_usuario,
    salva_dados,
)


class TesteUsuarios(unittest.TestCase):
    """Testes das funções de acesso do módulo usuarios."""

    def setUp(self):
        self.diretorio_original = os.getcwd()
        self.tempdir = tempfile.TemporaryDirectory()
        os.chdir(self.tempdir.name)
        carrega_dados()

    def tearDown(self):
        os.chdir(self.diretorio_original)
        self.tempdir.cleanup()

    def test_01_acessa_usuario_encontrado(self):
        print("\nCaso de Teste 01 acessa_usuario - Usuário encontrado")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo, usuario = acessa_usuario("u1")

        self.assertEqual(codigo, 0)
        self.assertEqual(usuario["email"], "u1@email.com")

    def test_02_acessa_usuario_nao_encontrado(self):
        print("\nCaso de Teste 02 acessa_usuario - Usuário não encontrado")

        codigo, usuario = acessa_usuario("inexistente")

        self.assertEqual(codigo, 1)
        self.assertIsNone(usuario)

    def test_03_cria_usuario_com_sucesso(self):
        print("\nCaso de Teste 03 cria_usuario - Usuário criado com sucesso")

        codigo = cria_usuario(
            {"id_user": "u1", "email": "u1@email.com", "senha": "123"}
        )

        self.assertEqual(codigo, 0)

    def test_04_cria_usuario_duplicado(self):
        print("\nCaso de Teste 04 cria_usuario - Identificador já cadastrado")
        usuario = {"id_user": "u1", "email": "u1@email.com", "senha": "123"}
        cria_usuario(usuario)

        codigo = cria_usuario(usuario)

        self.assertEqual(codigo, 3)

    def test_05_cria_usuario_dados_invalidos(self):
        print("\nCaso de Teste 05 cria_usuario - Dados inválidos")

        codigo = cria_usuario({"id_user": "", "email": "", "senha": ""})

        self.assertEqual(codigo, 2)

    def test_06_modifica_usuario_com_sucesso(self):
        print("\nCaso de Teste 06 modifica_usuario - Usuário modificado")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo = modifica_usuario(
            "u1",
            {"id_user": "u1", "email": "novo@email.com", "senha": "456"},
        )
        codigo_consulta, usuario = acessa_usuario("u1")

        self.assertEqual(codigo, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(usuario["email"], "novo@email.com")

    def test_07_modifica_usuario_nao_encontrado(self):
        print("\nCaso de Teste 07 modifica_usuario - Usuário não encontrado")

        codigo = modifica_usuario(
            "u1",
            {"id_user": "u1", "email": "u1@email.com", "senha": "123"},
        )

        self.assertEqual(codigo, 1)

    def test_08_modifica_usuario_dados_invalidos(self):
        print("\nCaso de Teste 08 modifica_usuario - Dados inválidos")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo = modifica_usuario(
            "u1",
            {"id_user": "", "email": "", "senha": ""},
        )

        self.assertEqual(codigo, 2)

    def test_09_deleta_usuario_com_sucesso(self):
        print("\nCaso de Teste 09 deleta_usuario - Usuário removido")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo = deleta_usuario("u1")

        self.assertEqual(codigo, 0)

    def test_10_deleta_usuario_nao_encontrado(self):
        print("\nCaso de Teste 10 deleta_usuario - Usuário não encontrado")

        codigo = deleta_usuario("u1")

        self.assertEqual(codigo, 1)

    def test_11_persistencia_de_dados(self):
        print("\nCaso de Teste 11 usuários - Persistência de dados")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        codigo_salva = salva_dados()
        carrega_dados()
        codigo_consulta, usuario = acessa_usuario("u1")

        self.assertEqual(codigo_salva, 0)
        self.assertEqual(codigo_consulta, 0)
        self.assertEqual(usuario["email"], "u1@email.com")

    def test_12_consulta_retorna_copia(self):
        print("\nCaso de Teste 12 usuários - Encapsulamento")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})

        _codigo, usuario = acessa_usuario("u1")
        usuario["email"] = "alterado@email.com"
        _codigo, usuario_armazenado = acessa_usuario("u1")

        self.assertEqual(usuario_armazenado["email"], "u1@email.com")

    def test_13_modifica_usuario_rejeita_email_duplicado(self):
        print("\nCaso de Teste 13 - Rejeitar e-mail duplicado")
        cria_usuario({"id_user": "u1", "email": "u1@email.com", "senha": "123"})
        cria_usuario({"id_user": "u2", "email": "u2@email.com", "senha": "123"})

        codigo = modifica_usuario(
            "u2",
            {"id_user": "u2", "email": "u1@email.com", "senha": "456"},
        )

        self.assertEqual(codigo, 3)

    def test_14_carrega_dados_invalidos(self):
        print("\nCaso de Teste 14 - Arquivo de usuários inválido")
        os.makedirs("dados", exist_ok=True)
        with open("dados/usuarios.json", "w", encoding="utf-8") as arquivo:
            json.dump({"conteudo": "invalido"}, arquivo)

        codigo = carrega_dados()

        self.assertEqual(codigo, 2)


if __name__ == "__main__":
    unittest.main()
