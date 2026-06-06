# INF1040-Modular

## Contrato de persistência dos módulos

Cada TAD (`usuarios.py`, `livro.py` e `avaliacoes.py`) deve disponibilizar:

- `carrega_dados()`: lê o arquivo do próprio módulo no início da aplicação e
  armazena os dados em sua estrutura encapsulada.
- `salva_dados()`: grava a estrutura encapsulada no arquivo do próprio módulo
  ao final da aplicação.

O módulo `main.py` apenas chama essas funções. Ele não abre nem altera
diretamente os arquivos ou as estruturas internas dos outros módulos.
