from game.models import Board, Player, BagTiles

class ScrabbleGame:
    def __init__(self, players_count):
        self.board = Board()
        self.board.positions()
        self.bag_tiles = BagTiles()
        self.players = []
        for _ in range(players_count):
            self.players.append(Player(self.bag_tiles))
        self.turn = 0
    def playing(self):
        return True
    def next_turn(self):
        turn += 1
