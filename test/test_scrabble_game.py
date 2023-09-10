import unittest
from game.models import Tiles, BagTiles, Player, Board, Cell
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

if __name__ == '__main__':
    unittest.main()