from game.models import Player, BagTiles
from game.board import Board
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
        for i in word:
            letritas.append(i)
        for j in self.current_player.bag_tiles:
            letritas_user.append(j.letter)
        
        validation = self.board.validate_word_inside_board(word, location, orientation)

        if validation == False:
            return False
        else:
            for w in range(len(letritas)):
                if letritas[w] in letritas_user:
                    posicion = letritas_user.index(letritas[w])
                    letritas_user.pop(posicion)
                else:
                    validation = False
        if validation == True:
            validation = self.get_word(word)

        return validation

    def get_word(self, word):
        res = dle.search_by_word(word)
        result = res.to_dict()
        if result == {'title': 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'}:
            return False
        else:
            return True

    def put_word(self, word, location, orientation):
        f = location[0]
        c = location[1]
        if orientation == "H":
            for j in range(len(word)):
                self.board.grid[f][c + j].letter = word[j]
        if orientation == "V":
            for i in range(len(word)):
                self.board.grid[f + i][c].letter = word[i]

    def calculate_word_value(self, word, location, orientation):
        f = location[0]
        c = location[1]
        counter = 0
        word_multiplier = 1
        cell = None

        self.put_word(word, location, orientation)

        for letrita in range(len(word)):
            if orientation == "H":
                    cell = self.board.grid[f][c + letrita]
            elif orientation == "V":
                    cell = self.board.grid[f + letrita][c]

            if cell.letter is None:
                    return 0
            
            if cell.state == False:
                 counter = counter + cell.letter.value
            
            if cell.multiplier_type == 'letter' and cell.state == True:
                counter = counter + (cell.letter.value * cell.multiplier * word_multiplier)

            if cell.multiplier_type == 'word' and word_multiplier != 1 and cell.state == True:
                counter = (counter + (cell.letter.value * word_multiplier))
                word_multiplier = cell.multiplier
                counter = counter * word_multiplier

            if cell.multiplier_type == 'word' and word_multiplier == 1 and cell.state == True:
                word_multiplier = cell.multiplier
                counter = ((counter + cell.letter.value) * word_multiplier)
            cell.used_cell(cell)
        return counter 