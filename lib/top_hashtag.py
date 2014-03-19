import socket
from ast import literal_eval

class TopHashtagClient(object):
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 8000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def __del__(self):
        self.sock.close()

    def get_top_n(self, n):
        self.sock.send(str(n))
        data = self.sock.recv(4096)
        return literal_eval(data)


def main():
    client = TopHashtagClient()
    while 1:
        print client.get_top_n(5)

if __name__ == '__main__':
    main()
