import unittest
from game.models import Tiles, BagTiles, Player, Cell
from game.board import Board
from game.scrabble_game import ScrabbleGame, WordDoesntExists, DictionaryConnectionError
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
        scrabble_game.current_player.tiles = (Tiles("A", 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4), Tiles("White", 0), Tiles("N", 9))
        word = "HOLA"
        location = (5, 4)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, True)

    def test_word_validation_not_tiles_(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = (Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
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
        scrabble_game.current_player.tiles = (Tiles('A', 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        word = "HOLA"
        location = (0, 0)
        orientation = "H"
        validation = scrabble_game.validate_word(word, location, orientation)
        self.assertEqual(validation, True)
    
    def test_put_simple_word_h(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("B", 1), Tiles("A", 2), Tiles("N", 3), Tiles("A", 4), Tiles("N", 3), Tiles("A", 4)]
        word = "BANANA"
        location = (0,0)
        orientation = "H"
        scrabble_game.put_word(word, location, orientation)
        self.assertEqual(scrabble_game.board.grid[0][0].letter.letter, "B")
        self.assertEqual(scrabble_game.board.grid[0][1].letter.letter, "A")
        self.assertEqual(scrabble_game.board.grid[0][2].letter.letter, "N")
        self.assertEqual(scrabble_game.board.grid[0][3].letter.letter, "A")
        self.assertEqual(scrabble_game.board.grid[0][4].letter.letter, "N")
        self.assertEqual(scrabble_game.board.grid[0][5].letter.letter, "A")

    def test_put_simple_word_v(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("Z", 1), Tiles("A", 2), Tiles("P", 3), Tiles("A", 4), Tiles("T", 3), Tiles("O", 4)]
        word = "ZAPATO"
        location = (4,5)
        orientation = "V"
        scrabble_game.put_word(word, location, orientation)
        self.assertEqual(scrabble_game.board.grid[4][5].letter.letter, "Z")
        self.assertEqual(scrabble_game.board.grid[5][5].letter.letter, "A")
        self.assertEqual(scrabble_game.board.grid[6][5].letter.letter, "P")
        self.assertEqual(scrabble_game.board.grid[7][5].letter.letter, "A")
        self.assertEqual(scrabble_game.board.grid[8][5].letter.letter, "T")
        self.assertEqual(scrabble_game.board.grid[9][5].letter.letter, "O")

class TestCalculateWordValue(unittest.TestCase):
    def test_simple(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "V"
        location = (7,7)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 5)

    def test_none_letter(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = ""
        orientation = "V"
        location = (7,7)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 0)

    def test_with_letter_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "H"
        location = (8,7)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 6)

    def test_with_word_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "H"
        location = (1,1)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 10)

    def test_with_letter_word_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "V"
        location = (0,0)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 18)

    def test_with_letter_word_multiplier_2_word(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("M", 2), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1), Tiles("Y", 4), Tiles("O", 1), Tiles("N", 1), Tiles("E", 1)]
        word = "MAYONESA"
        orientation = "V"
        location = (0,0)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 126)

    def test_with_letter_word_multiplier_no_active(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "V"
        location = (8,7)
        scrabble_game.board.grid[11][7].state = False
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 5)
    
    def test_get_tile(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        tile = scrabble_game.get_tile_from_player(players_tiles, "A")
        self.assertEqual(tile, scrabble_game.current_player.tiles[1])
    
    def test_get_tile_not_in_tiles(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        tile = scrabble_game.get_tile_from_player(players_tiles, "W")
        self.assertNotEqual(tile, scrabble_game.current_player.tiles[1])


    def test_cells_values_vertical(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("H", 4), Tiles("O", 1), Tiles("L", 2), Tiles("A", 1)]
        scrabble_game.put_word("HOLA", (0,0), 'V')
        scrabble_game.calculate_word_without_any_multiplier("HOLA", (0,0), 'V')
        self.assertEqual(scrabble_game.cells_values,
                        {
                            ( 0, 0) : 8,
                            ( 1, 0) : 8,
                            ( 2, 0) : 8,
                            ( 3, 0) : 8,
                        }
                         )
        
    def test_cells_values_horizontal(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("H", 4), Tiles("O", 1), Tiles("L", 2), Tiles("A", 1)]
        scrabble_game.put_word("HOLA", (0,0), 'H')
        scrabble_game.calculate_word_without_any_multiplier("HOLA", (0,0), 'H')
        self.assertEqual(scrabble_game.cells_values,
                        {
                            (0 , 0) : 8,
                            (0 , 1) : 8,
                            (0 , 2) : 8,
                            (0 , 3) : 8,
                        }
                         )


class TestWordValidationMultipleWords(unittest.TestCase):

### test de chech vertical

    def test_check_vertical_adding_left(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("CASA", (7,7), "H")
        word = "OLAS"
        location = (4, 11)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, ['CASAS'])

    def test_check_vertical_adding_right(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("ASA", (7,7), "H") 
        word = "MAS"
        location = (7, 6)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, ['MASA'])

    def test_check_vertical_adding_right_new_word_doesnt_exist(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("ASA", (7,7), "H") 
        word = "AS"
        location = (7, 10)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.vertical_word_check_for_sum(word, location)

    def test_check_vertical_adding_right_new_word_doesnt_exist(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("ASA", (7,7), "H") 
        word = "AS"
        location = (7, 6)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.vertical_word_check_for_sum(word, location)

    def test_check_vertical_making_words_right_works(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("CASA", (7,7), "V")
        word = "MA"
        location = (8,6)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, ['MA', 'AS'])

    def test_check_vertical_making_words_right_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("CASA", (7,7), "V")
        word = "KK"
        location = (8,6)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.vertical_word_check_for_sum(word, location)

    def test_check_vertical_making_words_left_works(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("ASA", (7,7), "V")
        word = "LI"
        location = (7,8)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, ['AL', 'SI'])

    def test_check_vertical_making_words_left_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("CASA", (7,7), "V")
        word = "KA"
        location = (8,8)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.vertical_word_check_for_sum(word, location)

    def test_get_horizontal_word(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("AS", (7,8), "V")
        scrabble_game.put_word("CA", (7,7), "V")
        check = scrabble_game.get_horizontal_word((8,6), "M",)
        
        self.assertEqual(check, "MAS")
    
    def test_check_vertical_making_words_both_sides_fine(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1), Tiles("A", 1),  Tiles("A", 1), Tiles("N", 4)]
        scrabble_game.put_word("ASA", (7,7), "V")
        scrabble_game.put_word("ANA", (7,9), "V")
        word = "LI"
        location = (7,8)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, ['ALA', 'SIN', ])
    
    def test_check_vertical_making_words_both_sides_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1), Tiles("A", 1),  Tiles("A", 1), Tiles("N", 4)]
        scrabble_game.put_word("ASA", (7,7), "V")
        scrabble_game.put_word("ANA", (7,9), "V")
        word = "LK"
        location = (7,8)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.vertical_word_check_for_sum(word, location)

### Test de check horizontal

    def test_check_horizontal_adding_to_word_up_fine(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("I", 1), Tiles("N", 2), Tiles("T", 1), Tiles("A", 1)]
        scrabble_game.put_word("CINTA", (7,7), "V")
        word = "OSOS"
        location = (12,4)
        check = scrabble_game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, ['CINTAS'])


    def test_check_horizontal_adding_to_word_up_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("I", 1), Tiles("N", 2), Tiles("T", 1), Tiles("A", 1)]
        scrabble_game.put_word("CINTA", (7,7), "V")
        word = "CANA"
        location = (12,4)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.horizontal_word_check_for_sum(word, location)

    def test_check_horizontal_adding_to_word_down_fine(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("O", 1), Tiles("S", 1), Tiles("N", 2), Tiles("T", 1), Tiles("A", 1)]
        scrabble_game.put_word("OSA", (7,7), "V")
        word = "CAN"
        location = (6,7)
        check = scrabble_game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, ['COSA'])
    
    def test_check_horizontal_adding_to_word_down_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("O", 1), Tiles("S", 1), Tiles("N", 2), Tiles("T", 1), Tiles("A", 1)]
        scrabble_game.put_word("OSA", (7,7), "V")
        word = "KIWI"
        location = (6,7)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.horizontal_word_check_for_sum(word, location)

    def test_check_horizontal_new_word_down_fine(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("O", 1), Tiles("L", 1), Tiles("N", 2), Tiles("T", 1), Tiles("A", 1)]
        scrabble_game.put_word("OLA", (7,7), "H")
        word = "NA"
        location = (6,7)
        check = scrabble_game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, ['NO', 'AL'])
    
    def test_check_horizontal_new_word_down_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("O", 1), Tiles("L", 1), Tiles("A", 1)]
        scrabble_game.put_word("OLA", (7,7), "H")
        word = "KA"
        location = (6,7)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.horizontal_word_check_for_sum(word, location)
    
    def test_check_horizontal_new_word_up_fine(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[1]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("M", 1), Tiles("L", 1), Tiles("A", 1)]
        scrabble_game.put_word("MAL", (7,7), "H")
        word = "HILO"
        location = (8,6)
        check = scrabble_game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, ['MI', 'AL', 'LO'])
    
    def test_check_horizontal_new_word_up_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[0]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("M", 1), Tiles("L", 1), Tiles("A", 1)]
        scrabble_game.put_word("MAL", (7,7), "H")
        word = "HOLA"
        location = (6,7)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.horizontal_word_check_for_sum(word, location)


    def test_check_horizontal_new_word_both_sides(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[0]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("S", 1), Tiles("L", 1), Tiles("A", 1), Tiles("S", 1), Tiles("O", 1), Tiles("N", 1)]
        scrabble_game.put_word("LAS", (7,7), "H")
        scrabble_game.put_word("SON", (9,7), "H")
        word = "AMAN"
        location = (8,7)
        check = scrabble_game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, ['LAS', 'AMO', 'SAN'])
    
    def test_check_horizontal_new_word_both_sides_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[0]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("S", 1), Tiles("L", 1), Tiles("A", 1), Tiles("S", 1), Tiles("O", 1), Tiles("N", 1)]
        scrabble_game.put_word("LAS", (7,7), "H")
        scrabble_game.put_word("SON", (9,7), "H")
        word = "AMAN"
        location = (8,6)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.horizontal_word_check_for_sum(word, location)

    def test_get_vertical_word(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("S", 1), Tiles("A", 1), Tiles("L", 2), Tiles("M", 1)]
        scrabble_game.put_word("SAL", (9,5), "H")
        scrabble_game.put_word("M", (7,7), "H")
        check = scrabble_game.get_vertical_word((8,7), "A",)
        self.assertEqual(check, 'MAL')


if __name__ == '__main__':
    unittest.main()