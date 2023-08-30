import random
class Tiles:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value

class BagTiles:
    def __init__(self):
        self.tiles = [
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('A', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('E', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('O', 1),
            Tiles('I', 1),
            Tiles('I', 1),
            Tiles('I', 1),
            Tiles('I', 1),
            Tiles('I', 1),
            Tiles('I', 1),
            Tiles('S', 1),
            Tiles('S', 1),
            Tiles('S', 1),
            Tiles('S', 1),
            Tiles('S', 1),
            Tiles('S', 1),
            Tiles('N', 1),
            Tiles('N', 1),
            Tiles('N', 1),
            Tiles('N', 1),
            Tiles('N', 1),
            Tiles('L', 1),
            Tiles('L', 1),
            Tiles('L', 1),
            Tiles('L', 1),
            Tiles('R', 1),
            Tiles('R', 1),
            Tiles('R', 1),
            Tiles('R', 1),
            Tiles('R', 1),
            Tiles('U', 1),
            Tiles('U', 1),
            Tiles('U', 1),
            Tiles('U', 1),
            Tiles('U', 1),
            Tiles('T', 1),
            Tiles('T', 1),
            Tiles('T', 1),
            Tiles('T', 1),
            Tiles('D', 2),
            Tiles('D', 2),
            Tiles('D', 2),
            Tiles('D', 2),
            Tiles('D', 2),
            Tiles('G', 2),
            Tiles('G', 2),
            Tiles('C', 3),
            Tiles('C', 3),
            Tiles('C', 3),
            Tiles('C', 3),
            Tiles('B', 3),
            Tiles('B', 3),
            Tiles('M', 3),
            Tiles('M', 3),
            Tiles('P', 3),
            Tiles('P', 3),
            Tiles('H', 4),
            Tiles('H', 4),
            Tiles('F', 4),
            Tiles('V', 4),
            Tiles('Y', 4),
            Tiles('CH',5),
            Tiles('Q', 5),
            Tiles('J', 8),
            Tiles('LL',8),
            Tiles('Ñ', 8),
            Tiles('RR',8),
            Tiles('X', 8),
            Tiles('Z',10),
            Tiles('White', 0),
            Tiles('White', 0),
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
        self.grid =[[Cell(1, '') for _ in range(15)] for _ in range (15)]

    def positions(self):
        self.grid[0][0].multiplier = 3
        self.grid[0][0].multiplier_type = 'word'
        self.grid[7][0].multiplier = 3
        self.grid[7][0].multiplier_type= 'word'
        self.grid[14][0].multiplier = 3
        self.grid[14][0].multiplier_type = 'word'

        self.grid[0][7].multiplier = 3
        self.grid[0][7].multiplier_type= 'word'
        self.grid[0][14].multiplier = 3
        self.grid[0][14].multiplier_type= 'word'

        self.grid[7][14].multiplier = 3
        self.grid[7][14].multiplier_type= 'word'
        self.grid[14][14].multiplier = 3
        self.grid[14][14].multiplier_type= 'word'

        for i in range(15):
            for j in range(14):
                not_there = [0, 5, 6, 7, 8, 9, 14]
                if i == j or (i + j == 14):
                    if (i and j) not in not_there:
                        self.grid[i][j].multiplier = 2
                        self.grid[i][j].multiplier_type = 'word'

        self.grid[3][0].multiplier = 2
        self.grid[3][0].multiplier_type = 'letter'
        self.grid[11][0].multiplier = 2
        self.grid[11][0].multiplier_type = 'letter'

        self.grid[6][2].multiplier = 2
        self.grid[6][2].multiplier_type = 'letter'
        self.grid[8][2].multiplier = 2
        self.grid[8][2].multiplier_type= 'letter'

        self.grid[0][3].multiplier = 2
        self.grid[0][3].multiplier_type = 'letter'
        self.grid[14][3].multiplier = 2
        self.grid[14][3].multiplier_type= 'letter'
        self.grid[7][3].multiplier = 2
        self.grid[7][3].multiplier_type= 'letter'

        self.grid[2][6].multiplier = 2
        self.grid[2][6].multiplier_type = 'letter'
        self.grid[6][6].multiplier = 2
        self.grid[6][6].multiplier_type= 'letter'
        self.grid[8][6].multiplier = 2
        self.grid[8][6].multiplier_type= 'letter'
        self.grid[12][6].multiplier = 2
        self.grid[12][6].multiplier_type= 'letter'

        self.grid[3][7].multiplier = 2
        self.grid[3][7].multiplier_type= 'letter'
        self.grid[11][7].multiplier = 2
        self.grid[11][7].multiplier_type = 'letter'

        self.grid[2][8].multiplier = 2
        self.grid[2][8].multiplier_type = 'letter'
        self.grid[6][8].multiplier = 2
        self.grid[6][8].multiplier_type= 'letter'
        self.grid[8][8].multiplier = 2
        self.grid[8][8].multiplier_type= 'letter'
        self.grid[12][8].multiplier = 2
        self.grid[12][8].multiplier_type= 'letter'

        self.grid[14][11].multiplier = 2
        self.grid[14][11].multiplier_type = 'letter'
        self.grid[0][11].multiplier = 2
        self.grid[0][11].multiplier_type= 'letter'
        self.grid[7][11].multiplier = 2
        self.grid[7][11].multiplier_type= 'letter'

        self.grid[6][12].multiplier = 2
        self.grid[6][12].multiplier_type = 'letter'
        self.grid[8][12].multiplier = 2
        self.grid[8][12].multiplier_type= 'letter'

        self.grid[11][14].multiplier = 2
        self.grid[11][14].multiplier_type= 'letter'
        self.grid[3][14].multiplier = 2
        self.grid[3][14].multiplier_type = 'letter'

        self.grid[1][5].multiplier = 3
        self.grid[1][5].multiplier_type = 'letter'
        self.grid[1][9].multiplier = 3
        self.grid[1][9].multiplier_type= 'letter'

        self.grid[5][1].multiplier = 3
        self.grid[5][1].multiplier_type = 'letter'
        self.grid[5][5].multiplier = 3
        self.grid[5][5].multiplier_type= 'letter'
        self.grid[5][9].multiplier = 3
        self.grid[5][9].multiplier_type = 'letter'
        self.grid[5][13].multiplier = 3
        self.grid[5][13].multiplier_type= 'letter'

        self.grid[9][1].multiplier = 3
        self.grid[9][1].multiplier_type = 'letter'
        self.grid[9][5].multiplier = 3
        self.grid[9][5].multiplier_type= 'letter'
        self.grid[9][9].multiplier = 3
        self.grid[9][9].multiplier_type = 'letter'
        self.grid[9][13].multiplier = 3
        self.grid[9][13].multiplier_type= 'letter'

        self.grid[13][5].multiplier = 3
        self.grid[13][5].multiplier_type = 'letter'
        self.grid[13][9].multiplier = 3
        self.grid[13][9].multiplier_type= 'letter'

class Cell:
    def __init__(self, multiplier, multiplier_type):
        self.multiplier = multiplier
        self.multiplier_type = multiplier_type
        self.letter = None

    def add_letter(self, letter):
        self.letter = letter

    def calculate_value(self):
        if self.letter is None:
            return 0
        if self.multiplier_type == 'letter':
            return self.letter.value * self.multiplier
        else:
            return self.letter.value

    def used_cell(self):
        self.multiplier = 1
        self.multiplier_type = ''


