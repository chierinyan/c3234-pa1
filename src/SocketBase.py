import sys
import socket
import logging

LOG_FORMAT = '%(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class SocketBase:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr

    def close(self):
        try:
            self.sock.close()
        except:
            pass

    def recv_str(self):
        try:
            msg = self.sock.recv(1024).decode()
            logging.debug(f'Received %{self.addr}%{msg}%')
        except (socket.error, ConnectionError):
            logging.exception('Failed receiving message')
            return ''
        return msg

    def send_str(self, msg):
        try:
            self.sock.send(msg.encode())
            logging.debug(f'Sent %{self.addr}%{msg}%')
        except (socket.error, ConnectionError):
            logging.exception('Failed sending message')

    def __str__(self):
        return f'{self.addr[0]}:{self.addr[1]}'

