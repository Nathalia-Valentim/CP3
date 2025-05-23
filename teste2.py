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
    senha_entrada = maskpass.advpass("Digite a senha: ")

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
            break

        # login e senha corretos
        print("Bem-vindo!")
        u["ultimo_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        u["tentativas_falhas"] = 0

        # esse é o menu caso a pessoa entre como administrador
        if u["perfil"] == "admin":
            opcao = ""

            while opcao != 5:
                print('''
                Menu Admin:
                1. Listar usuários
                2. Trocar senha de alguém
                3. Bloquear/desbloquear alguém
                4. Cadastrar novo usuário
                5. Sair
                ''')

                # lista os usuários para o administrador
                def lista_usuarios():
                    for x in usuarios:
                        print(f"- {x['nome']} ({x['login']}) [{x['perfil']}]")
                
                # permite que o administrador altere a senha de algum usuário
                def troca_senha():
                    alvo = input("Login do usuário: ")
                    for x in usuarios:
                        if x["login"] == alvo:
                            nova = maskpass.advpass("Nova senha: ")
                            repetir = maskpass.advpass("Repita a senha: ")
                            if nova == repetir:
                                x["senha"] = nova
                                print("Senha trocada com sucesso.")
                                break
                            else:
                                print("Certifique-se que as senhas são iguais")
                            break

                # permite que o administrador bloqueie e desbloqueie um usuário
                def bloqueia_desbloqueia():
                    alvo = input("Login do usuário: ")
                    for x in usuarios:
                        if x["login"] == alvo:
                            x["ativo"] = not x["ativo"]
                            print("Usuário desbloqueado." if x["ativo"] else "Usuário bloqueado.")
                            break
                
                # permite que o administrador cadastre um novo usuário
                def cadastrar_usuario():
                    login_novo = input("Login do novo usuário: ")
                    nome_novo = input("Nome: ")
                    senha_nova = maskpass.advpass("Senha: ")
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
                        break
                    # caso a opção não seja uma das opções acima
                    case _:
                        print("Opção inválida.")

                # salva as alterações no arquivo JSON
                with open("usuarios.json", "w") as arq:
                    json.dump(usuarios, arq, indent=4)

        # caso a conta que for logada seja um usuário
        elif u["perfil"] == "user":
            opcao = ""

            while opcao != 2:
                print('''
                Menu Usuário:
                1. Trocar senha
                2. Sair
                ''')

                def alerar_senha_usuario():
                    nova = input("Nova senha: ")
                    u["senha"] = nova
                    print("Senha trocada.")
                    with open("usuarios.json", "w") as arq:
                        json.dump(usuarios, arq, indent=4)

                opcao = input("Digite a opção desejada: ")

                match opcao:
                    case "1":
                        alerar_senha_usuario()
                    case "2":
                        break
                    case _:
                        print("Opção inválida.")

                # salva login bem-sucedido e sai do programa
                with open("usuarios.json", "w") as arq:
                    json.dump(usuarios, arq, indent=4)
                exit()

    # caso o login e senha inseridos não existam no JSON
    print("Login inválido.")

# caso tenha ultrapassado as três tentaivas de login
print("Não foi possível logar. Tente novamente mais tarde.")
