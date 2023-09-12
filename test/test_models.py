import unittest
from game.models import Tiles, BagTiles, Player, Cell
from game.board import Board
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
        bag_tiles = BagTiles()
        player_1 = Player(1, bag_tiles)
        self.assertEqual(len(player_1.tiles),7,)

class TestCell(unittest.TestCase):
    def test_init(self):
        cell = Cell(multiplier = 2, multiplier_type = 'letter',)
        self.assertEqual(cell.multiplier, 2)
        self.assertEqual(cell.multiplier_type, 'letter')
        self.assertIsNone(cell.letter)
        self.assertEqual(cell.calculate_value(),0,)

    def test_add_letter(self):
        cell = Cell(multiplier = 1, multiplier_type = 'letter')
        letter = Tiles(letter = 'P', value = 3)
        cell.add_letter(letter)
        self.assertEqual(cell.letter, letter)

    def test_cell_value(self):
        board = Board()
        board.positions()
        cell= board.grid[11][0]
        letter = Tiles(letter = 'P', value = 3)
        cell.add_letter(letter)
        self.assertEqual(cell.calculate_value(),6)

class TestCalculateWordValue(unittest.TestCase):
    def test_simple(self):
        board = Board()
        board.positions()
        word = [
            Cell(letter = Tiles('C', 1),),
            Cell(letter = Tiles('A', 1),),
            Cell(letter = Tiles('S', 2),),
            Cell(letter = Tiles('A', 1),),
        ]
        value = board.calculate_word_value(word)
        self.assertEqual(value, 5)

    def test_with_letter_multiplier(self):
        board = Board()
        board.positions()
        word = [
            Cell(letter = Tiles('C', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('S', 2), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[9][1].multiplier,  multiplier_type = board.grid[9][1].multiplier_type) ,
        ]
        value = board.calculate_word_value(word)
        self.assertEqual(value, 7)

    def test_with_word_multiplier(self):
        board = Board()
        board.positions()
        word = [
            Cell(letter = Tiles('C', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('S', 2), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[11][3].multiplier, multiplier_type = board.grid[11][3].multiplier_type) ,
        ]
        value = board.calculate_word_value(word)
        self.assertEqual(value, 10)

    def test_with_letter_word_multiplier(self):
        board = Board()
        board.positions()
        word = [
            Cell(multiplier = board.grid[5][1].multiplier, multiplier_type = board.grid[5][1].multiplier_type, letter = Tiles('C', 1)),
            Cell(letter = Tiles('A', 1)),
            Cell(letter = Tiles('S', 2), multiplier = board.grid[3][3].multiplier, multiplier_type = board.grid[3][3].multiplier_type),
            Cell(letter = Tiles('A', 1)),
        ]
        value = board.calculate_word_value(word)
        self.assertEqual(value, 14)

    def test_with_letter_word_multiplier_no_active(self):
        board = Board()
        board.positions()
        word = [
                Cell(
                multiplier=3,
                multiplier_type='letter',
                letter=Tiles('C', 1)
            ),
            Cell(letter=Tiles('A', 1)),
            Cell(
                letter=Tiles('S', 2),
                multiplier=2,
                multiplier_type='word', state = False
            ),
            Cell(letter = Tiles('A', 1),),
        ]
        value = board.calculate_word_value(word)
        self.assertEqual(value, 7)

if __name__ == '__main__':
    unittest.main()