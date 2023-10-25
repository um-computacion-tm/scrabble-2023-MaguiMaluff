from game.models import Cell, Player, BagTiles, Tiles


class Board:
    def __init__(self):
        self.grid =[[Cell(1, 'letter') for _ in range(15)] for _ in range (15)]
        self.words_on_board = []
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
        print("  ")
        first_row = "x\y    "
        for i in range(15):
            if i <= 9:
                first_row += str(i) + "    "
            else:
                first_row += str(i) + "   "
        print(first_row)
        for row in range(len(self.grid)):
            if row >= 10:
                row_str = "   "
            else:
                row_str = "    "
            for cell in self.grid[row]:
                if cell.letter == None:
                    row_str += "[" + str(cell.multiplier)
                    if cell.multiplier_type == "letter":
                        row_str +=  "L] "
                    else:
                        row_str +=  "W] "
                if cell.letter != None:
                    row_str += "  " + str(cell.letter.letter) + "  "
            print(row, row_str)

    def is_empty(self):
        if self.grid[7][7].letter == None:
            return True
        else:
            return False
    
    def list_of_words(self, word, location, orientation):
        word_info = [word, orientation]
        celdas = []
        for i in range(len(word)):
            f = location[0]
            c = location[1]
            if orientation == "H":
                c += i
            elif orientation == "V":
                f += i
            celdas.append((f , c))
        word_info.extend(celdas)
        self.words_on_board.append(word_info)
        return self.words_on_board
    
    def validate_word_when_not_empty(self, word, location, orientation):
        count = 0
        for i in range(len(word)):
            f = location[0]
            c = location[1]
            if orientation == "H":
                c = c + i
            elif orientation == "V":
                f = f + i
            if 0 <= f < 14 and 0 <= c < 14:
                tiles = [ self.grid[f + 1][c],  ###Arriba
                          self.grid[f - 1][c],  ###Abajo
                          self.grid[f][c + 1],  ###Derecha
                          self.grid[f][c - 1],] ###Izquierda
                for t in tiles:
                    if t.letter is not None:
                        count += 1
        if count != 0:
            return True
        else:
            return False
    
    def get_word_from_cell(self, list):
        words = []
        for i in list:
            for j in range(len(self.words_on_board)):
                if i in self.words_on_board[j]:
                    words.append([self.words_on_board[j][0], j, self.words_on_board[j][1]])
        return words
        
