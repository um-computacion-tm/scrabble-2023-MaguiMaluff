from game.models import Board, Player, BagTiles
from pyrae import dle


class ScrabbleGame:
    def __init__(self, players_count, current_player = None):
        self.board = Board()
        self.board.positions()
        self.bag_tiles = BagTiles()
        self.players = []
        self.current_player = current_player
        for id in range(players_count):
            self.players.append(Player(id = id, bag_tiles = self.bag_tiles))


    def next_turn(self):
        if self.current_player is None:
            self.current_player = self.players[0]
        else:
            turn = self.players.index(self.current_player)
            if turn == (len(self.players) - 1):
                self.current_player = self.players[0]
            else:
                self.current_player = self.players[turn + 1]


    def validate_word(self, word, location, orientation):
        validation = True
        letritas = []
        letritas_user = []
        validation = self.board.validate_word_inside_board(word, location, orientation)

        if validation == False:
            return False
        
        for i in word:
            letritas.append(i)
        for j in self.current_player.bag_tiles:
            letritas_user.append(j.letter)
        for w in range(len(letritas)):
            if letritas[w] in letritas_user:
                posicion = letritas_user.index(letritas[w])
                letritas_user.pop(posicion)
            else:
                validation = False

        return validation

    def get_word(self, word):
        res = dle.search_by_word(word)
        res = res.to_dict()
        if res == {'title': 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'}:
            return False
        else:
            return True


        """
        obtener un diccionario (desde el doc de google)
        y tener la lista para verificar las palabras
        """

    def put_word():
        """
        modificar que el tablero con la palabra que ya esta validada
        """