import socket
from ast import literal_eval

class TopHashtagClient(object):
    def __init__(self):
        self._ip = '127.0.0.1'
        self._port = 8000
        self._sock = None

    def __del__(self):
        self.disconnect()

    def connect(self):
        if self._sock:
            return
        sock = self._connect()
        self._sock = sock

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))
        return sock

    def disconnect(self):
        if self._sock is None:
            return
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
        except:
            pass
        self._sock = None

    def get_top_n(self, n):
        if not self._sock:
            self.connect()
        try:
            self._sock.send(str(n))
            data = self._sock.recv(4096)
            return literal_eval(data)
        except:
            self.disconnect()
            return None

if __name__ == '__main__':
    client = TopHashtagClient()
    while 1:
        print client.get_top_n(5)
