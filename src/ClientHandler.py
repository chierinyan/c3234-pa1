from SocketBase import *
import threading
from enum import Enum, auto


class ClientHandler(SocketBase):
    class Status(Enum):
        UNAUTHORIZED = auto()
        HALL         = auto()
        WAITING      = auto()
        STARTED      = auto()

    def __init__(self, conn, server):
        super().__init__(conn[0], conn[1])
        self.server = server

        self.connected = True
        self.status = ClientHandler.Status.UNAUTHORIZED

        self.thread = threading.Thread(target=self.game)
        self.thread.start()

    def recv_cmd(self, expected=('/login', '/list', '/enter', '/guess', '/exit')):
        msg_segs = self.recv_str().split()
        if not msg_segs:
            logging.warning(f'Connection lost with {self}')
            self.connected = False
            return ['/disconnected']
        if msg_segs[0] not in expected:
            logging.debug('Failed parsing message')
            return ['/unexpected']
        return msg_segs

    def game(self):
        logging.debug(f'New connection: {self}')

        while True:
            cmd = self.recv_cmd()

            if not self.connected:
                return

            if cmd[0] == '/exit':
                self.send_str('4001 Bye bye')
                self.connected = False
            elif self.status is ClientHandler.Status.UNAUTHORIZED and cmd[0] == '/login':
                self.auth(cmd[1:])
            else:
                self.send_str('4002 Unrecognized message')

    def auth(self, rest):
        credentials = f'{rest[0]}:{rest[1]}'
        if credentials in self.server.USERINFO:
            self.send_str('1001 Authentication successful')
            self.status = ClientHandler.Status.HALL
            return
        self.send_str('1002 Authentication failed')

