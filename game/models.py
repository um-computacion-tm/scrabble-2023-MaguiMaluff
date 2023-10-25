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
    def __init__(self, id:int, bag_tiles:BagTiles):
        self.tiles = bag_tiles.take(7)
        self.bag_tiles = bag_tiles
        self.points = 0
        self.id = id

    def change_tiles(self, list_tiles):
        num = len(list_tiles)
        new_tiles = self.bag_tiles.take(num)
        self.bag_tiles.tiles.extend(list_tiles)
        self.tiles.extend(new_tiles)


    def take_to_seven(self):
        largo = len(self.tiles)
        to_take = 7 - largo
        self.bag_tiles.take(to_take)

    def player_tiles(self, word):
        letritas = []
        letritas_user = []
        for i in word:
            letritas.append(i)
        for j in self.tiles:
            letritas_user.append(j.letter)
        for w in range(len(letritas)):
                if letritas[w] in letritas_user:
                    posicion = letritas_user.index(letritas[w])
                    letritas_user.pop(posicion)
                else:
                    return False
        return True

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

    