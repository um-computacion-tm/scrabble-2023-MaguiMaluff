import unittest
from game.models import Player, BagTiles, Cell, Tiles
from game.board import Board

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

    def test_board_is_empty(self):
        board = Board()
        board.positions()
        assert board.is_empty() == True

    def test_board_is_not_empty(self):
        board = Board()
        board.grid[7][7].add_letter(Tiles('C', 1))
        assert board.is_empty() == False
        
    def test_place_word_empty_board_horizontal_fine(self):
        board = Board()
        word = "Facultad"
        location = (7, 4)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_empty_board_horizontal_wrong(self):
        board = Board()
        word = "Facultad"
        location = (2, 4)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_place_word_empty_board_vertical_fine(self):
        board = Board()
        word = "Facultad"
        location = (4, 7)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_empty_board_vertical_wrong(self):
        board = Board()
        word = "Facultad"
        location = (2, 4)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_place_word_not_empty_board_horizontal_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tiles('C', 1))
        board.grid[8][7].add_letter(Tiles('A', 1)) 
        board.grid[9][7].add_letter(Tiles('S', 1)) 
        board.grid[10][7].add_letter(Tiles('A', 1)) 
        word = "FACULTAD"
        location = (8, 6)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_not_empty_board_horizontal_wrong(self):
        board = Board()
        board.grid[5][7].add_letter(Tiles('S', 1)) 
        board.grid[6][7].add_letter(Tiles('A', 1))
        board.grid[7][7].add_letter(Tiles('L', 1))
        word = "FACULTAD"
        location = (8, 6)
        orientation = "H"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_place_word_not_empty_board_vertical_fine(self):
        board = Board()
        board.grid[7][7].add_letter(Tiles('C', 1))
        board.grid[8][7].add_letter(Tiles('A', 1)) 
        board.grid[9][7].add_letter(Tiles('S', 1)) 
        board.grid[10][7].add_letter(Tiles('A', 1)) 
        word = "PAZ"
        location = (8, 6)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_not_empty_board_vertical_wrong(self):
        board = Board()
        board.grid[5][7].add_letter(Tiles('S', 1)) 
        board.grid[6][7].add_letter(Tiles('A', 1))
        board.grid[7][7].add_letter(Tiles('L', 1))
        word = "PAZ"
        location = (8, 6)
        orientation = "V"
        word_is_valid = board.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False


if __name__ == '__main__':
    unittest.main()