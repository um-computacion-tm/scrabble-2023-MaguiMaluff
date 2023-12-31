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
            Tiles('L', 1), Tiles('L', 1), Tiles('C', 3), Tiles('H', 4),
            Tiles('L', 1), Tiles('L', 1), Tiles('R', 1), Tiles('R', 1),
            Tiles('R', 1), Tiles('R', 1), Tiles('R', 1), Tiles('U', 1),
            Tiles('U', 1), Tiles('U', 1), Tiles('U', 1), Tiles('U', 1),
            Tiles('T', 1), Tiles('T', 1), Tiles('T', 1), Tiles('T', 1),
            Tiles('D', 2), Tiles('D', 2), Tiles('D', 2), Tiles('D', 2),
            Tiles('D', 2), Tiles('G', 2), Tiles('G', 2), Tiles('C', 3),
            Tiles('C', 3), Tiles('C', 3), Tiles('C', 3), Tiles('B', 3),
            Tiles('B', 3), Tiles('M', 3), Tiles('M', 3), Tiles('P', 3),
            Tiles('P', 3), Tiles('H', 4), Tiles('H', 4), Tiles('F', 4),
            Tiles('V', 4), Tiles('Y', 4), Tiles('Q', 5), Tiles('J', 8), 
            Tiles('Ñ', 8), Tiles('R', 1), Tiles('R', 1), Tiles('X', 8), 
            Tiles('Z',10), Tiles('White', 0), Tiles('White', 0),
        ]
        random.shuffle(self.tiles)
    
    def take(self, count):
        random.shuffle(self.tiles)
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
        return_tiles = []
        num = len(list_tiles)
        may_to_men = sorted(list_tiles, reverse=True)
        new_tiles = self.bag_tiles.take(num)
        for i in may_to_men:
            return_tiles.append(self.tiles[i])
        self.bag_tiles.tiles.extend(return_tiles)
        for i in may_to_men:
            self.tiles[i] = new_tiles.pop()


    def take_to_seven(self):
        largo = len(self.tiles)
        to_take = 7 - largo
        if to_take == 0:
            pass
        else:
            new_tiles = self.bag_tiles.take(to_take)
            self.tiles.extend(new_tiles)

    def player_tiles(self, word):
        letritas = []
        letritas_user = []
        for i in word:
            letritas.append(i)
        for j in self.tiles:
            letritas_user.append(j.letter)
        for w in letritas:
                if w in letritas_user:
                    posicion = letritas_user.index(w)
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

    