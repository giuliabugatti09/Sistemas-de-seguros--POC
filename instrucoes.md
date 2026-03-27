# Sistema de Seguros

## Instruções de Uso

Este sistema permite gerenciar clientes, seguros, apólices e sinistros com funcionalidades de cadastro, autenticação, emissão de apólices, registro de sinistros e relatórios. O sistema possui controle de permissões para usuários comuns e administradores.

### Como rodar

1. Certifique-se de ter o Python 3 instalado na sua máquina.
2. Garanta que os arquivos JSON (clientes.json, seguros.json, apolices.json, sinistros.json, usuarios.json) estejam no mesmo diretório do script para armazenar os dados.
3. Rode o script principal que contém a classe `SistemaSeguros`.
4. Ao iniciar, será solicitado que você faça login ou cadastre um usuário.
5. Navegue pelo menu para acessar as diferentes funcionalidades.

### Funcionalidades principais

- Cadastro e autenticação de usuários (com senha oculta).
- Cadastro de clientes com validação de CPF, telefone e e-mail.
- Cadastro de seguros: Automóvel, Residencial e Vida (com validações específicas de idade e dados).
- Emissão de apólices vinculadas a clientes e seguros.
- Registro e atualização de sinistros.
- Geração de relatórios diversificados.
- Alteração de dados de clientes (só para administradores).
- Cancelamento de apólices (só para administradores).

## Estrutura de Arquivos

- `sistema_seguros.py`: Código principal com a classe `SistemaSeguros` contendo toda a lógica do sistema.
- `cliente.py`: Definição da classe Cliente.
- `seguro.py`: Definição das classes de seguros: Automovel, Residencial, Vida.
- `apolice.py`: Definição da classe Apolice.
- `sinistro.py`: Definição da classe Sinistro.
- `utils.py`: Funções auxiliares para validação (CPF, placa) e manipulação de arquivos JSON.
- Arquivos de dados JSON:
  - `clientes.json`
  - `seguros.json`
  - `apolices.json`
  - `sinistros.json`
  - `usuarios.json`

## Requisitos para Execução

- Python 3.x (preferencialmente Python 3.6 ou superior)
- Biblioteca padrão do Python (nenhuma biblioteca externa é requerida)

Para rodar o sistema, execute o script principal que instancia e interage com a classe `SistemaSeguros`. O sistema utiliza entrada via terminal para todas as interações com o usuário.

---
Este sistema foi desenvolvido para ser utilizado via linha de comando e visa facilitar a gestão de seguros com validações e controles adequados.
