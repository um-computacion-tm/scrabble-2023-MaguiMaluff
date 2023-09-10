from game.models import Board, Player, BagTiles

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

        """
        1 - las letras estan en la bolsa del usuario
        2 - la locacation y orientacion no se pasa del tablero
        3 - es una palabra valida
        """

    def get_word():
        """
        obtener un diccionario (desde el doc de google)
        y tener la lista para verificar las palabras
        """

    def put_word():
        """
        modificar que el tablero con la palabra que ya esta validada
        """