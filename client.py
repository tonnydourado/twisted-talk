"""
Cliente para testar  as implementações de echo server (select-server.py and thread-server.py)

Uso:
    $ python client.py <host> <port>
"""

import socket
from multiprocessing.dummy import Pool
from threading import current_thread
from time import sleep


def connect(id_, host, port):
    """
    Envia uma string para o servidor echo e imprime a resposta

    :param id_: id, só pra identificar as mensagens
    :param host: endereço do servidor socket
    :param port: porta do servidor socket
    """
    print(f"Host: '{host}', port: '{port}")
    print(f"Thread: {current_thread()}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print(f"Sending data ({id_})")
    client.send(f"test {id_}".encode())
    response = client.recv(1024)
    print(f"Response: {response}")
    sleep(1)
    client.close()


def main(host, port):
    """
    Manda um punhado de mensagens para o servidor socket

    :param host: endereço do servidor socket
    :param port: porta do servidor socket
    """
    thread_pool = Pool(3)
    thread_pool.map(lambda i: connect(i, host, port), range(3))


if __name__ == '__main__':
    import sys
    main(host=sys.argv[1], port=int(sys.argv[2]))
