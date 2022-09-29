from SocketBase import *
from ClientHandler import ClientHandler


class Room:
    def __init__(self):
        self.players = []

    def get_count(self):
        return len(self.players)

    def enter(self, new_player):
        count = len(self.players)
        if count == 2:
            new_player.send_str('3013 The room is full')
        else:
            self.players.append(new_player)
            if count == 0:
                new_player.status = ClientHandler.Status.WAITING
                new_player.room = (self, False)
                new_player.send_str('3011 Wait')
            else:
                new_player.room = (self, True)
                for player in self.players:
                    player.status = ClientHandler.Status.STARTED
                    player.send_str('3012 Game started. Please guess true or false')

