import unittest
from game.models import Tiles, BagTiles, Player, Board, Cell
from game.value import calculate_word_value
from game.scrabble_game import ScrabbleGame
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
    
    def test_positions_word_3(self):
        board = Board()
        board.positions()
        self.assertEqual(board.grid[0][0].multiplier, 3)
        self.assertEqual(board.grid[0][0].multiplier_type, 'word')
        self.assertEqual(board.grid[7][0].multiplier, 3)
        self.assertEqual(board.grid[7][0].multiplier_type, 'word')
        self.assertEqual(board.grid[14][14].multiplier, 3)
        self.assertEqual(board.grid[14][14].multiplier_type, 'word')
        self.assertNotEqual(board.grid[0][14], board.grid[5][7])

    def test_positions_word_3(self):
        board = Board()
        board.positions()
        self.assertEqual(board.grid[1][1].multiplier, 2)
        self.assertEqual(board.grid[2][12].multiplier_type, 'word')
        self.assertEqual(board.grid[11][3].multiplier, 2)
        self.assertEqual(board.grid[1][13].multiplier_type, 'word')
        self.assertNotEqual(board.grid[0][14].multiplier, 2)
        self.assertNotEqual(board.grid[7][7].multiplier, 2)
        self.assertNotEqual(board.grid[6][7].multiplier, 2)

    def test_positions_letter_2(self):
        board = Board()
        board.positions()
        self.assertEqual(board.grid[0][3].multiplier, 2)
        self.assertEqual(board.grid[0][3].multiplier_type, 'letter')
        self.assertEqual(board.grid[6][6].multiplier, 2)
        self.assertEqual(board.grid[6][6].multiplier_type, 'letter')
        self.assertNotEqual(board.grid[0][14].multiplier, 2)
        self.assertNotEqual(board.grid[7][7].multiplier, 2)
        self.assertNotEqual(board.grid[6][1].multiplier, 2)

class TestScrabbleGame(unittest.TestCase):
    def test_init(self):
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertIsNotNone(scrabble_game.board)
        self.assertEqual(
            len(scrabble_game.players),
            3,
        )
        self.assertIsNotNone(scrabble_game.bag_tiles)

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
        print(cell.multiplier)
        letter = Tiles(letter = 'P', value = 3)
        cell.add_letter(letter)
        self.assertEqual(cell.calculate_value(),6)


class TestCalculateWordValue(unittest.TestCase):
    def test_simple(self):
        board = Board()
        board.positions()
        wordd = [
            Cell(Tiles('C', 1), board.grid[7][7]),
            Cell(Tiles('A', 1), board.grid[7][8]),
            Cell(Tiles('S', 2), board.grid[7][9]),
            Cell(Tiles('A', 1), board.grid[7][10]),
        ]
        value = calculate_word_value(wordd)
        self.assertEqual(value, 5)
    def test_with_letter_multiplier(self):
        board = Board()
        board.positions()
        word = [
            Cell(letter=Tiles('C', 1), cell = board.grid[7][7]),
            Cell(letter=Tiles('A', 1), cell = board.grid[7][7]),
            Cell(letter=Tiles('S', 2), cell = board.grid[7][7]),
            Cell(letter=Tiles('A', 1), cell = board.grid[11][13]) ,
        ]
        value = calculate_word_value(word)
        self.assertEqual(value, 7)

    def test_with_word_multiplier(self):
        board = Board()
        board.positions()
        word = [
            Cell(letter = Tiles('C', 1), cell = board.grid[7][7]),
            Cell(letter=Tiles('A', 1), cell = board.grid[7][7]),
            Cell(letter=Tiles('S', 2), cell = board.grid[7][7]),
            Cell(letter=Tiles('A', 1), cell = board.grid[11][13]) ,
        ]
        value = calculate_word_value(word)
        self.assertEqual(value, 10)

    def test_with_letter_word_multiplier(self):
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
                multiplier_type='word',
            ),
            Cell(letter=Tiles('A', 1)),
        ]
        value = calculate_word_value(word)
        self.assertEqual(value, 14)

    def test_with_letter_word_multiplier_no_active(self):
        # QUE HACEMOS CON EL ACTIVE ????
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
                multiplier_type='word',
            ),
            Cell(letter=Tiles('A', 1)),
        ]
        value = calculate_word_value(word)
        self.assertEqual(value, 5)

if __name__ == '__main__':
    unittest.main()