import random
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

    def check_result(self):
        for player in self.players:
            if player.guess is None:
                return

        ans = random.randint(0,1)
        logging.debug(f'Generated %{ans}%')

        if self.players[0].guess == self.players[1].guess:
            self.tie()
        else:
            loser = self.players[0].guess == ans
            self.defeat(loser)

        for player in self.players:
            player.status = ClientHandler.Status.HALL

    def tie(self):
        for player in self.players:
            player.send_str('3023 The result is a tie')
        self.clear()

    def defeat(self, loser, disconnected=False):
        self.players[not loser].send_str('3021 You are the winner')
        if not disconnected:
            self.players[loser].send_str('3022 You lost this game')
        self.clear()

    def clear(self):
        for player in self.players:
            player.status = ClientHandler.Status.HALL
            player.room = None
        self.players = []

