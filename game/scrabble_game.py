from game.models import Player, BagTiles
from game.board import Board
from pyrae import dle

class DictionaryConnectionError(Exception):
    pass

class WordDoesntExists(Exception):
    pass

class ScrabbleGame:
    def __init__(self, players_count, current_player = None):
        self.board = Board()
        self.board.positions()
        self.bag_tiles = BagTiles()
        self.players = []
        self.current_player = current_player
        self.cells_values = {}
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
        if self.board.validate_word_inside_board(word, location, orientation) == False:
            return False
        elif self.current_player.player_tiles(word) == False:
            return False
        elif self.get_word == False:
            return False
        return True


    def get_word(self, word):
        res = dle.search_by_word(word)
        result = res.to_dict()
        if res is None:
            raise DictionaryConnectionError()
        if result == {'title': 'Diccionario de la lengua española | Edición del Tricentenario | RAE - ASALE'}:
            return False
        else:
            return True

    def put_word(self, word, location, orientation):
        players_tiles = self.current_player.tiles

        for i in range(len(word)):
            f = location[0]
            c = location[1]
            if orientation == "H":
                cell = self.board.grid[f][c + i]
            elif orientation == "V":
                cell = self.board.grid[f + i][c]
            tile = self.get_tile_from_player(players_tiles, word[i])
            if tile != None:
                cell.letter = tile
                self.current_player.tiles.remove(tile)
        self.board.list_of_words(word, location, orientation)    

    def get_tile_from_player(self, player_tiles, letter):
        for tiles in player_tiles:
            if tiles.letter == letter:
                return tiles
        return None


    def calculate_word_value(self, word, location, orientation):
        f = location[0]
        c = location[1]
        counter = 0
        word_multiplier = 1

        self.put_word(word, location, orientation)

        for letrita in range(len(word)):
            if orientation == "H":
                cell = self.board.grid[f][c + letrita]
            elif orientation == "V":
                cell = self.board.grid[f + letrita][c]

            if cell.letter.letter is None:
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
        self.current_player.points += counter
        return counter 

    def calculate_word_without_any_multiplier(self, word, location, orientation):
        f = location[0]
        c = location[1]
        counter = 0

        for letrita in range(len(word)):
            if orientation == "H":
                cell = self.board.grid[f][c + letrita]
            elif orientation == "V":
                cell = self.board.grid[f + letrita][c]
            counter = counter + cell.letter.value
        
        for i in range(len(word)):
            f = location[0]
            c = location[1]
            if orientation == "H":
                c += i
            elif orientation == "V":
                f += i
            self.cells_values[(f , c)] = counter

    def vertical_word_check_for_sum_1(self, word, location):
        izquierda = []
        derecha = []
        for i in range(len(word)): 
            f = location[0] + i
            c = location[1]
            if self.board.grid[f][c - 1].letter != None and self.board.grid[f][c + 1].letter == None:
                izquierda.append((f , c - 1))
                search = self.board.get_word_from_cell(izquierda)
                new_word = search[0] + word[i]
                if self.get_word(new_word) == True:
                    self.board.words_on_board[search[1]][0] = new_word
                    return f'{new_word}, Sumando'
                else:
                    raise WordDoesntExists()
                
            elif self.board.grid[f][c - 1].letter == None and self.board.grid[f][c + 1].letter != None:
                derecha.append((f , c + 1))
                search = self.board.get_word_from_cell(derecha)
                new_word = word[i] +search[0] 
                if self.get_word(new_word) == True:
                    self.board.words_on_board[search[1]][0] = new_word
                    return f'{new_word}, Sumando'
                else:
                    raise WordDoesntExists()

    def playing(self, word, location, orientation):
        word = word.upper()
        orientation = orientation.upper()
        self.board.validate_word_place_board(word, location, orientation)
        self.validate_word(word, location, orientation)
        if location == "V":
            self.board.vertical_word_check_for_sum_1(word, location)

        
