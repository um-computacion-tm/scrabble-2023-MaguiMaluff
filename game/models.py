import random
class Tiles:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

class BagTiles:
    def __init__(self):
        self.tiles = [
            Tiles('A', 1), Tiles('A', 1), Tiles('A', 1), Tiles('A', 1),
            Tiles('A', 1), Tiles('A', 1), Tiles('A', 1), Tiles('A', 1),
            Tiles('A', 1), Tiles('A', 1), Tiles('A', 1), Tiles('A', 1), 
            Tiles('E', 1), Tiles('E', 1), Tiles('E', 1), Tiles('E', 1),
            Tiles('E', 1), Tiles('E', 1), Tiles('E', 1), Tiles('E', 1),
            Tiles('E', 1), Tiles('E', 1), Tiles('E', 1), Tiles('E', 1),
            Tiles('O', 1), Tiles('O', 1), Tiles('O', 1), Tiles('O', 1),
            Tiles('O', 1), Tiles('O', 1), Tiles('O', 1), Tiles('O', 1),
            Tiles('O', 1), Tiles('I', 1), Tiles('I', 1), Tiles('I', 1),
            Tiles('I', 1), Tiles('I', 1), Tiles('I', 1), Tiles('S', 1),
            Tiles('S', 1), Tiles('S', 1), Tiles('S', 1), Tiles('S', 1),
            Tiles('S', 1), Tiles('N', 1), Tiles('N', 1), Tiles('N', 1),
            Tiles('N', 1), Tiles('N', 1), Tiles('L', 1), Tiles('L', 1),
            Tiles('L', 1), Tiles('L', 1), Tiles('R', 1), Tiles('R', 1),
            Tiles('R', 1), Tiles('R', 1), Tiles('R', 1), Tiles('U', 1),
            Tiles('U', 1), Tiles('U', 1), Tiles('U', 1), Tiles('U', 1),
            Tiles('T', 1), Tiles('T', 1), Tiles('T', 1), Tiles('T', 1),
            Tiles('D', 2), Tiles('D', 2), Tiles('D', 2), Tiles('D', 2),
            Tiles('D', 2), Tiles('G', 2), Tiles('G', 2), Tiles('C', 3),
            Tiles('C', 3), Tiles('C', 3), Tiles('C', 3), Tiles('B', 3),
            Tiles('B', 3), Tiles('M', 3), Tiles('M', 3), Tiles('P', 3),
            Tiles('P', 3), Tiles('H', 4), Tiles('H', 4), Tiles('F', 4),
            Tiles('V', 4), Tiles('Y', 4), Tiles('CH',5), Tiles('Q', 5),
            Tiles('J', 8), Tiles('LL',8), Tiles('Ñ', 8), Tiles('RR',8),
            Tiles('X', 8), Tiles('Z',10), Tiles('White', 0), Tiles('White', 0),
        ]
        random.shuffle(self.tiles)

    def take(self, count):
        tiles = []
        for _ in range(count):
            tiles.append(self.tiles.pop())
        return tiles
    
    def put(self, tiles):
        self.tiles.extend(tiles)

class Player:
    def __init__(self, bag_tiles):
        self.tiles = bag_tiles.take(7)
        self.bag_tiles = bag_tiles
    

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

class Cell:
    def __init__(self, multiplier = 1, multiplier_type = 'letter', letter = None, state = True):
        self.multiplier = multiplier
        self.multiplier_type = multiplier_type
        self.letter = letter
        self.state = state

    def add_letter(self, letter):
        self.letter = letter

    def calculate_value(self):
        if self.letter is None:
            return 0
        if self.multiplier_type == 'letter':
            return self.letter.value * self.multiplier
        else:
            return self.letter.value

    def used_cell(self, cell):
        self.multiplier = 1
        self.multiplier_type = 'letter'
        self.state = False


