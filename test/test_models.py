import unittest
from game.models import Tiles, BagTiles, Player, Board, Cell
from unittest.mock import patch

class TestTiles(unittest.TestCase):
    def test_tiles(self):
        tiles = Tiles('A', 1)
        self.assertEqual(tiles.letter, 'A')
        self.assertEqual(tiles.value,  1)

class TestBagTiles(unittest.TestCase):
    @patch('random.shuffle')
    def test_bag_tiles(self, patch_shuffle):
        bag = BagTiles ()
        self.assertEqual(
            len(bag.tiles),
            100,
        )
        self.assertEqual(
            patch_shuffle.call_count,
            1,
        )
        self.assertEqual(
            patch_shuffle.call_args [0] [0], 
            bag.tiles,)
        
    def test_take(self):
        bag = BagTiles()
        tiles = bag.take(2)
        self.assertEqual(
            len(bag.tiles),
            98,)
        self.assertEqual(
            len(tiles),
            2,)

    def test_put(self):
        bag = BagTiles()
        put_tiles = [Tiles('Z', 10), Tiles('Y', 4)]
        bag.put(put_tiles)
        self.assertEqual(
            len(bag.tiles), 
            102,)
        

class TestPlayer(unittest.TestCase):
    def test_init(self):
        player_1 = Player()
        self.assertEqual(len(player_1.tiles),0,)

class TestBoard(unittest.TestCase):
    def test_init(self):
        board = Board()
        self.assertEqual(len(board.grid),15,)
        self.assertEqual(len(board.grid[0]),15,)

class TestCell(unittest.TestCase):
    def test_init(self):
        cell = Cell(multiplier = 2, multiplier_type = 'letter',)
        self.assertEqual(cell.multiplier, 2)
        self.assertEqual(cell.multiplier_type, 'letter')
        self.assertIsNone(self.letter)

    def test_add_letter(self):
        cell = Cell(multiplier = 1, multiplier_type = 'letter')
        letter = Tiles(letter = 'P', value = 3)
        cell.add_letter(letter = letter)
        self.assertEqual(cell.letter == letter)

    def test_cell_value(self):
        cell = Cell(multiplier=1, multiplier_type='letter')
        letter = Tiles(letter = 'P', value = 3)
        cell.add_letter(letter = letter)
        self.assertEqual(cell.calculate_value(),3,)

    def test_multiplier_word(self):
        cell = Cell(multiplier = 2, multiplier_type= 'word')
        letter = Tiles(letter = 'P', value = 3)
        cell.add_letter(letter = letter)
        self.assertEqual(cell.calculate_value(),6,)

if __name__ == '__main__':
    unittest.main()