"""Módulo para gerenciamento de avaliações de livros."""

from copy import deepcopy
import json
import os


_avaliacoes = []
_proximo_id = 1
_ARQUIVO_DADOS = os.path.join("dados", "avaliacoes.json")

__all__ = [
    "acessa_avaliacao",
    "acessa_avaliacoes_livro",
    "acessa_avaliacoes_usuario",
    "cria_avaliacao",
    "modifica_avaliacao",
    "deleta_avaliacao",
    "calculaNotas",
    "carrega_dados",
    "salva_dados",
]


def _eh_dados_avaliacao_validos(avaliacao):
    """Valida os dados recebidos para criar ou modificar uma avaliação."""
    campos_obrigatorios = ["nota", "id_livro", "email"]

    if not isinstance(avaliacao, dict):
        return False

    if not all(campo in avaliacao for campo in campos_obrigatorios):
        return False

    nota = avaliacao["nota"]
    if not isinstance(nota, (int, float)) or nota < 0 or nota > 5:
        return False

    if not isinstance(avaliacao["id_livro"], int) or avaliacao["id_livro"] <= 0:
        return False

    email = avaliacao["email"]
    if not isinstance(email, str) or email.strip() == "":
        return False

    return True


def _eh_avaliacao_armazenada_valida(avaliacao):
    """Valida uma avaliação completa armazenada pelo módulo."""
    if not _eh_dados_avaliacao_validos(avaliacao):
        return False

    return (
        isinstance(avaliacao.get("id_avaliacao"), int)
        and avaliacao["id_avaliacao"] > 0
    )


def _gera_id_avaliacao():
    """Gera o próximo identificador de avaliação."""
    global _proximo_id
    id_avaliacao = _proximo_id
    _proximo_id = _proximo_id + 1
    return id_avaliacao


def acessa_avaliacao(id_avaliacao):
    """Consulta uma avaliação por seu identificador.

    Parâmetros:
        id_avaliacao: Identificador da avaliação procurada.

    Retorna:
        (0, avaliacao): Avaliação encontrada. O registro retornado é uma
            cópia.
        (1, None): Avaliação não encontrada.

    Efeito no TAD:
        Não altera as avaliações armazenadas.
    """
    for avaliacao in _avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            return 0, deepcopy(avaliacao)

    return 1, None


def acessa_avaliacoes_livro(id_livro):
    """Consulta todas as avaliações associadas a um livro.

    Parâmetros:
        id_livro: Identificador do livro procurado.

    Retorna:
        (0, avaliacoes): Lista com cópias das avaliações encontradas.
        (1, []): O livro não possui avaliações.

    Efeito no TAD:
        Não altera as avaliações armazenadas.
    """
    avaliacoes_livro = []
    for avaliacao in _avaliacoes:
        if avaliacao["id_livro"] == id_livro:
            avaliacoes_livro.append(deepcopy(avaliacao))

    if len(avaliacoes_livro) == 0:
        return 1, []

    return 0, avaliacoes_livro


def acessa_avaliacoes_usuario(email):
    """Consulta todas as avaliações feitas por um usuário.

    Parâmetros:
        email: E-mail do usuário procurado.

    Retorna:
        (0, avaliacoes): Lista com cópias das avaliações encontradas.
        (1, []): O usuário não possui avaliações.

    Efeito no TAD:
        Não altera as avaliações armazenadas.
    """
    avaliacoes_usuario = []
    for avaliacao in _avaliacoes:
        if avaliacao["email"] == email:
            avaliacoes_usuario.append(deepcopy(avaliacao))

    if len(avaliacoes_usuario) == 0:
        return 1, []

    return 0, avaliacoes_usuario


def cria_avaliacao(nova_avaliacao):
    """Cadastra ou atualiza a avaliação de um usuário para um livro.

    Parâmetros:
        nova_avaliacao: Dicionário com ``nota``, ``id_livro`` e ``email``.
            A nota deve estar entre 0 e 5; o ID do livro deve ser inteiro
            positivo; o e-mail deve ser um texto não vazio. O cliente não
            fornece ``id_avaliacao``.

    Retorna:
        0: Avaliação cadastrada ou atualizada.
        2: Dados inválidos.

    Efeito no TAD:
        Se não existir avaliação para o par ``(email, id_livro)``, cria um
        registro com novo ``id_avaliacao``. Se já existir, substitui seus dados
        e preserva o identificador anterior.
    """
    if not _eh_dados_avaliacao_validos(nova_avaliacao):
        return 2

    for indice, avaliacao in enumerate(_avaliacoes):
        if (
            avaliacao["email"] == nova_avaliacao["email"]
            and avaliacao["id_livro"] == nova_avaliacao["id_livro"]
        ):
            avaliacao_atualizada = {
                "nota": nova_avaliacao["nota"],
                "id_livro": nova_avaliacao["id_livro"],
                "email": nova_avaliacao["email"],
                "id_avaliacao": avaliacao["id_avaliacao"],
            }
            _avaliacoes[indice] = avaliacao_atualizada
            return 0

    avaliacao_cadastrada = {
        "nota": nova_avaliacao["nota"],
        "id_livro": nova_avaliacao["id_livro"],
        "email": nova_avaliacao["email"],
        "id_avaliacao": _gera_id_avaliacao(),
    }
    _avaliacoes.append(avaliacao_cadastrada)
    return 0


