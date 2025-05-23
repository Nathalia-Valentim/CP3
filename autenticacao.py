# importa JSON, data e hora
import json
from datetime import datetime
import maskpass # type: ignore

# carrega os dados dos usuários do arquivo JSON
with open("usuarios.json", "r") as arquivo:
    usuarios = json.load(arquivo)

# definir autenticação
# três tentativas de login, caso o email ou senha não funcionem o programa é encerrado
for i in range(3):
    login_entrada = input("Digite o login: ")
    senha_entrada = maskpass.advpass("Digite a senha: ") # mantem a senha oculta com *

    # caso o login e senha digitados/inseridos sejam diferentes do que está no JSON
    for u in usuarios:
        if login_entrada != u["login"]:
            continue  # tenta o próximo usuário

        # caso tenha encontrado o login, passa para a senha
        if not u["ativo"]:
            print("Usuário bloqueado.")
            break

        # se a senha estiver errada vai ser adicionado uma tentativa falha no dicionário
        if senha_entrada != u["senha"]:
            print("Senha incorreta.")
            u["tentativas_falhas"] += 1

            # se a senha estiver errada 3 vezes, o usuário é bloqueado
            if u["tentativas_falhas"] >= 3:
                u["ativo"] = False
                print("Usuário bloqueado após 3 tentativas.")

            # salva as alterações no arquivo JSON
            with open("usuarios.json", "w") as arq:
                json.dump(usuarios, arq, indent=4)

            break

        # login e senha corretos
        print("Bem-vindo!")
        u["ultimo_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Último login: {u['ultimo_login']}")
        u["tentativas_falhas"] = 0
        print("")
        print(f"Tentativas falhas: {u['tentativas_falhas']} de 3")

        # esse é o menu caso a pessoa entre como administrador
        if u["perfil"] == "admin":
            opcao = ""

            while opcao != "5":
                print('''
                \nMenu Admin:
                \n1. Listar usuários
                \n2. Trocar senha de alguém
                \n3. Bloquear/desbloquear alguém
                \n4. Cadastrar novo usuário
                \n5. Sair
                ''')

                # lista os usuários para o administrador
                def lista_usuarios():
                    for x in usuarios:
                        print(f"- {x['nome']} ({x['login']}) [{x['perfil']}]")
                
                # permite que o administrador altere a senha de algum usuário
                def troca_senha():
                    alvo = input("Login do usuário: ")
                    for x in usuarios:
                        if x["login"] == alvo: # se o login for igual ao que foi digitado
                            nova = ""
                            repetir = "diferente"
                            
                            while nova != repetir:
                                nova = maskpass.advpass("Nova senha: ") # mantem a senha oculta com *
                                repetir = maskpass.advpass("Repita a senha: ") # mantem a senha oculta com *
                                
                                if nova != repetir: # se as senhas não coincidirem
                                    print("As senhas não coincidem. Tente novamente.")

                            x["senha"] = nova
                            print("Senha trocada com sucesso.")
                            break  # sai do for após trocar a senha
                            
                # permite que o administrador bloqueie e desbloqueie um usuário
                # o usuário é bloqueado se o ativo for False
                # o usuário é desbloqueado se o ativo for True
                def bloqueia_desbloqueia():
                    alvo = input("Login do usuário: ")
                    for x in usuarios:
                        if x["login"] == alvo: # se o login for igual ao que foi digitado
                            x["ativo"] = not x["ativo"]
                            print("Usuário desbloqueado." if x["ativo"] else "Usuário bloqueado.")
                            break
                
                # permite que o administrador cadastre um novo usuário
                def cadastrar_usuario():
                    nome_novo = input("Nome: ")
                    login_novo = input("Login do novo usuário: ")
                    senha_nova = maskpass.advpass("Senha: ") # mantem a senha oculta com *
                    perfil_novo = input("Perfil (admin/user): ")
                    novo = {
                        "nome": nome_novo,
                        "login": login_novo,
                        "senha": senha_nova,
                        "perfil": perfil_novo,
                        "ultimo_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # salva a data e hora de criação
                        "tentativas_falhas": 0,
                        "ativo": True
                    }
                    usuarios.append(novo)
                    print("Usuário cadastrado.")

                opcao = input("Digite a opção desejada: ")

                match opcao:
                    # lista os usuários para o administrador
                    case "1":
                        lista_usuarios()
                    # permite que o administrador altere a senha de algum usuário
                    case "2":
                        troca_senha()
                    # permite que o administrador bloqueie e desbloqueie um usuário
                    case "3":
                        bloqueia_desbloqueia()
                    # permite que o administrador cadastre um novo usuário
                    case "4":
                        cadastrar_usuario()
                    # para sair
                    case "5":
                        exit()
                    # caso a opção não seja uma das opções acima
                    case _:
                        print("Opção inválida.")
                        

                # salva as alterações no arquivo JSON
                with open("usuarios.json", "w") as arq:
                    json.dump(usuarios, arq, indent=4)

        # caso a conta que for logada seja um usuário
        elif u["perfil"] == "user":
            opcao = ""

            # opções do menu do usuário
            while opcao != "2":
                print('''
                \nMenu Usuário:
                \n1. Trocar senha
                \n2. Sair
                ''')

                # permite que o usuário troque a própria senha
                def alerar_senha_usuario(usuario):
                    nova = ""
                    repetir = "diferente"
                    
                    while nova != repetir:
                        nova = maskpass.advpass("Nova senha: ") # mantem a senha oculta com *
                        repetir = maskpass.advpass("Repita a senha: ") # mantem a senha oculta com *

                        if nova != repetir:
                            print("As senhas não coincidem. Tente novamente.")

                    usuario["senha"] = nova
                    print("Senha trocada com sucesso.")

                opcao = input("Digite a opção desejada: ")

                match opcao:
                    case "1":
                        alerar_senha_usuario(u)
                    case "2":
                        exit()
                    case _:
                        print("Opção inválida.")
                        continue

                # salva login bem-sucedido e sai do programa
                with open("usuarios.json", "w") as arq:
                    json.dump(usuarios, arq, indent=4)

    # caso o login e senha inseridos não existam no JSON
    print("Login inválido.")
