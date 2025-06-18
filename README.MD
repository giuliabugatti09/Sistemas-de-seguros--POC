# Sistema de Gestão de Apólices de Seguro

## 📌 Visão Geral
Sistema Python para gestão completa de apólices de seguro, agora refatorado com:
- **Programação Orientada a Objetos**
- **Autenticação básica de usuários**
- **Relatórios avançados**
- **Persistência em JSON**

## 🚀 Funcionalidades Principais

### 1. **Estrutura OO Completa**
```python
├── Cliente
├── Seguro (Superclasse)
│   ├── Automovel
│   ├── Residencial
│   └── Vida
├── Apolice
├── Sinistro
└── SistemaSeguros (Controlador)
```

### 2. Sistema de Autenticação
- Dois níveis de acesso:
  - **Usuário:** Apenas consulta
  - **Administrador:** Cadastro/edição completa

### 3. Relatórios Avançados
```markdown
- Valor total segurado por cliente
- Apólices por tipo de seguro
- Status de sinistros (abertos/fechados)
- Ranking de clientes
```

### 4. Gerenciamento de Dados
- ✅ Edição de cadastros
- 🚫 Cancelamento de apólices (com confirmação)
- 🔄 Atualização de status

## 🛠️ Estrutura Técnica

### Arquitetura Modular
```bash
sistema_seguros/
├── main.py            # Interface principal
├── sistema.py         # Controlador
├── cliente.py         # Classe Cliente
├── seguro.py          # Classes de Seguro
├── apolice.py         # Classe Apólice
├── sinistro.py        # Classe Sinistro
├── utils.py           # Funções auxiliares
├── data/
│   ├── clientes.json
│   ├── apolices.json
│   ├── seguros.json
│   └── sinistros.json
└── requirements.txt
```

### Validações Implementadas
- ✔️ CPF (algoritmo real)
- ✔️ Datas (formato e consistência)
- ✔️ Campos obrigatórios

## ⚙️ Pré-requisitos
- Python 3.8+
- Bibliotecas:
  ```bash
  pip install -r requirements.txt
  ```

## 🖥️ Como Executar
1. Clone o repositório
2. Instale as dependências
3. Execute:
   ```bash
   python main.py
   ```
4. Use as credenciais:
   - Admin: `admin/senha123`
   - Usuário: `user/user123`
*Ou crie seu próprio usuário

## 📊 Exemplo de Uso
```python
# Criando novo seguro
from seguro import Automovel

carro = Automovel(
    modelo="Fiat Uno",
    placa="ABC1D23",
    valor_segurado=25000.00
)
```

## 📝 Próximas Etapas
- [ ] Integração com API de consulta CPF
- [ ] Geração de PDF para apólices
- [ ] Dashboard web básico

## 🤝 Contribuição
Contribuições são bem-vindas! Abra issues ou envie PRs.

---
Desenvolvido por Giulia Bugatti - FIAP 2024
