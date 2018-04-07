import socket
from multiprocessing.dummy import Pool
from threading import current_thread
from time import sleep


def connect(id_, host, port):
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
    thread_pool = Pool(3)
    thread_pool.map(lambda i: connect(i, host, port), range(3))


if __name__ == '__main__':
    import sys
    print("oi?")
    main(host=sys.argv[1], port=int(sys.argv[2]))
