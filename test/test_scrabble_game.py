import unittest
from game.models import Tiles, BagTiles, Player, Cell
from game.board import Board
from game.scrabble_game import ScrabbleGame
from unittest.mock import patch

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
        scrabble_game.current_player = scrabble_game.players[0]
        scrabble_game.next_turn()
        assert scrabble_game.current_player == scrabble_game.players[1]

    def test_next_turn_player_is_last(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.next_turn()
        assert scrabble_game.current_player == scrabble_game.players[0]
    
    def test_word_validation_only_tiles_user_and_board(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.bag_tiles = (Tiles("A", 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        word = "HOLA"
        location = (5, 4)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, True)

    def test_word_validation_not_tiles_(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.bag_tiles = (Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        board = Board()
        word = "HOLA"
        location = (5, 4)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, False)

    def test_word_validation_out_of_range(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.bag_tiles = (Tiles('A', 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        word = "HOLA"
        location = (14, 4)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, False)

    def test_word_validation_out_of_range(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.bag_tiles = (Tiles('A', 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        word = "HOLA"
        location = (14, 4)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, False)
    
    def test_get_word_dictionary(self):
        scrabble_game = ScrabbleGame(players_count=3)
        word = "Noche"
        valor = scrabble_game.get_word(word)
        assert valor == True 

    def test_get_word_dictionary_not(self):
        scrabble_game = ScrabbleGame(players_count=3)
        word = "oicnowebcouwb"
        valor = scrabble_game.get_word(word)
        assert valor == False

    def test_validate_everything(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.bag_tiles = (Tiles('A', 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        word = "HOLA"
        location = (0, 0)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, True)
    
    def test_put_simple_word_h(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        word = "Banana"
        location = (0,0)
        orientation = "H"
        scrabble_game.put_word(word, location, orientation)
        self.assertEqual(scrabble_game.board.grid[0][0].letter, "B")
        self.assertEqual(scrabble_game.board.grid[0][1].letter, "a")
        self.assertEqual(scrabble_game.board.grid[0][2].letter, "n")
        self.assertEqual(scrabble_game.board.grid[0][3].letter, "a")
        self.assertEqual(scrabble_game.board.grid[0][4].letter, "n")
        self.assertEqual(scrabble_game.board.grid[0][5].letter, "a")

    def test_put_simple_word_v(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        word = "zapato"
        location = (4,5)
        orientation = "V"
        scrabble_game.put_word(word, location, orientation)
        self.assertEqual(scrabble_game.board.grid[4][5].letter, "z")
        self.assertEqual(scrabble_game.board.grid[5][5].letter, "a")
        self.assertEqual(scrabble_game.board.grid[6][5].letter, "p")
        self.assertEqual(scrabble_game.board.grid[7][5].letter, "a")
        self.assertEqual(scrabble_game.board.grid[8][5].letter, "t")
        self.assertEqual(scrabble_game.board.grid[9][5].letter, "o")

class TestCalculateWordValue(unittest.TestCase):
    def test_simple(self):
        scrabble_game = ScrabbleGame(players_count=3)
        word = "casa"
        orientation = "V"
        location = (0,0)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 12)

    def test_with_letter_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        word = [
            Cell(letter = Tiles('C', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('S', 2), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[9][1].multiplier,  multiplier_type = board.grid[9][1].multiplier_type) ,
        ]
        value = scrabble_game.calculate_word_value(word)
        self.assertEqual(value, 7)

    def test_with_word_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        word = [
            Cell(letter = Tiles('C', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('S', 2), multiplier = board.grid[7][7].multiplier, multiplier_type = board.grid[7][7].multiplier_type),
            Cell(letter = Tiles('A', 1), multiplier = board.grid[11][3].multiplier, multiplier_type = board.grid[11][3].multiplier_type) ,
        ]
        value = scrabble_game.calculate_word_value(word)
        self.assertEqual(value, 10)

    def test_with_letter_word_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        word = [
            Cell(multiplier = board.grid[5][1].multiplier, multiplier_type = board.grid[5][1].multiplier_type, letter = Tiles('C', 1)),
            Cell(letter = Tiles('A', 1)),
            Cell(letter = Tiles('S', 2), multiplier = board.grid[3][3].multiplier, multiplier_type = board.grid[3][3].multiplier_type),
            Cell(letter = Tiles('A', 1)),
        ]
        value = scrabble_game.calculate_word_value(word)
        self.assertEqual(value, 14)

    def test_with_letter_word_multiplier_no_active(self):
        scrabble_game = ScrabbleGame(players_count=3)
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
        value = scrabble_game.calculate_word_value(word)
        self.assertEqual(value, 7)

board = Board()
board.positions()
board.print_board()
if __name__ == '__main__':
    unittest.main()