def modifica_avaliacao(id_avaliacao, nova_avaliacao):
    """Substitui os dados de uma avaliação identificada.

    Parâmetros:
        id_avaliacao: Identificador da avaliação que será modificada.
        nova_avaliacao: Dicionário com os novos valores de ``nota``,
            ``id_livro`` e ``email``.

    Retorna:
        0: Avaliação modificada.
        1: Avaliação não encontrada.
        2: Novos dados inválidos.
        7: A modificação produziria duas avaliações do mesmo usuário para o
            mesmo livro.

    Efeito no TAD:
        Em caso de sucesso, substitui os dados e preserva o
        ``id_avaliacao`` informado.
    """
    if not _eh_dados_avaliacao_validos(nova_avaliacao):
        return 2

    for indice, avaliacao in enumerate(_avaliacoes):
        if avaliacao["id_avaliacao"] == id_avaliacao:
            for outra_avaliacao in _avaliacoes:
                if (
                    outra_avaliacao["id_avaliacao"] != id_avaliacao
                    and outra_avaliacao["email"] == nova_avaliacao["email"]
                    and outra_avaliacao["id_livro"] == nova_avaliacao["id_livro"]
                ):
                    return 7

            avaliacao_atualizada = {
                "nota": nova_avaliacao["nota"],
                "id_livro": nova_avaliacao["id_livro"],
                "email": nova_avaliacao["email"],
                "id_avaliacao": id_avaliacao,
            }
            _avaliacoes[indice] = avaliacao_atualizada
            return 0

    return 1


def deleta_avaliacao(id_avaliacao):
    """Remove uma avaliação por seu identificador.

    Parâmetros:
        id_avaliacao: Identificador usado para localizar a avaliação.

    Retorna:
        0: Avaliação removida.
        1: Avaliação não encontrada.

    Efeito no TAD:
        Remove o registro encontrado.
    """
    for avaliacao in _avaliacoes:
        if avaliacao["id_avaliacao"] == id_avaliacao:
            _avaliacoes.remove(avaliacao)
            return 0

    return 1


def calculaNotas(id_livro):
    """Calcula a média aritmética das notas atribuídas a um livro.

    Parâmetros:
        id_livro: Identificador do livro cujas avaliações serão consideradas.

    Retorna:
        (0, nota): Média aritmética das notas, como inteiro ou ponto
            flutuante.
        (1, None): Não existem avaliações para o livro.

    Efeito no TAD:
        Não altera as avaliações armazenadas.
    """
    codigo, avaliacoes_livro = acessa_avaliacoes_livro(id_livro)
    if codigo != 0:
        return codigo, None

    soma = 0
    for avaliacao in avaliacoes_livro:
        soma = soma + avaliacao["nota"]

    return 0, soma / len(avaliacoes_livro)


def carrega_dados():
    """Inicializa o TAD com o conteúdo de ``dados/avaliacoes.json``.

    Também prepara a geração dos próximos identificadores de avaliação.

    Parâmetros:
        Nenhum.

    Retorna:
        0: Arquivo carregado ou arquivo ainda inexistente.
        2: Conteúdo com formato inválido, avaliação inválida ou
            ``id_avaliacao`` duplicado.

    Efeito no TAD:
        Limpa as avaliações atuais e reinicia a geração de IDs antes da
        leitura. Para registros repetidos do mesmo usuário e livro, mantém
        somente o último encontrado. O próximo ID será maior que todos os IDs
        carregados.

    Compatibilidade:
        Aceita um único objeto JSON no lugar de uma lista. Registros antigos
        sem ``nota`` são migrados conforme a regra implementada pelo módulo.

    Exceções:
        Erros de leitura e JSON malformado são propagados ao módulo cliente.
    """
    global _proximo_id
    _avaliacoes.clear()
    _proximo_id = 1

    if not os.path.exists(_ARQUIVO_DADOS):
        return 0

    with open(_ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if isinstance(dados, dict):
        dados = [dados]

    if not isinstance(dados, list):
        return 2

    ids_encontrados = set()
    for avaliacao in dados:
        if not isinstance(avaliacao, dict):
            _avaliacoes.clear()
            return 2

        avaliacao_carregada = deepcopy(avaliacao)
        if "nota" not in avaliacao_carregada:
            avaliacao_carregada["nota"] = avaliacao_carregada.get("id_avaliacao")
            avaliacao_carregada["id_avaliacao"] = _proximo_id

        if not _eh_avaliacao_armazenada_valida(avaliacao_carregada):
            _avaliacoes.clear()
            return 2

        id_avaliacao = avaliacao_carregada["id_avaliacao"]
        if id_avaliacao in ids_encontrados:
            _avaliacoes.clear()
            return 2

        ids_encontrados.add(id_avaliacao)
        avaliacao_carregada = {
            "nota": avaliacao_carregada["nota"],
            "id_livro": avaliacao_carregada["id_livro"],
            "email": avaliacao_carregada["email"],
            "id_avaliacao": id_avaliacao,
        }

        substituiu = False
        for indice, avaliacao_atual in enumerate(_avaliacoes):
            if (
                avaliacao_atual["email"] == avaliacao_carregada["email"]
                and avaliacao_atual["id_livro"] == avaliacao_carregada["id_livro"]
            ):
                _avaliacoes[indice] = avaliacao_carregada
                substituiu = True
                break

        if not substituiu:
            _avaliacoes.append(avaliacao_carregada)

        if id_avaliacao >= _proximo_id:
            _proximo_id = id_avaliacao + 1

    return 0


def salva_dados():
    """Persiste as avaliações encapsuladas em ``dados/avaliacoes.json``.

    Parâmetros:
        Nenhum.

    Retorna:
        0: Dados gravados.

    Efeito externo:
        Cria o diretório ``dados``, quando necessário, e substitui o conteúdo
        do arquivo pelo estado atual do TAD.

    Exceções:
        Erros do sistema de arquivos são propagados ao módulo cliente.
    """
    os.makedirs(os.path.dirname(_ARQUIVO_DADOS), exist_ok=True)
    with open(_ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(_avaliacoes, arquivo, ensure_ascii=False, indent=2)
    return 0
