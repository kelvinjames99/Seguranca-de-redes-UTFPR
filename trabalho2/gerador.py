import hashlib
import datetime

SALT = "a32dbfdf6"


def autenticacao(user, senhaLocal):
    usersFile = open("geradorFile.txt", "r")
    inputSenha = hashlib.sha224(str.encode(senhaLocal)).hexdigest()
    for line in usersFile:
        if line.replace("\n", "") == user:
            senhaFile = usersFile.readline().replace("\n", "")
            if senhaFile == inputSenha:
                usersFile.close()
                return senhaFile

    usersFile.close()
    return False


def getSenhaSemente(user):
    file = open("usersFile.txt", "r")
    for line in file:
        if line.replace("\n", "") == user:
            senhaFile = file.readline().replace("\n", "")
            return senhaFile


def PasswordCreator(senhaSemente):
    senhas = []
    for i in range(5):
        senhaSemente = hashlib.sha224(str.encode(senhaSemente)).hexdigest()[:8]
        senhas.append(senhaSemente)
    return senhas


def newUser():
    usersFile = open("usersFile.txt", "a")
    geradorFile = open("geradorFile.txt", "a")
    name = input("digite o nome do usuário\n")
    senhaLocal = input("digite a senha local\n")  # lembrar de usar salt
    senhaLocal += SALT
    senhaLocal = hashlib.sha224(str.encode(senhaLocal)).hexdigest()
    senhaSemente = input("digite a senha semente\n")  # lembrar de usar salt
    senhaSemente += SALT
    senhaSemente = hashlib.sha224(str.encode(senhaSemente)).hexdigest()
    usersFile.write(name + "\n" + senhaSemente + "\n")
    geradorFile.write(name + "\n" + senhaLocal + "\n")
    geradorFile.close()
    usersFile.close()


def newPassword():
    user = input("Digite o nome do usuário\n")
    senhaLocal = input("Digite a senha local\n")
    senhaFile = autenticacao(user, senhaLocal + SALT)
    if senhaFile:
        senhaSemente = getSenhaSemente(user)
        print("Logado!")
        data = datetime.datetime.now()
        time = data.strftime("%m/%d/%Y %H:%M")
        senhas = PasswordCreator(senhaSemente + time)
        print(senhas)
    else:
        print("usuário não encontrado")


op = int(input("Qual é a operação (0 - criar um novo usuário | 1 - gerar uma senha)\n"))

options = {
    0: newUser,
    1: newPassword,
}

options.get(op)()
