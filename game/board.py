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

    def calculate_word_value(self, word:list):
        
        counter = 0
        word_multiplier = 1

        for i in range(len(word)):
            cell = word[i]

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