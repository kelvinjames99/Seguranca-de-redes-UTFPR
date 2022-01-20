from collections import Counter
import unidecode

texto = "Y6ySN aq6QbdPAUXRh sat aZn 911 Xu 0vFKkXq Zv yPzlFr\nSG8c2b5MMF. BmNlk PuoBiiC9fmqC, FIV m6 od4ZqF\ncrvePre0. vu 96gS6 VDB iw 7acN3RO whn omdaJ W2YoKE\nXO0qFArkPhw1PMX 1 GgrYbX Lzlr 7 wUH, f8OmwhcY nw\nFSdq8I MP H20jCi 4jWK 4 MnvLp, XDU n2m.\n2wICUz6n c1 Pl264."

alfabeto = list(range(65, 91))
alfabeto.extend(list(range(97, 123)))
alfabeto.extend(list(range(48, 58)))

counter = Counter(texto.replace(" ", ""))
print(counter)
chave = alfabeto.index(ord(counter.most_common(1)[0][0])) - alfabeto.index(97)
outputFile = open(input("insira o nome do arquivo decifrado:"), "w")
for charac in texto:
    charac = unidecode.unidecode(charac)  # tira acentos
    try:
        outputFile.write(
            chr(alfabeto[(alfabeto.index(ord(charac)) - chave) % len(alfabeto)])
        )
    except:
        outputFile.write(charac)

outputFile.close()
