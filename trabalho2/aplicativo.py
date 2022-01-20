import hashlib
import datetime

SALT = "a32dbfdf6"


def PasswordCreator(senhaSemente):
    senhas = []
    for i in range(5):
        senhaSemente = hashlib.sha224(str.encode(senhaSemente)).hexdigest()[:8]
        senhas.append(senhaSemente)
    return senhas


def validaSenha(senha):
    try:
        senhasUsadas = open("senhasUsadas.txt", "r")
        for line in senhasUsadas:
            line = line.replace("\n", "")
            if senha == line:
                print("Senha já utilizada")
                return False
        return True
    except:
        return True


def aplicativo():
    aux = 0
    usersFile = open("usersFile.txt", "r")
    user = input("Digite o usuário\n")
    senha = input("Digite a senha de 8 dígitos\n")
    for line in usersFile:
        if line.replace("\n", "") == user:
            senhaSemente = usersFile.readline().replace("\n", "")

    data = datetime.datetime.now()
    time = data.strftime("%m/%d/%Y %H:%M")
    senhaSemente += time
    senhas = PasswordCreator(senhaSemente)
    if senha in senhas and validaSenha(senha):
        print("Chave válida")
        senhasUsadas = open("senhasUsadas.txt", "w")
        for x in senhas:
            if x == senha:
                aux = 1
                senhasUsadas.write(x + "\n")
            elif aux == 1:
                senhasUsadas.write(x + "\n")
        aux = 0
        senhasUsadas.close()
    else:
        print("Chave inválida")


aplicativo()
