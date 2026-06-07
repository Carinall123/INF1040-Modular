# teste_avaliacoes.py - Testes para as funções do módulo avaliacoes.py
# teste-avaliacoes.py

# Convenção dos códigos de teste
# 0 - operação realizada com sucesso
# 1 - registro não encontrado  
# 3 - identificador já cadastrado
# 4 - livro inexistente
# 5 - usuário inexistente
# 6 - nota inválida
import unittest
from avaliacoes import *

class TesteAvaliacoes(unittest.TestCase):

    def setUp(self):
        global avaliacoes
        avaliacoes.clear()
        avaliacoes.update({
            "id_avaliacao": 4,
            "id_livro": 10,
            "id_user": 5
        })

    def test_01_acessa_avaliacao_encontrada_1(self):
        print("\nCaso de Teste 01 acessa_avaliacao - Avaliação encontrada")
        retorno = acessa_avaliacao(4)
        print("\nCódigo 0: Operação realizada com sucesso")
        self.assertEqual(retorno, 0)
        
        
    def test_02_acessa_avaliacao_nao_encontrada_2(self):
        print("\nCaso de Teste 02 acessa avalicao - Avaliação não encontrada")

        retorno = acessa_avaliacao(999)
        print("\nCódigo 1: Registro não encontrado")
        self.assertEqual(retorno, 1)
        

    def test_03_acessa_avaliacoes_livro_1(self):
        print("\nCaso de Teste 01 acessa_avaliacao_livro- Avaliações encontradas")

        retorno = acessa_avaliacoes_livro(10)
        print("\nCódigo 0: Operação realizada com sucesso")
        self.assertEqual(retorno, 0)


    #def test_04_acessa_avaliacoes_livro_2(self):
     #   print("\nCaso de Teste 02 acessa_avaliacao_livro - Livro sem avaliações")

       # retorno = acessa_avaliacoes_livro(10)
        #print("\nCódigo 1: Registro não encontrado")
        #self.assertEqual(retorno, 1)

    def test_05_acessa_avaliacoes_livro_3(self):
        print("\nCaso de Teste 03 acessa_avaliacao_livro - Livro inexistente")

        retorno = acessa_avaliacoes_livro(2)
        print("\nCódigo 4: Livro inexistente")
        self.assertEqual(retorno, 4)


    def test_06_acessa_avaliacoes_usuario_1(self):
        print("\nCaso de Teste 01 acessa_avaliacao_usuario - Avaliações encontradas")

        retorno = acessa_avaliacoes_usuario(5)
        print("\nCódigo 0: Operação realizada com sucesso")
        self.assertEqual(retorno, 0)
    
    #def test_07_acessa_avaliacoes_usuario_2(self):
       # print("\nCaso de Teste 02 acessa_avaliacao_usuario - Usuário sem avaliação")

        #retorno = acessa_avaliacoes_usuario(5)
        #print("\nCódigo 1: Registro não encontrado")
        #self.assertEqual(retorno, 1)

    def test_08_acessa_avaliacoes_usuario_3(self):
        print("\nCaso de Teste 03 acessa_avaliacao_usuario - Usuário inexistente")

        retorno = acessa_avaliacoes_usuario(2)
        print("\nCódigo 5: Usuário inexistente")
        self.assertEqual(retorno, 5)

    def test_09_cria_avaliacao_1(self):
        print("\nCaso de Teste 01 cria_avaliacao - Avaliação criada com sucesso")
        retorno = cria_avaliacao(avaliacoes)

        print("\nCódigo 0: Operação realizada com sucesso")
        self.assertEqual(retorno, 0)

    def test_10_cria_avaliacao_2(self):
        print("\nCaso de Teste 02 cria_avaliacao - Livro inexistente")

        retorno = cria_avaliacao(avaliacao2)
        print("\nCódigo 4: Livro inexistente")
        self.assertEqual(retorno, 4)

    def test_11_cria_avaliacao_3(self):
        print("\nCaso de Teste 03 cria_avaliacao - Usuário inexistente")

        retorno = cria_avaliacao(avaliacao3)
        print("Código 5: Usuário inexistente")
        self.assertEqual(retorno, 5)

    def test_12_cria_avaliacao_4(self):
        print("\nCaso de Teste 04 cria_avaliacao - Nota inválida")

        retorno = cria_avaliacao(avaliacao5)
        print("Código 6: Nota inválida")
        self.assertEqual(retorno, 6)

    def test_13_modifica_avaliacao_1(self):
        print("\nCaso de Teste 01 modifica_avaliacao - Avaliação modificada com sucesso")

        retorno = modifica_avaliacao(4,avaliacao2)
        self.assertEqual(retorno, 0)

    def test_14_modifica_avaliacao_2(self):
        print("\nCaso de Teste 02 modifica_avaliacao - Avaliação não encontrada")

        retorno = modifica_avaliacao(1, avaliacao2)
        self.assertEqual(retorno, 1)

    def test_15_modifica_avaliacao_3(self):
        print("\nCaso de Teste 03 modifica_avaliacao - Dados inválidos")

        retorno = modifica_avaliacao(4, avaliacao5)
        self.assertEqual(retorno, 2)
        
    def test_16_deleta_avaliacao_1(self): 
        print("\nCaso de Teste 01 deleta_avaliacao - Avaliação removida com sucesso")

        retorno = deleta_avaliacao(4)
        self.assertEqual(retorno, 0)
    
    def test_17_deleta_avaliacao_2(self): 
        print("\nCaso de Teste 02 deleta_avaliacao - Avaliação não encontrada")

        retorno = deleta_avaliacao(2)
        self.assertEqual(retorno, 1)
    
    def test_18_calculaNotas_1(self):
        print("\nCaso de Teste 01 calculaNotas - Nota calculada com sucesso")

        retorno = calculaNotas(10)
        self.assertEqual(retorno, 0)

    #def test_19_calculaNotas_2(self):
        #print("\nCaso de Teste 02 calculaNotas - Livro sem avaliações")

        #retorno = calculaNotas(10)
       # self.assertEqual(retorno, 1)

    def test_20_calculaNotas_3(self):
        print("\nCaso de Teste 03 calculaNotas - Livro inexistente")

        retorno = calculaNotas(2)
        self.assertEqual(retorno, 4)

if __name__ == "__main__":
    unittest.main()