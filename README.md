# Sistema de Livros - INF1040

Aplicação modular para cadastro de usuários, consulta de livros e registro de
avaliações. A interação com o usuário é realizada por `main.py`. Os dados são
mantidos em estruturas encapsuladas pelos módulos `usuarios.py`, `livro.py` e
`avaliacoes.py`.

O campo `email` é a chave primária de usuário e também a referência ao usuário
armazenada nas avaliações.

## Funções de acesso

A especificação completa de cada função de acesso está em sua docstring, no
início do corpo da própria função. Cada contrato informa:

- objetivo;
- parâmetros e formatos aceitos;
- códigos e valores de retorno;
- efeitos sobre o TAD ou sobre o arquivo;
- exceções e regras de compatibilidade, quando aplicáveis.

As funções públicas disponibilizadas são:

### `usuarios.py`

- `acessa_usuario(email)`
- `cria_usuario(novo_usuario)`
- `modifica_usuario(email, novo_usuario)`
- `deleta_usuario(email)`
- `carrega_dados()`
- `salva_dados()`

### `livro.py`

- `acessa_livro(nome_livro)`
- `acessa_livros()`
- `acessa_livros_por_tag(tag)`
- `cria_livro(novo_livro)`
- `modifica_livro(id_livro, novo_livro)`
- `deleta_livro(id_livro)`
- `carrega_dados()`
- `salva_dados()`

### `avaliacoes.py`

- `acessa_avaliacao(id_avaliacao)`
- `acessa_avaliacoes_livro(id_livro)`
- `acessa_avaliacoes_usuario(email)`
- `cria_avaliacao(nova_avaliacao)`
- `modifica_avaliacao(id_avaliacao, nova_avaliacao)`
- `deleta_avaliacao(id_avaliacao)`
- `calculaNotas(id_livro)`
- `carrega_dados()`
- `salva_dados()`

Os módulos clientes devem utilizar somente essas funções e não podem acessar
diretamente `_usuarios`, `_livros`, `_avaliacoes` ou `_proximo_id`.

## Formatos dos registros

### Usuário

```python
{
    "email": str,
    "senha": str
}
```

### Livro

```python
{
    "id_livro": int,
    "nome": str,
    "autor": str,
    "tags": list
}
```

### Avaliação

```python
{
    "id_avaliacao": int,
    "nota": int | float,
    "id_livro": int,
    "email": str
}
```

O campo `id_avaliacao` é controlado pelo módulo `avaliacoes.py` e não deve ser
informado pelo cliente ao criar uma avaliação.

## Persistência

Cada TAD lê exclusivamente seu próprio arquivo por meio de `carrega_dados()` e
o grava por meio de `salva_dados()`:

- `usuarios.py`: `dados/usuarios.json`
- `livro.py`: `dados/livros.json`
- `avaliacoes.py`: `dados/avaliacoes.json`

O módulo `main.py` chama essas interfaces no início e no final da execução, mas
não acessa diretamente os arquivos nem as estruturas internas dos TADs.

## Execução

```bash
python3 main.py
```

## Testes

Para executar toda a suíte automatizada:

```bash
python3 -m unittest -v
```
