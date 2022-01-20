import unidecode

alfabeto = list(range(65, 91))
alfabeto.extend(list(range(97, 123)))
alfabeto.extend(list(range(48, 58)))

def cifra():
    inputFile = open(
        input("insira o nome do arquivo localizado na pasta local do programa:")
    )
    outputFile = open(input("insira o nome do arquivo cifrado:"), "w")
    chave = int(input("digite a chave que será usada:"))
    for line in inputFile:
        for charac in line:
            charac = unidecode.unidecode(charac)  # tira acentos
            try:
                outputFile.write(
                    chr(alfabeto[(alfabeto.index(ord(charac)) + chave) % len(alfabeto)])
                )
            except:
                outputFile.write(charac)
    inputFile.close()
    outputFile.close()


def decifrar():
    inputFile = open(
        input("insira o nome do arquivo localizado na pasta local do programa:")
    )
    outputFile = open(input("insira o nome do arquivo decifrado:"), "w")
    chave = int(input("digite a chave que será usada:"))
    for line in inputFile:
        for charac in line:
            charac = unidecode.unidecode(charac)  # tira acentos
            try:
                outputFile.write(
                    chr(alfabeto[(alfabeto.index(ord(charac)) - chave) % len(alfabeto)])
                )
            except:
                outputFile.write(charac)
    inputFile.close()
    outputFile.close()


op = int(input("Qual é a operação (0 - cifrar | 1 - decifrar)\n"))

options = {
    0: cifra,
    1: decifrar,
}

options.get(op)()
