import socket
from multiprocessing.dummy import Pool
from threading import current_thread


def dispatcher(host, port):
    print(f"Thread: {current_thread()}, Host: '{host}', Port: '{port}")
    thread_pool = Pool(5)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    while True:
        # Aqui a thread principal vai bloquear até que um cliente se conecte ao
        # servidor:
        client, address = sock.accept()
        client.settimeout(60)
        # A nova conexão é passada para uma thread no thread pool:
        thread_pool.apply_async(process_request, (client, address))


def process_request(client, address, size=1024):
    print(f"Thread: {current_thread()}, Client: {client}, "
          f"Address: {address}")

    # O processamento do request é sequencial: lemos os dados, e escrevemos a
    # reposta:
    while True:
        try:
            data = client.recv(size)
            if data:
                print(f"Data: {data}")
                client.send(data)
            break
        finally:
            client.close()


if __name__ == '__main__':
    import sys
    dispatcher(host=sys.argv[1], port=int(sys.argv[2]))

