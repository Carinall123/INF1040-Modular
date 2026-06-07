# Convenção dos Códigos de Retorno
# 0: operação realizada com sucesso 
# 1: registro não encontrado
# 2: dados inválidos
# 3: identificador já cadastrado 
# 4: livro inexistente 
# 5: usuário inexistente 
# 6: nota inválida
# 7: operação não permitida 

# MOCK TEMPORÁRIO
######
avaliacoes = {
        "id_avaliacao": 4,
        "id_livro": 10,
        "id_user": 5
    }
avaliacao2 = {
        "id_avaliacao": 2,
        "id_livro": 1,
        "id_user": 5
}
avaliacao3 = {
        "id_avaliacao": 2,
        "id_livro": 10,
        "id_user": 1
}
avaliacao4 = {
        "id_avaliacao": 2,
        "id_livro": 10,
        "id_user": 1
}
avaliacao5 = {
        "id_avaliacao": -2,
        "id_livro": 10,
        "id_user": 5
}
livros = {10}
usuarios = {5}

def acessa_avaliacao(id_avaliacao):
    """Retorna uma avaliação a partir do seu ID."""
    if avaliacoes["id_avaliacao"] == id_avaliacao:
        return 0
    return 1

def acessa_avaliacoes_livro(id_livro):
    """Retorna todas as avaliações associadas a um livro."""
    if avaliacoes["id_livro"] != id_livro:
        return 4
    if acessa_avaliacao(4) != 0: #precisa alterar
        return 1
    else:
        return 0
       

def acessa_avaliacoes_usuario(id_user):
    """Retorna todas as avaliações feitas por um usuário."""
    if avaliacoes["id_user"] != id_user:
        return 5
    if acessa_avaliacao(4) != 0: #precisa alterar
        return 1
    else:
        return 0

def cria_avaliacao(nova_avaliacao):
    """Cadastra uma nova avaliação para um livro."""
    if nova_avaliacao["id_livro"] not in livros:
        return 4

    if nova_avaliacao["id_user"] not in usuarios:
        return 5

    if nova_avaliacao["id_avaliacao"] <= -1 or nova_avaliacao["id_avaliacao"] > 5:
        return 6

    return 0

def modifica_avaliacao(id_avaliacao, nova_avaliacao): 
    """Modifica uma avaliação já cadastrada."""
    if avaliacoes["id_avaliacao"] != id_avaliacao:
        return 1

    if nova_avaliacao["id_avaliacao"] >= 6 or nova_avaliacao["id_avaliacao"] < 0 :
        return 2

    avaliacoes["id_avaliacao"] = nova_avaliacao
    return 0

def deleta_avaliacao(id_avaliacao): 
    """Remove uma avaliação cadastrada."""
    if avaliacoes["id_avaliacao"] == id_avaliacao:
        avaliacoes["id_avaliacao"] = None
        return 0
    return 1

def calculaNotas(id_livro):
    """Calcula a nota de um livro a partir das avaliações cadastradas."""
    resultado = acessa_avaliacoes_livro(id_livro)

    if resultado == 1:
        return 1

    if resultado == 4:
        return 4

    return 0