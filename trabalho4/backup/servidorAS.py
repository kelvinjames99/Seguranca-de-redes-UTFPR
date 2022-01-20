import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64decode
from Crypto.Util.Padding import unpad
import uuid
from base64 import b64encode

HOST = "127.0.0.1"
PORT = 65432
IV = "silkBIVAVL2Yc0Kf1Rp8zg=="


def getCipherTGS():
    chaveTGSFile = open("chaveTGS.txt", "r")
    key = chaveTGSFile.readline().encode()
    return AES.new(key, AES.MODE_CBC, b64decode(IV))


def getCipherCliente():
    chaveFile = open("chaveCliente.txt", "r")
    key = chaveFile.readline().encode()
    return AES.new(key, AES.MODE_CBC, b64decode(IV))


def m1Decrypt(data):
    m1 = data.decode().split("\n")
    ID_C = m1[0]
    if(ID_C == "CLIENTE"):
        cipher = getCipherCliente()
    submensagem = (
        unpad(cipher.decrypt(b64decode(m1[1])), AES.block_size).decode().split("\n")
    )
    ID_S = submensagem[0]
    T_R = submensagem[1]
    N1 = submensagem[2]
    # print(ID_S + T_R + N1)
    return ID_C, ID_S, T_R, N1


def m2Encrypt(N1, ID_C, T_R, cipherTGS, cipherUser):
    chaveSessaoTGS = uuid.uuid4().hex
    submensagem1 = chaveSessaoTGS + "\n" + N1
    submensagem1 = cipherUser.encrypt(pad(submensagem1.encode(), AES.block_size))
    submensagem2 = ID_C + "\n" + T_R + "\n" + chaveSessaoTGS
    submensagem2 = cipherTGS.encrypt(pad(submensagem2.encode(), AES.block_size))
    mensagem2 = (
        b64encode(submensagem1).decode("utf-8")
        + "\n"
        + b64encode(submensagem2).decode("utf-8")
    )
    return mensagem2


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor AS escutando...")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("mensagem recebida: " + repr(data))
            ID_C, ID_S, T_R, N1 = m1Decrypt(data)
            cipherTGS = getCipherTGS()
            cipherUser = getCipherCliente()
            mensagem2 = m2Encrypt(N1, ID_C, T_R, cipherTGS, cipherUser)
            conn.sendall(mensagem2.encode())
            # print(ID_C + "-" + ID_S + "-" + T_R + "-" + N1)
