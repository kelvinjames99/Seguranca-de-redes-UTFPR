import socket
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import uuid
import datetime
import sys

SALT = "a32dbfdf6"
CHAVESERVICO = "KELVINSERVICO" + SALT
IV = "silkBIVAVL2Yc0Kf1Rp8zg=="
HOST = "127.0.0.1"
PORT = 65434

chaveServico = open("chaveServico.txt", "w")
key = hashlib.sha224(str.encode(CHAVESERVICO)).hexdigest()[:32].encode()
chaveServico.write(key.decode())
chaveServico.close()

def m5Decrypt(cipherServico, data):
    m5 = data.decode().split("\n")
    ticket = (
        unpad(cipherServico.decrypt(b64decode(m5[1])), AES.block_size).decode().split("\n")
    )
    # print(ticket)
    sessionKeyServico = hashlib.sha224(str.encode(ticket[2])).hexdigest()[:32].encode()
    cipherSession = AES.new(sessionKeyServico, AES.MODE_CBC, b64decode(IV))
    submensagem = (
        unpad(cipherSession.decrypt(b64decode(m5[0])), AES.block_size)
        .decode()
        .split("\n")
    )
    # print(submensagem)
    print(ticket)
    print(submensagem)
    return ticket, submensagem, sessionKeyServico

def m6Encrypt(ticket, submensagem, sessionKeyServico):
    cipherSession = AES.new(sessionKeyServico, AES.MODE_CBC, b64decode(IV))
    dataVencimento = datetime.datetime.strptime(ticket[1], "%m/%d/%Y, %H:%M:%S")
    if(datetime.datetime.now() > dataVencimento):
        print("Tempo de acesso ao serviço já acabou")
        sys.exit(0)
    if(submensagem[2] != "PING"):
        print("Serviço solicitado não existe")
        sys.exit(0)
    mensagem6 = "PONG" + "\n" + submensagem[3]
    mensagem6 = cipherSession.encrypt(pad(mensagem6.encode(), AES.block_size))
    mensagem6 = b64encode(mensagem6).decode("utf-8")
    return mensagem6

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor de Serviço escutando...")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("mensagem recebida: " + repr(data))
            cipher = AES.new(key, AES.MODE_CBC, b64decode(IV))
            ticket, submensagem, sessionKeyServico = m5Decrypt(cipher, data)
            mensagem6 = m6Encrypt(ticket, submensagem, sessionKeyServico)
            conn.sendall(mensagem6.encode())
