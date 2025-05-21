# importa JSON, data e hora
import json
from datetime import datetime

# carrega os dados dos usuários do arquivo JSON
with open ("usuarios.json", "r") as arquivo:
    usuarios = json.load(arquivo)

# definir autenticação
# três tentativas de login, caso o email ou senha não funcionem o programa é encerrado
for entrada in range(3):
    login_entrada = input("Digite o login: ")
    senha_entrada = input("Digite a senha: ")

    for u in usuarios:
        if login_entrada == u["login"]:
            usuario_encontrado = u
            break

        if senha_entrada != u["senha"]:
            print("Senha incorreta.")
            u["tentativas_falhas"] += 1
            if u["tentativas_falhas"] >= 3:
                print("Você foi bloqueado. Tente novamente mais tarde.")
                break
        else:
            print("Login efetuado com sucesso.")
            break

    if u["login"] == "admin"