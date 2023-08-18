import random, unittest

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
        ]
        random.shuffle(self.tiles)
    
    def take(self, count):
        tiles = []
        for _ in range(count):
            tiles.append(self.tiles.pop())
        return tiles
    
    def put(self, tiles):
        self.tiles.extend(tiles)

