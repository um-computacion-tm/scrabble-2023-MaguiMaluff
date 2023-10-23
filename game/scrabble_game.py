from game.models import Player, BagTiles
from game.board import Board
from pyrae import dle

class DictionaryConnectionError(Exception):
    pass

class WordDoesntExists(Exception):
    pass

class IsNotNumber(Exception):
    pass

class OutOfRange(Exception):
    pass

class InvalidWord(Exception):
    pass

class OutOfTiles(Exception):
    pass

class InvalidTask(Exception):
    pass

class InvalidPlace(Exception):
    pass

dle.set_log_level(log_level='CRITICAL')

class ScrabbleGame:
    def __init__(self, players_count, current_player = None):
        self.board = Board()
        self.board.positions()
        self.bag_tiles = BagTiles()
        self.players = []
        self.current_player = current_player
        self.cells_values = {}
        self.playing = True
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
        if not self.board.validate_word_inside_board(word, location, orientation):
            raise OutOfRange("Palabra fuera de rango")
        elif not self.current_player.player_tiles(word):
            raise OutOfTiles("No tiene las fichas necesarias")
        elif not self.get_word(word):
            raise InvalidWord("La palabra no es valida")
        else:
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
        if players_tiles == False:
            raise OutOfTiles()
        else:
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

    def player_tiles_list(self): ###TESTEAR
        letras = []
        for i in range(len(self.current_player.tiles)):
            letras.append(self.current_player.tiles[i].letter)
        return letras

    def calculate_word_value(self, word, location, orientation):
        f = location[0]
        c = location[1]
        counter = 0
        word_multiplier = 1

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

    def vertical_word_check_for_sum(self, word, location):
        izquierda = []
        derecha = []
        new_words = []
        search = None
        for i in range(len(word)): 
            f = location[0] + i
            c = location[1]
            celda_actual = self.board.grid[f][c].letter
            if c - 1 >= 0:
                celda_i = self.board.grid[f][c - 1].letter
            if c + 1 <= 14:
                celda_d = self.board.grid[f][c + 1].letter
            if  celda_i != None and celda_d == None and celda_actual == None:
                izquierda.append((f , c - 1))
                search = self.board.get_word_from_cell(izquierda)
                if search[0][2] == "V":
                    new_word_list = self.get_horizontal_word((f , c), word[i])
                    new_word = new_word_list[0]
                    if self.get_word(new_word) == False:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
                    else:
                        new_words.append(new_word_list)
                else:
                    new_word = search[0][0] + word[i]
                    if self.get_word(new_word) == True:
                        self.board.words_on_board[search[0][1]][0] = new_word
                        new_words.append([new_word, self.board.words_on_board[search[0][1]][2] , "V" ])
                    else:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
            elif celda_d != None and celda_i == None and celda_actual == None:
                derecha.append((f , c + 1))
                search = self.board.get_word_from_cell(derecha)
                if search[0][2] == "V":
                    new_word_list = self.get_horizontal_word((f , c), word[i])
                    new_word = new_word_list[0]
                    if self.get_word(new_word) == False:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
                    else:
                        new_words.append(new_word_list)
                else:
                    new_word = word[i] + search[0][0] 
                    if self.get_word(new_word) == True:
                        self.board.words_on_board[search[0][1]][0] = new_word
                        new_words.append([new_word, (f , c), "H" ])
                    else:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
            elif celda_d != None and celda_i != None and celda_actual == None:
                derecha.append((f , c + 1))
                if search == None:
                    search = self.board.get_word_from_cell(derecha)
                for w in range(len(search)):
                    if search[w][2] == "V":
                        new_word_list = self.get_horizontal_word((f , c), word[i])
                        new_word = new_word_list[0]
                        if self.get_word(new_word) == False:
                            raise WordDoesntExists("La palabra ", new_word, " no existe")
                        else:
                            new_words.append(new_word_list)
                    
        return new_words

    def horizontal_word_check_for_sum(self, word, location):
        up = []
        down = []
        new_words = []
        search = None
        for i in range(len(word)):
            f = location[0]
            c = location[1] + i
            celda_actual = self.board.grid[f][c].letter
            if f + 1 <= 14:
                celda_u = self.board.grid[f - 1][c].letter
            if f - 1 >= 0:
                celda_d = self.board.grid[f + 1][c].letter
            if  celda_u != None and celda_d == None and celda_actual == None:
                up.append((f - 1, c))
                search = self.board.get_word_from_cell(up)
                if search[0][2] == "H":
                    new_word_list = self.get_vertical_word((f , c), word[i])
                    new_word = new_word_list[0]
                    if self.get_word(new_word) == False:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
                    else:
                        new_words.append(new_word_list)
                else:
                    new_word = search[0][0] + word[i] 
                    if self.get_word(new_word) == True:
                        self.board.words_on_board[search[0][1]][0] = new_word
                        new_words.append([new_word, self.board.words_on_board[search[0][1]][2], "V" ])
                    else:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
            elif celda_d != None and celda_u == None and celda_actual == None:
                down.append((f + 1 , c))
                search = self.board.get_word_from_cell(down)
                if search[0][2] == "H":
                    new_word_list = self.get_vertical_word((f , c), word[i])
                    new_word = new_word_list[0]
                    if self.get_word(new_word) == False:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
                    else:
                            new_words.append(new_word_list)
                else:
                    new_word = word[i] + search[0][0] 
                    if self.get_word(new_word) == True:
                        self.board.words_on_board[search[0][1]][0] = new_word
                        new_words.append([new_word, (f , c), "V" ])
                    else:
                        raise WordDoesntExists("La palabra ", new_word, " no existe")
            elif celda_d != None and celda_u != None and celda_actual == None:
                up.append((f + 1, c))
                if search == None:
                    search = self.board.get_word_from_cell(up)
                for w in range(len(search)):
                    if search[w][2] == "H":
                        new_word_list = self.get_vertical_word((f , c), word[i])
                        new_word = new_word_list[0]
                        if self.get_word(new_word) == False:
                            raise WordDoesntExists("La palabra ", new_word, " no existe")
                        else:
                            new_words.append(new_word_list)
        return new_words

    def get_vertical_word(self, cell, letter):
        k = 1
        new_word = letter
        new_word_info = ["V"]
        while letter != None:
            f = cell[0]
            c = cell[1]
            if f + k <= 14 and f - k >= 0:
                celda_1 = self.board.grid[f + k][c].letter
                celda_2 = self.board.grid[f - k][c].letter
                if celda_1 != None:
                    letter_1 = celda_1.letter
                    new_word += letter_1
                if celda_2 != None:
                    letter_2 = celda_2.letter
                    new_word = letter_2 + new_word
                    if (f - k) < (f - k + 1):
                        new_word_info.insert(0, (f - k, c))
                else: 
                    break
                k +=1
        if len(new_word_info) < 2:
            new_word_info.insert(0, cell)
        new_word_info.insert(0,new_word)
        return new_word_info

    
    def get_horizontal_word(self, cell, letter):
        k = 1
        new_word = letter
        new_word_info = ["H"]
        while letter != None:
            f = cell[0]
            c = cell[1]
            if c + k <= 14 and c - k >= 0:
                celda_1 = self.board.grid[f][c - k].letter
                celda_2 = self.board.grid[f][c + k].letter
                if celda_1 != None:
                    letter_1 = celda_1.letter
                    new_word = letter_1 + new_word
                    if (c - k) < (c - k + 1):
                        new_word_info.insert(0, (f, c - k))
                if celda_2 != None:
                    letter_2 = celda_2.letter
                    new_word += letter_2
                else: 
                    break
                k +=1
        if len(new_word_info) < 2:
            new_word_info.insert(0, cell)
        new_word_info.insert(0, new_word)      
        return new_word_info   


    def validate_word_place_board(self, word, location, orientation):
        f = location[0]
        c = location[1]
        good = self.board.is_empty()
        celdas = []
        for i in range(len(word)):
            if orientation == "H":
                cell = self.board.grid[f][c + i]
            elif orientation == "V":
                cell = self.board.grid[f + i][c]
            if good == True:
                celdas.append(cell)
                if self.board.grid[7][7] in celdas:
                    return True
            elif good == False:
                if (cell.letter != None and cell.letter.letter == word[i]):
                    self.current_player.tiles.append(cell.letter) ###Testear
                    return True
                if self.board.validate_word_when_not_empty(word, location, orientation) == True:
                    return True
        return False

    def is_playing(self):
        return self.playing
    
    def printbb(self):
        self.board.print_board()

    def get_player_info(self):
        print(self.current_player.points)
        print(self.player_tiles_list())

    def add_word(self, word, location, orientation):
        try:
            first_validation = self.validate_word_place_board(word, location, orientation)
            self.validate_word(word, location, orientation)
            if first_validation == False:
                raise InvalidPlace("Su palabra debe agregar o pasar por otra palabra. Si es el primer turno, debe pasar por la celda (7 , 7)")
                
            if orientation == "H":
                third_validation = self.horizontal_word_check_for_sum(word, location)
            elif orientation == "V":
                third_validation = self.vertical_word_check_for_sum(word, location)
                
            self.put_word(word, location, orientation)
            return True
        except Exception as e:
            print(e)
        
    