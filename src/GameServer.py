#!/usr/bin/env python3
from SocketBase import *
from ClientHandler import ClientHandler


class Server:
    def __init__(self, argv):
        try:
            self.PORT = int(argv[1])
            with open(argv[2]) as userinfo:
                self.USERINFO = set(userinfo.read().split('\n'))
        except (IndexError, ValueError):
            logging.error(f'Usage: {argv[0]} <server_port> <path/to/Userinfo.txt>')
            exit(1)
        except FileNotFoundError:
            logging.error(f'File {argv[2]} not found')
            exit(1)
        self.USERINFO.remove('')

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('', self.PORT))
            self.server_socket.listen()
        except (OSError, ConnectionError):
            logging.exception('Failed starting socket')
            exit(1)

        self.clients = {}

    def start_listen(self):
        while True:
            connection = self.server_socket.accept()
            new_client = ClientHandler(connection, self)
            self.clients[new_client.addr] = new_client


def main(argv):
    server = Server(argv)
    logging.info(f'Server started. Listening {server.PORT}')
    server.start_listen()


if __name__ == '__main__':
    main(sys.argv)

