import select
import socket
from queue import Queue, Empty


class EventLoop(object):
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self._server = None
        self._inputs, self._outputs = [], []
        self._queues = {}

    def __call__(self):
        if self._server is not None:
            raise Exception("Can't start server twice!")
        self._start_listening()
        self._inputs.append(self._server)

        while self._inputs:
            readable, writable, errors = select.select(
                self._inputs,
                self._outputs,
                self._inputs
            )
            for sock in readable:
                self._handle_readable(sock)
            for sock in writable:
                self._handle_writable(sock)
            for sock in errors:
                self._handle_error(sock)

    def _start_listening(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setblocking(0)
        self._server.bind((self.host, self.port))
        self._server.listen(5)

    def _handle_readable(self, sock):
        # Quando a conexão de servidor está pronta pra ser lida, significa que
        # temos um novo cliente:
        if sock is self._server:
            conn, addr = sock.accept()
            conn.setblocking(0)
            self._inputs.append(conn)
            self._queues[conn] = Queue()
        else:
            data = sock.recv(1024)
            if data:
                # Colocamos os dados lidos na fila, pra enviar quando o socket
                # estiver pronto para ser escrito:
                self._queues[sock].put(data)
                # Caso seja uma nova conexão, vamos monitorar ela para escrita
                # também:
                if sock not in self._outputs:
                    self._outputs.append(sock)
            else:
                # Sem dados, podemos fechar a conexão:
                if sock in self._outputs:
                    self._outputs.remove(sock)
                self._inputs.remove(sock)
                del self._queues[sock]
                sock.close()

    def _handle_writable(self, sock):
        try:
            next_msg = self._queues[sock].get_nowait()
        except Empty:
            self._outputs.remove(sock)
            self._inputs.remove(sock)
            del self._queues[sock]
            sock.close()
        else:
            sock.send(next_msg)

    def _handle_error(self, sock):
        self._inputs.remove(sock)
        if sock in self._outputs:
            self._outputs.remove(sock)
        del self._queues[sock]
        sock.close()


if __name__ == '__main__':
    import sys
    loop = EventLoop(host=sys.argv[1], port=int(sys.argv[2]))
    loop()
