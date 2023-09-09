import unittest
from game.models import Tiles, BagTiles, Player, Board, Cell
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
        bag_tiles = BagTiles()
        player_1 = Player(1, bag_tiles)
        self.assertEqual(len(player_1.tiles),7,)

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

    def test_word_inside_board(self):
        board = Board()
        word = "Facultad"
        location = (5, 4)
        orientation = "H"
        word_is_valid = board.validate_word_inside_board(word, location, orientation)
        assert word_is_valid == True
        
    def test_word_out_of_board(self):
        board = Board()
        word = "Facultad"
        location = (14, 4)
        orientation = "H"
        word_is_valid = board.validate_word_inside_board(word, location, orientation)
        
        assert word_is_valid == False


class TestScrabbleGame(unittest.TestCase):
    def test_init(self):
        scrabble_game = ScrabbleGame(players_count=3)
        self.assertIsNotNone(scrabble_game.board)
        self.assertEqual(
            len(scrabble_game.players),
            3,
        )
        self.assertIsNotNone(scrabble_game.bag_tiles)

    def test_next_turn_when_game_is_starting(self):
        scrabble_game = ScrabbleGame(players_count = 3)
        scrabble_game.next_turn()
        assert scrabble_game.current_player == scrabble_game.players[0]

    def test_next_turn_when_player_is_not_the_first(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player == scrabble_game.players[0]
        print(scrabble_game.current_player)
        scrabble_game.next_turn()
        assert scrabble_game.current_player == scrabble_game.players[1]

    def test_next_turn_player_is_last(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player == scrabble_game.players[2]
        scrabble_game.next_turn()
        assert scrabble_game.current_player == scrabble_game.players[0]


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