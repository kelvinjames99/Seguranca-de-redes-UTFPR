import socket
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode
import datetime
from Crypto.Util.Padding import unpad
import sys

# declaração de variáveis globais
SALT = "a32dbfdf6"
CHAVECLIENTE = "KELVIN" + SALT
HOST = "127.0.0.1"
PORT_AS = 65432
PORT_TGS = 65433
PORT_SERVICO = 65434
ID_C = "KELVIN"
ID_S = "SERVICO"
tempoVencimento = 15
T_R = (datetime.datetime.now() + datetime.timedelta(minutes=tempoVencimento)).strftime(
    "%m/%d/%Y, %H:%M:%S"
)
N1 = str(random.randint(0, 100))
N2 = str(random.randint(0, 100))
N3 = str(random.randint(0, 100))
IV = "silkBIVAVL2Yc0Kf1Rp8zg=="


def m2Decrypt(data, cipherClient, N1):
    mensagens = data.decode().split("\n")
    submensagem1 = (
        unpad(cipherClient.decrypt(b64decode(mensagens[0])), AES.block_size)
        .decode()
        .split("\n")
    )
    if N1 == submensagem1[1]:
        print("Número aleatório recebido correto")
    else:
        print("Número aleatório recebido incorreto, fechando o programa...")
        sys.exit(0)

    sessionKey = hashlib.sha224(str.encode(submensagem1[0])).hexdigest()[:32].encode()
    return mensagens[1], sessionKey


def m3Encrypt(ticket, sessionKey):
    cipher = AES.new(sessionKey, AES.MODE_CBC, b64decode(IV))
    encrpty = ID_C + "\n" + ID_S + "\n" + T_R + "\n" + N2
    # ID_S é o serviço solicitado, o TGS deve fazer algo com isso?
    ct_bytes = cipher.encrypt(pad(encrpty.encode(), AES.block_size))
    mensagem3 = b64encode(ct_bytes).decode("utf-8") + "\n" + ticket
    return mensagem3


def m4Decrypt(data, sessionKey, N2):
    mensagens = data.decode().split("\n")
    cipher = AES.new(sessionKey, AES.MODE_CBC, b64decode(IV))
    submensagem1 = (
        unpad(cipher.decrypt(b64decode(mensagens[0])), AES.block_size)
        .decode()
        .split("\n")
    )
    print(submensagem1)
    if N2 == submensagem1[2]:
        print("Número aleatório recebido correto")
    else:
        print("Número aleatório recebido incorreto, fechando o programa...")
        sys.exit(0)
    sessionKeyServico = (
        hashlib.sha224(str.encode(submensagem1[0])).hexdigest()[:32].encode()
    )
    return sessionKeyServico, submensagem1[1], mensagens[1]


def getCipherCliente():
    chaveFile = open("chaveCliente.txt", "r")
    key = chaveFile.readline().encode()
    # iv = b64decode(chaveFile.readline())
    return AES.new(key, AES.MODE_CBC, b64decode(IV))


def m5Encrypt(ticket, sessionKey):
    cipher = AES.new(sessionKey, AES.MODE_CBC, b64decode(IV))
    encrpty = ID_C + "\n" + T_R + "\n" + "PING" + "\n" + N3
    ct_bytes = cipher.encrypt(pad(encrpty.encode(), AES.block_size))
    mensagem5 = b64encode(ct_bytes).decode("utf-8") + "\n" + ticket
    return mensagem5

def m6Decrypt(data, sessionKey, N3):
    mensagens = data.decode()
    cipher = AES.new(sessionKey, AES.MODE_CBC, b64decode(IV))
    mensagens = (
        unpad(cipher.decrypt(b64decode(mensagens)), AES.block_size)
        .decode()
        .split("\n")
    )
    print(mensagens)
    if N3 == mensagens[1]:
        print("Número aleatório recebido correto")
    else:
        print("Número aleatório recebido incorreto, fechando o programa...")
        sys.exit(0)

    print(mensagens[0])
    print("------------------------FIM------------------------")


# montagem da mensagem1
key = hashlib.sha224(str.encode(CHAVECLIENTE)).hexdigest()[:32].encode()
cipher = AES.new(key, AES.MODE_CBC, b64decode(IV))
encrpty = ID_S + "\n" + T_R + "\n" + N1
ct_bytes = cipher.encrypt(pad(encrpty.encode(), AES.block_size))
mensagem1 = ID_C + "\n" + b64encode(ct_bytes).decode("utf-8")
chaveCliente = open("chaveCliente.txt", "w")
chaveCliente.write(key.decode())
chaveCliente.close()
print(mensagem1)

# comunicação com AS
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT_AS))
    s.sendall(mensagem1.encode())
    data = s.recv(1024)
    print("Client-Received", repr(data))
    s.close()

# comunicação com TGS
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    cipherCliente = getCipherCliente()
    ticket, sessionKeyTgs = m2Decrypt(data, cipherCliente, N1)
    mensagem3 = m3Encrypt(ticket, sessionKeyTgs)
    s.connect((HOST, PORT_TGS))
    s.sendall(mensagem3.encode())
    data = s.recv(1024)
    print("Client-Received", repr(data))
    s.close()


# comunicação com o servidor de serviço
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    sessionKeyServico, T_R, ticket = m4Decrypt(data, sessionKeyTgs, N2)
    mensagem5 = m5Encrypt(ticket, sessionKeyServico)
    s.connect((HOST, PORT_SERVICO))
    s.sendall(mensagem5.encode())
    data = s.recv(1024)
    print("Client-Received", repr(data))
    s.close()
    m6Decrypt(data, sessionKeyServico, N3)
