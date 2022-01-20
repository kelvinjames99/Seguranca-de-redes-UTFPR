import socket
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import uuid

SALT = "a32dbfdf6"
CHAVETGS = "KELVINTGS" + SALT
IV = "silkBIVAVL2Yc0Kf1Rp8zg=="
HOST = "127.0.0.1"
PORT = 65433

chaveTGS = open("chaveTGS.txt", "w")
key = hashlib.sha224(str.encode(CHAVETGS)).hexdigest()[:32].encode()
chaveTGS.write(key.decode())
chaveTGS.close()


def m3Decrypt(cipherTGS, data):
    m3 = data.decode().split("\n")
    ticket = (
        unpad(cipherTGS.decrypt(b64decode(m3[1])), AES.block_size).decode().split("\n")
    )
    # print(ticket)
    # se o ticket é descriptografado com sucesso, ele é considerado válido ?
    sessionKeyTgs = hashlib.sha224(str.encode(ticket[2])).hexdigest()[:32].encode()
    cipherSession = AES.new(sessionKeyTgs, AES.MODE_CBC, b64decode(IV))
    submensagem = (
        unpad(cipherSession.decrypt(b64decode(m3[0])), AES.block_size)
        .decode()
        .split("\n")
    )
    # print(submensagem)
    return ticket, submensagem, sessionKeyTgs


def m4Encrypt(ticket, submensagem, sessionKeyTgs):
    sessaoServico = uuid.uuid4().hex
    T_A = ticket[1]
    N2 = submensagem[3]
    ID_C = ticket[0]
    submensagem1 = sessaoServico + "\n" + T_A + "\n" + N2
    cipherSession = AES.new(sessionKeyTgs, AES.MODE_CBC, b64decode(IV))
    submensagem1 = cipherSession.encrypt(pad(submensagem1.encode(), AES.block_size))
    cipherServico = getCipherServico()
    submensagem2 = ID_C + "\n" + T_A + "\n" + sessaoServico
    submensagem2 = cipherServico.encrypt(pad(submensagem2.encode(), AES.block_size))
    mensagem4 = (
        b64encode(submensagem1).decode("utf-8")
        + "\n"
        + b64encode(submensagem2).decode("utf-8")
    )
    return mensagem4


def getCipherServico():
    chaveFile = open("chaveServico.txt", "r")
    key = chaveFile.readline().encode()
    return AES.new(key, AES.MODE_CBC, b64decode(IV))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor TGS escutando...")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("mensagem recebida: " + repr(data))
            cipher = AES.new(key, AES.MODE_CBC, b64decode(IV))
            ticket, submensagem, sessionKeyTgs = m3Decrypt(cipher, data)
            mensagem4 = m4Encrypt(ticket, submensagem, sessionKeyTgs)
            conn.sendall(mensagem4.encode())
