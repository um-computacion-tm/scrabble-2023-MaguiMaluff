from game.models import Cell, Player, BagTiles, Tiles

class Board:
    def __init__(self):
        self.grid =[[Cell(1, 'letter') for _ in range(15)] for _ in range (15)]

    def set_word_multiplier(self):
        word_multi = [
            (0,0), (7,0), (14,0), (0,7), (0,14), (7,14), (14,14)
        ]
        for i in range(15):
            for j in range(15):
                cell = self.grid[i][j]
                if (i,j) in word_multi:
                    cell.multiplier = 3
                    cell.multiplier_type = 'word'
                    
        for i in range(15):
            for j in range(15):
                not_there = [0, 5, 6, 7, 8, 9, 14]
                cell = self.grid[i][j]
                if i == j or (i + j == 14):
                    if (i and j) not in not_there:
                        cell.multiplier = 2
                        cell.multiplier_type = 'word'

    def set_letter_multiplier(self):
        letter_multi_2 = [
            (3,0), (11,0), (6,2), (8,2), (0,3), (14,3), (7,3),
            (2,6), (6,6), (8,6), (12,6), (3,7), (11,7), (2,8),
            (6,8), (8,8), (12,8), (14,11), (0,11), (7,11), (6,12),
            (8,12), (11,14), (3,14), 
        ]

        letter_multi_3 = [
            (1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1),
            (9,5), (9,9), (9,13), (13,5), (13,9),
        ]
        for i in range(15):
            for j in range(15):
                cell = self.grid[i][j]
                if (i,j) in letter_multi_2:
                    cell.multiplier = 2
                    cell.multiplier_type = 'letter'
                if (i,j) in letter_multi_3:
                    cell.multiplier = 3
                    cell.multiplier_type = "letter"

    def positions(self):
        self.set_letter_multiplier()
        self.set_word_multiplier()
    
    def validate_word_inside_board(self, word, location, orientation):
        word_list = []
        for letra in word:
            word_list.append(letra)
        
        i = location[0]
        j = location[1]

        if orientation == "V":
            j += len(word_list)
        if orientation == "H":
            i += len(word_list)

        if i > 14 or j > 14:
            return False
        else:
            return True

    def print_board(self):
        for row in self.grid:
            row_str = ""
            for cell in row:
                if cell.letter == None:
                    row_str += str(cell.multiplier) + " "
                if cell.letter != None:
                    row_str += str(cell.letter.letter) + " "
            print(row_str)

    def is_empty(self):
        if self.grid[7][7].letter == None:
            return True
        else:
            return False

    def validate_word_place_board(self, word, location, orientation):
        f = location[0]
        c = location[1]
        good = self.is_empty()
        celdas = []

        for i in range(len(word)):
            if orientation == "H":
                cell = self.grid[f][c + i]
            elif orientation == "V":
                cell = self.grid[f + i][c]
            if good == True:
                celdas.append(cell)
                if self.grid[7][7] in celdas:
                    return True
            elif good == False:
                if cell.letter != None and cell.letter.letter == word[i]:
                    return True
                elif self.validate_word_when_not_empty(word, location, orientation) == True:
                    return True
        return False
    
    def words_on_board(self, word, location, orientation):
        words_on_board = []
        word = [word, location, orientation]
        words_on_board.append(word)
        return words_on_board
    
    def validate_word_when_not_empty(self, word, location, orientation):
        f = location[0]
        c = location[1]
        las = len(word) - 1
        if orientation == "H":
            c += las
            if self.grid[f][c].letter == None and (self.grid[f - 1][c].letter != None or self.grid[f + 1][c].letter != None):
                return True
        elif orientation == "V":
            f += las
            if self.grid[f][c].letter == None and (self.grid[f][c - 1].letter != None or self.grid[f][c + 1].letter != None):
                return True