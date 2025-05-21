# importa JSON, data e hora
import json
from datetime import datetime

# carrega os dados dos usuários do arquivo JSON
with open ("usuarios.json", "r") as arquivo:
    usuarios = json.load(arquivo)

# definir autenticação
# três tentativas de login, caso o email ou senha não funcionem o programa é encerrado
for i in range(3):
    login_entrada = input("Digite o login: ")
    senha_entrada = input("Digite a senha: ")

    # caso o login e senha digitados/inseridos sejam diferentes do que está no JSON
    for u in usuarios:
        if login_entrada != u["login"]:
            print("Login inválido.")
            continue
        
        if not u["ativo"]:
            break
        
        # se a senha estiver errada conta uma tentativa falha no dicionário
        if senha_entrada != u["senha"]:
            print("Senha incorreta.")
            u["tentativas_falhas"] += 1

            with open("usuarios.json", "w") as arq:
                json.dump(usuarios, arq, indent=4)

            break

        else:
            # printa caso o login e a senha estejam corretas, troca a data
            # e horário para a hora que foi logada
            print("Bem vindo!")
            u["ultimo_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usuario_logado = u
            break

# MENU ADMIN
if u["perfil"] == "admin":
    while True:
        print("\nMenu Admin:")
        print("1. Listar usuários")
        print("2. Trocar senha de alguém")
        print("3. Bloquear/desbloquear alguém")
        print("4. Cadastrar novo usuário")
        print("5. Sair")
        op = input("Escolha: ")

        if op == "1":
            for u in usuarios:
                print(f"- {u['nome']} ({u['login']}) [{u['perfil']}]")
        elif op == "2":
            alvo = input("Login do usuário: ")
            for u in usuarios:
                if u["login"] == alvo:
                    nova = input("Nova senha: ")
                    u["senha"] = nova
                    print("Senha trocada.")
                    break
        elif op == "3":
            alvo = input("Login do usuário: ")
            for u in usuarios:
                if u["login"] == alvo:
                    u["ativo"] = not u["ativo"]
                    print("Usuário desbloqueado." if u["ativo"] else "Usuário bloqueado.")
                    break
        elif op == "4":
            login_novo = input("Login do novo usuário: ")
            nome_novo = input("Nome: ")
            senha_nova = input("Senha: ")
            perfil_novo = input("Perfil (admin/user): ")
            novo = {
                "nome": nome_novo,
                "login": login_novo,
                "senha": senha_nova,
                "perfil": perfil_novo,
                "ultimo_login": "",
                "tentativas_falhas": 0,
                "ativo": True
            }
            usuarios.append(novo)
            print("Usuário cadastrado.")
        elif op == "5":
            break

        with open("usuarios.json", "w") as arq:
            json.dump(usuarios, arq, indent=4)

# MENU USER
if u["perfil"] == "user":
    while True:
        print("\nMenu Usuário:")
        print("1. Trocar minha senha")
        print("2. Sair")
        op = input("Escolha: ")

        if op == "1":
            nova = input("Nova senha: ")
            u["senha"] = nova
            print("Senha trocada.")
            with open("usuarios.json", "w") as arq:
                json.dump(usuarios, arq, indent=4)
        elif op == "2":
            break

