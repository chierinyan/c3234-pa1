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
        self.room = None

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
                if self.status is ClientHandler.Status.WAITING:
                    self.room[0].clear()
                elif self.status is ClientHandler.Status.STARTED:
                    self.room[0].defeat(self.room[1], disconnected=True)
                return

            if cmd[0] == '/exit':
                self.send_str('4001 Bye bye')
                self.connected = False
            elif self.status is ClientHandler.Status.UNAUTHORIZED and cmd[0] == '/login':
                self.auth(cmd[1:])
            elif self.status is ClientHandler.Status.HALL and cmd[0] in ('/list', '/enter'):
                if cmd[0] == '/list':
                    self.send_list()
                elif cmd[0] == '/enter':
                    self.enter(int(cmd[1]))
            else:
                self.send_str('4002 Unrecognized message')

    def auth(self, rest):
        credentials = f'{rest[0]}:{rest[1]}'
        if credentials in self.server.USERINFO:
            self.send_str('1001 Authentication successful')
            self.status = ClientHandler.Status.HALL
            return
        self.send_str('1002 Authentication failed')

    def send_list(self):
        list_str = ' '.join(map(str, self.server.get_room_list()))
        list_res = '3001 ' + list_str
        self.send_str(list_res)

    def enter(self, room_num):
        room_num -= 1

        if -1 < room_num < self.server.TOTAL_ROOMS:
            self.server.rooms[room_num].enter(self)
        else:
            self.send_str('4002 Unrecognized message')

