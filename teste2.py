# importa JSON, data e hora
import json
from datetime import datetime

# carrega os dados dos usuários do arquivo JSON
with open("usuarios.json", "r") as arquivo:
    usuarios = json.load(arquivo)

# definir autenticação
# três tentativas de login, caso o email ou senha não funcionem o programa é encerrado
for i in range(3):
    login_entrada = input("Digite o login: ")
    senha_entrada = input("Digite a senha: ")

    # caso o login e senha digitados/inseridos sejam diferentes do que está no JSON
    for u in usuarios:
        if login_entrada != u["login"]:
            continue  # tenta o próximo usuário

        # caso tenha encontrado o login, passa para a senha
        if not u["ativo"]:
            print("Usuário bloqueado.")
            break

        if senha_entrada != u["senha"]:
            print("Senha incorreta.")
            u["tentativas_falhas"] += 1
            break

        # login e senha corretos
        print("Bem-vindo!")
        u["ultimo_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        u["tentativas_falhas"] = 0

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
                    for x in usuarios:
                        print(f"- {x['nome']} ({x['login']}) [{x['perfil']}]")
                elif op == "2":
                    alvo = input("Login do usuário: ")
                    for x in usuarios:
                        if x["login"] == alvo:
                            nova = input("Nova senha: ")
                            x["senha"] = nova
                            print("Senha trocada.")
                            break
                elif op == "3":
                    alvo = input("Login do usuário: ")
                    for x in usuarios:
                        if x["login"] == alvo:
                            x["ativo"] = not x["ativo"]
                            print("Usuário desbloqueado." if x["ativo"] else "Usuário bloqueado.")
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
        elif u["perfil"] == "user":
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

        # salva login bem-sucedido e sai do programa
        with open("usuarios.json", "w") as arq:
            json.dump(usuarios, arq, indent=4)
        exit()

    # se ninguém bateu com o login, avisa
    print("Login inválido.")

# se passou das 3 tentativas sem sucesso
print("Não foi possível logar. Tente novamente mais tarde.")
