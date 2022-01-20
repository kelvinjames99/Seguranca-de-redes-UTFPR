import random
import unidecode

alfabeto = list(range(65, 91))
alfabeto.extend(list(range(97, 123)))
alfabeto.extend(list(range(48, 58)))


def criaChave(tamMsg):
    chaveFile = open("chave.dat", "w")
    for i in range(tamMsg):
        chaveFile.write(chr(alfabeto[random.randint(0, len(alfabeto) - 1)]))
    chaveFile.close()


def contaCaracteres(fileName):
    file = open(fileName)
    numchar = 0
    for line in file:
        for charac in line:
            try:
                alfabeto.index(ord(charac))
                numchar += 1
            except:
                continue
    file.close()
    return numchar


def decifrar():
    inputFileName = input(
        "insira o nome do arquivo localizado na pasta local do programa:"
    )
    outputFile = open(input("insira o nome do arquivo decifrado:"), "w")
    tamChave = contaCaracteres(inputFileName)
    chaveName = open("chave.dat").readline()
    aux = 0
    for line in open(inputFileName):
        for charac in line:
            charac = unidecode.unidecode(charac)
            try:
                inputIndex = alfabeto.index(ord(charac))
                chaveIndex = alfabeto.index(ord(chaveName[aux])) + 1
                aux += 1
                newIndex = (inputIndex - chaveIndex) % len(alfabeto)
                outputFile.write(chr(alfabeto[newIndex]))
            except:
                outputFile.write(charac)


def cifra():
    inputFileName = input(
        "insira o nome do arquivo localizado na pasta local do programa:"
    )
    outputFile = open(input("insira o nome do arquivo cifrado:"), "w")
    tamChave = contaCaracteres(inputFileName)
    criaChave(tamChave)
    chaveName = open("chave.dat").readline()
    aux = 0
    for line in open(inputFileName):
        for charac in line:
            charac = unidecode.unidecode(charac)
            try:
                inputIndex = alfabeto.index(ord(charac))
                chaveIndex = alfabeto.index(ord(chaveName[aux])) + 1
                aux += 1
                newIndex = (inputIndex + chaveIndex) % len(alfabeto)
                outputFile.write(chr(alfabeto[newIndex]))
            except:
                outputFile.write(charac)


op = int(input("Qual é a operação (0 - cifrar | 1 - decifrar)\n"))

options = {
    0: cifra,
    1: decifrar,
}

options.get(op)()
