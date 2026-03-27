from cliente import Cliente
from seguro import Automovel, Residencial, Vida
from apolice import Apolice
from sinistro import Sinistro
from utils import validar_cpf, validar_placa, salvar_dados, carregar_dados
from datetime import datetime
import getpass  # Para ocultar a senha

class SistemaSeguros:
    def __init__(self):
        self.clientes = [Cliente(
            c['nome'],
            c['cpf'],
            datetime.strptime(c['data_nascimento'], "%d/%m/%Y"),
            c['endereco'],
            c['telefone'],
            c['email']
        ) for c in carregar_dados("clientes.json")]
        self.seguros = carregar_dados("seguros.json")
        self.apolices = carregar_dados("apolices.json")
        self.sinistros = carregar_dados("sinistros.json")
        self.usuarios = carregar_dados("usuarios.json")
        if not self.usuarios:
            self.usuarios = {"admin": {"senha": "senha123", "tipo": "admin"}}
            salvar_dados("usuarios.json", self.usuarios)

    def salvar_todos_dados(self):
        salvar_dados("clientes.json", [c.to_dict() for c in self.clientes])
        salvar_dados("seguros.json", self.seguros)
        salvar_dados("apolices.json", self.apolices)
        salvar_dados("sinistros.json", self.sinistros)
        salvar_dados("usuarios.json", self.usuarios)

    def autenticar_usuario(self):
        print("Você já possui usuário e senha? (s/n)")
        while True:
            possui = input().strip().lower()
            if possui == 's':
                return self.login()
            elif possui == 'n':
                return self.cadastrar_usuario_e_login()
            else:
                print("Resposta inválida. Digite 's' para sim ou 'n' para não.")

    def login(self):
        while True:
            print("=== Login ===")
            usuario = input("Usuário: ").strip()
            senha = getpass.getpass("Senha: ")  # Oculta a senha
            if not usuario or not senha:
                print("Usuário e senha são obrigatórios.")
                continue
            if usuario in self.usuarios and self.usuarios[usuario]["senha"] == senha:
                self.usuario_atual = usuario
                self.tipo_usuario = self.usuarios[usuario]["tipo"]
                print(f"Login bem-sucedido! Tipo de usuário: {self.tipo_usuario}")
                return True
            else:
                print("Usuário ou senha inválidos. Tente novamente.")

    def cadastrar_usuario_e_login(self):
        print("=== Cadastro de novo usuário ===")
        while True:
            usuario = input("Digite o nome de usuário desejado: ").strip()
            if not usuario:
                print("Usuário não pode ser vazio.")
                continue
            if usuario in self.usuarios:
                print("Usuário já existe. Tente outro.")
                continue

            while True:
                senha = getpass.getpass("Digite a senha: ")  # Oculta a senha
                senha_confirm = getpass.getpass("Confirme a senha: ")  # Oculta a senha
                if not senha:
                    print("Senha não pode ser vazia.")
                    continue
                if senha != senha_confirm:
                    print("Senhas não conferem. Tente novamente.")
                    continue
                break

            while True:
                tipo = input("Digite o tipo de usuário ('usuario' para comum ou 'admin' para administrador): ").strip().lower()
                if tipo in ['usuario', 'admin']:
                    break
                else:
                    print("Tipo inválido. Digite 'usuario' ou 'admin'.")

            self.usuarios[usuario] = {"senha": senha, "tipo": tipo}
            self.salvar_todos_dados()
            print("Usuário cadastrado com sucesso! Faça login agora.")
            return self.login()

    def cadastrar_cliente(self):
        print("=== Cadastro de Cliente ===")
        while True:
            nome = input("Nome: ").strip()
            if nome:
                break
            print("Nome não pode ser vazio.")

        while True:
            cpf = input("CPF (somente números): ").strip()
            if validar_cpf(cpf):
                if any(c.cpf == cpf for c in self.clientes):
                    print("Cliente já cadastrado com esse CPF. Digite outro.")
                else:
                    break
            else:
                print("CPF inválido. Tente novamente.")

        while True:
            data_nasc_str = input("Data de nascimento (DD/MM/AAAA): ").strip()
            try:
                data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y")
                if data_nasc > datetime.now():
                    print("Data de nascimento não pode ser no futuro. Tente novamente.")
                else:
                    break
            except ValueError:
                print("Formato inválido da data. Use DD/MM/AAAA.")

        while True:
            telefone = input("Telefone (somente números): ").strip()
            if len(telefone) < 11 or not telefone.isdigit():
                print("Telefone inválido. Deve conter pelo menos 11 dígitos numéricos.")
                continue
            if any(c.telefone == telefone for c in self.clientes):
                print("Telefone já cadastrado. Tente outro.")
                continue
            break

        while True:
            email = input("E-mail: ").strip()
            if not email:
                print("E-mail não pode ser vazio.")
                continue
            if any(c.email == email for c in self.clientes):
                print("E-mail já cadastrado. Tente outro.")
                continue
            break

        while True:
            endereco = input("Endereço: ").strip()
            if endereco:
                break
            print("Endereço é obrigatório. Por favor, preencha.")

        cliente = Cliente(nome, cpf, data_nasc, endereco, telefone, email)
        self.clientes.append(cliente)
        self.salvar_todos_dados()
        print("Cliente cadastrado com sucesso!")

    def cadastrar_seguro(self):
        print("=== Cadastro de Seguro ===")
        while True:
            cpf = input("CPF do cliente: ").strip()
            cliente = next((c for c in self.clientes if c.cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado. Cadastre o cliente primeiro.")
            else:
                break

        idade_cliente = (datetime.now() - cliente.data_nasc).days // 365

        while True:
            tipo = input("Tipo de Seguro (Automóvel, Residencial, Vida): ").strip().capitalize()
            if tipo in ["Automóvel", "Residencial", "Vida"]:
                break
            else:
                print("Tipo de seguro inválido. Escolha Automóvel, Residencial ou Vida.")

        if tipo == "Automóvel" and idade_cliente < 18:
            print("É necessário ser maior de idade para contratar um seguro de automóvel.")
            return

        if tipo == "Vida" and idade_cliente < 18:
            print("Menores de 18 anos podem contratar seguro de vida apenas com a assistência de um responsável.")
            responsavel = input("O responsável está presente? (s/n): ").strip().lower()
            if responsavel != 's':
                print("Cadastro de seguro de vida não permitido sem responsável.")
                return

        dados = {}
        if tipo == "Residencial":
            usar_endereco_cliente = input("Usar o endereço do cliente? (s/n): ").strip().lower()
            if usar_endereco_cliente == "s":
                endereco = cliente.endereco
            else:
                while True:
                    endereco = input("Endereço: ").strip()
                    if endereco:
                        break
                    print("Endereço é obrigatório. Por favor, preencha.")

            while True:
                valor_str = input("Valor do imóvel (ex: 150000.00): ").strip().replace(',', '.')
                try:
                    valor = float(valor_str)
                    valor = round(valor, 2)
                    break
                except ValueError:
                    print("Valor inválido. Digite um número válido com até 2 casas decimais.")
            seguro_obj = Residencial(endereco, valor)
            dados = seguro_obj.dados

        elif tipo == "Vida":
            while True:
                valor_segurado_str = input("Valor Segurado (ex: 100000.00): ").strip().replace(',', '.')
                try:
                    valor_segurado = float(valor_segurado_str)
                    valor_segurado = round(valor_segurado, 2)
                    break
                except ValueError:
                    print("Valor inválido. Digite um número válido com até 2 casas decimais.")
            beneficiarios = input("Beneficiários (separados por vírgula): ").strip()
            lista_benef = [b.strip() for b in beneficiarios.split(",")] if beneficiarios else []
            seguro_obj = Vida(valor_segurado, lista_benef)
            dados = seguro_obj.dados

        elif tipo == "Automóvel":
            while True:
                modelo = input("Modelo: ").strip()
                if modelo:
                    break
                print("Modelo é obrigatório.")

            while True:
                ano = input("Ano: ").strip()
                if ano:
                    break
                print("Ano é obrigatório.")

            while True:
                placa = input("Placa: ").strip().upper()
                if validar_placa(placa):
                    break
                else:
                    print("Placa inválida. Use o formato ABC1234 ou ABC1D23.")

            seguro_obj = Automovel(modelo, ano, placa)
            dados = seguro_obj.dados

        seguro_dict = {
            "cpf_cliente": cpf,
            "tipo": tipo,
            "dados": dados
        }

        self.seguros.append(seguro_dict)
        self.salvar_todos_dados()
        print("Seguro cadastrado com sucesso!")

    def emitir_apolice(self):
        print("=== Emissão de Apólice ===")
        while True:
            cpf_cliente = input("CPF do cliente: ").strip()
            cliente = next((c for c in self.clientes if c.cpf == cpf_cliente), None)
            if not cliente:
                print("Cliente não encontrado. Tente novamente.")
                continue
            break

        seguros_cliente = [s for s in self.seguros if s.get('cpf_cliente') == cpf_cliente]
        if not seguros_cliente:
            print("Este cliente não possui seguros cadastrados.")
            return

        print("Tipos de seguro disponíveis:")
        for i, s in enumerate(seguros_cliente):
            print(f"{i+1}: {s['tipo']} - {s['dados']}")

        while True:
            try:
                escolha = int(input("Escolha o número do seguro: ").strip())
                if 1 <= escolha <= len(seguros_cliente):
                    break
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

        seguro = seguros_cliente[escolha - 1]
        numero_apolice = len(self.apolices) + 1

        valor_mensal = 0
        tipo = seguro['tipo']
        dados = seguro['dados']

        if tipo == "Automóvel":
            valor_mensal = 200.0
        elif tipo == "Residencial":
            valor_mensal = dados.get('valor', 0) * 0.005
        elif tipo == "Vida":
            valor_mensal = dados.get('valor_segurado', 0) * 0.01

        apolice = {
            "numero": numero_apolice,
            "cliente_cpf": cpf_cliente,
            "tipo_seguro": tipo,
            "dados_seguro": dados,
            "valor_mensal": round(valor_mensal, 2),
            "data_emissao": datetime.now().strftime("%d/%m/%Y")
        }
        self.apolices.append(apolice)
        self.salvar_todos_dados()
        print(f"Apolice emitida com sucesso! Número: {numero_apolice}")

    def registrar_sinistro(self):
        print("=== Registro de Sinistro ===")
        while True:
            cpf = input("Informe o CPF do cliente: ").strip()
            cliente = next((c for c in self.clientes if c.cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado.")
            else:
                break

        while True:
            try:
                numero_apolice = int(input("Número da Apólice: ").strip())
                break
            except ValueError:
                print("Número inválido. Digite um número válido.")
        apolice = next((a for a in self.apolices if a['numero'] == numero_apolice), None)
        if not apolice:
            print("Apólice não encontrada.")
            return

        descricao = input("Descrição do ocorrido: ").strip()
        while True:
            data = input("Data do sinistro (DD/MM/AAAA): ").strip()
            try:
                data_sinistro = datetime.strptime(data, "%d/%m/%Y")
                if data_sinistro > datetime.now():
                    print("A data do sinistro não pode ser no futuro.")
                else:
                    break
            except ValueError:
                print("Data inválida. Use o formato DD/MM/AAAA.")

        sinistro = {
            "numero_apolice": numero_apolice,
            "descricao": descricao,
            "data": data,
            "status": "aberto"
        }
        self.sinistros.append(sinistro)
        self.salvar_todos_dados()
        print("Sinistro registrado com sucesso!")

    def relatorios(self):
        while True:
            print("\n=== Relatórios ===")
            print("1 - Valor total segurado por cliente")
            print("2 - Apólices emitidas por tipo de seguro")
            print("3 - Quantidade de sinistros abertos/fechados")
            print("0 - Voltar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                print("\n--- Valor total segurado por cliente ---")
                for cliente in self.clientes:
                    total = sum(
                        apolice['valor_mensal'] * 12  # valor anual
                        for apolice in self.apolices
                        if apolice['cliente_cpf'] == cliente.cpf
                    )
                    print(f"{cliente.nome} ({cliente.cpf}): R$ {total:.2f}")

            elif opcao == '2':
                print("\n--- Apólices por tipo de seguro ---")
                contagem = {"Automóvel": 0, "Residencial": 0, "Vida": 0}
                for apolice in self.apolices:
                    tipo = apolice['tipo_seguro']
                    if tipo in contagem:
                        contagem[tipo] += 1
                for tipo, qtd in contagem.items():
                    print(f"{tipo}: {qtd} apólices")

            elif opcao == '3':
                print("\n--- Sinistros por status ---")
                abertos = sum(1 for s in self.sinistros if s['status'] == 'aberto')
                fechados = sum(1 for s in self.sinistros if s['status'] == 'fechado')
                print(f"Abertos: {abertos}")
                print(f"Fechados: {fechados}")

            elif opcao == '0':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def alterar_dados_cliente(self):
        if self.tipo_usuario != "admin":
            print("Acesso negado. Apenas administradores podem alterar dados de clientes.")
            return

        print("=== Alterar Dados do Cliente ===")
        cpf = input("Informe o CPF do cliente: ").strip()
        cliente = next((c for c in self.clientes if c.cpf == cpf), None)
        if not cliente:
            print("Cliente não encontrado.")
            return

        while True:
            print("1 - Alterar Telefone")
            print("2 - Alterar E-mail")
            print("3 - Voltar")
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                while True:
                    novo_telefone = input("Novo Telefone: ").strip()
                    if novo_telefone:
                        cliente.telefone = novo_telefone
                        self.salvar_todos_dados()
                        print("Telefone alterado com sucesso.")
                        break
                    print("Telefone não pode estar vazio.")
            elif opcao == "2":
                while True:
                    novo_email = input("Novo E-mail: ").strip()
                    if novo_email:
                        cliente.email = novo_email
                        self.salvar_todos_dados()
                        print("E-mail alterado com sucesso.")
                        break
                    print("E-mail não pode estar vazio.")
            elif opcao == "3":
                break
            else:
                print("Opção inválida.")

    def cancelar_apolice(self):
        if self.tipo_usuario != "admin":
            print("Acesso negado. Apenas administradores podem cancelar apólices.")
            return

        print("=== Cancelar Apólice ===")
        while True:
            try:
                numero_apolice = int(input("Número da Apólice: ").strip())
                break
            except ValueError:
                print("Número inválido.")
        apolice = next((a for a in self.apolices if a['numero'] == numero_apolice), None)
        if not apolice:
            print("Apólice não encontrada.")
            return

        confirmacao = input("Tem certeza que deseja cancelar esta apólice? (s/n): ").strip().lower()
        if confirmacao == 's':
            self.apolices.remove(apolice)
            self.salvar_todos_dados()
            print("Apólice cancelada com sucesso.")
        else:
            print("Cancelamento da apólice abortado.")

    def atualizar_status_sinistro(self):
        if self.tipo_usuario != "admin":
            print("Acesso negado. Apenas administradores podem atualizar status de sinistro.")
            return

        print("=== Atualizar Status de Sinistro ===")
        while True:
            try:
                numero_apolice = int(input("Número da Apólice: ").strip())
                break
            except ValueError:
                print("Número inválido.")

        sinistro = next((s for s in self.sinistros if s['numero_apolice'] == numero_apolice), None)
        if not sinistro:
            print("Sinistro não encontrado.")
            return

        while True:
            novo_status = input("Novo status (aberto/fechado): ").strip().lower()
            if novo_status in ["aberto", "fechado"]:
                sinistro['status'] = novo_status
                self.salvar_todos_dados()
                print("Status do sinistro atualizado com sucesso.")
                break
            else:
                print("Status inválido.")

