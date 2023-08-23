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
    def __init__(self):
        self.tiles = []
        
class Board:
    def __init__(self):
        self.grid =[
            [Cell(1,'') for _ in range(15)]
            for _ in range (15)
        ]

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