import socket, threading
import logging
import logging.handlers
import hashlib
import sys

HOST = "127.0.0.1"
PORT = 65432


def verificaIntegridade():
    fileProxy = open("./servidorProxy.py", "rb")
    readFileProxy = fileProxy.read()
    hashFileProxy = hashlib.sha224(readFileProxy)
    hashInteg = open("hashInteg.txt", "r")
    if hashFileProxy.hexdigest() != hashInteg.read():
        logging.error("Tentativa de rodar um codigo com integridade comprometida")
        print("Integridade do código comprometida, fechando o programa")
        sys.exit(0)


def proxy_thread(conn, addr):

    data = conn.recv(2048)
    first_line = data.split(b"\n")[0]
    url = first_line.split(b" ")[1]
    http_pos = url.find(b"://")
    requestHost = url[(http_pos + 3) :]
    webserver_pos = requestHost.find(b"/")
    if webserver_pos == -1:
        webserver_pos = len(requestHost)
    verificacao = requestHost[(webserver_pos + 1) :]
    if verificacao == b"monitorando":
        htmlResponse = "<html><head><title>Exemplo de resposta HTTP </title></head><body>Acesso nao autorizado!</body></html>"
        dataResponse = f"HTTP/1.1 200 OK\r\nServer: Microsoft-IIS/4.0\r\nDate: Mon, 3 Jan 2016 17:13:34 GMT\r\nContent-Type: text/html\r\nLast-Modified: Mon, 11 Jan 2016 17:24:42 GMT\r\nContent-Length: 112\r\n\r\n{htmlResponse}"
        conn.send(dataResponse.encode())
        logging.error("Acesso não autorizado detectado!")
    webserver = requestHost[:webserver_pos]

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((webserver.decode(), 80))
        print(
            f"Requisicao do Cliente {addr} sendo enviado para o servidor {webserver.decode()}"
        )
        logging.error(
            f"Requisicao do Cliente {addr} sendo enviado para o servidor {webserver.decode()}"
        )
        s.sendall(data)

        while 1:
            dataResponse = s.recv(2048)
            splitResponse = dataResponse.split(b" ")
            protocolo = splitResponse[0]
            if protocolo == b"HTTP/1.1":
                cod_response = splitResponse[1]
                print(f"Codigo de resposta: {cod_response}")
                logging.error(f"Codigo de resposta: {cod_response}")
            if not dataResponse:
                break
            conn.send(dataResponse)
    except socket.timeout:
        pass

    s.close()
    conn.close()
    return


verificaIntegridade()

my_logger = logging.getLogger()
handler = logging.handlers.SysLogHandler(
    address=("192.168.1.2", 1468), socktype=socket.SOCK_STREAM
)
my_logger.addHandler(handler)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    print("escutando...")

    while True:
        conn, addr = serverSocket.accept()
        threadConex = threading.Thread(
            name=addr, target=proxy_thread, args=(conn, addr), daemon=True
        )
        threadConex.start()
