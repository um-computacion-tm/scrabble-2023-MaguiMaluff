import unittest
from game.models import Tiles, BagTiles, Player, Cell
from game.board import Board
from game.scrabble_game import ScrabbleGame, WordDoesntExists, DictionaryConnectionError, OutOfRange, InvalidWord, OutOfTiles, NotInTheMiddle, WrongCross
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
        with self.assertRaises(OutOfTiles):
            scrabble_game.validate_word(word, location, orientation)

    def test_word_validation_out_of_range(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = (Tiles("A", 1), Tiles("H", 2), Tiles("L", 3), Tiles("O", 4))
        word = "HOLA"
        location = (14, 4)
        orientation = "V"
        with self.assertRaises(OutOfRange):
            scrabble_game.validate_word(word, location, orientation)
    
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

    def test_put_word_crossing(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("Z", 1), Tiles("P", 3), Tiles("A", 4), Tiles("T", 3), Tiles("O", 4)] ###Falta una A
        word = "ZAPATO"
        location = (8,6)
        orientation = "H"
        scrabble_game.board.grid[7][7].letter = Tiles("C", 1)
        scrabble_game.board.grid[8][7].letter = Tiles("A", 1)
        scrabble_game.board.grid[9][7].letter = Tiles("N", 1)
        scrabble_game.validate_word_place_board(word, location, orientation)
        self.assertEqual(len(scrabble_game.current_player.tiles), 6)
        scrabble_game.put_word(word, location, orientation) 
        self.assertEqual(scrabble_game.board.grid[8][6].letter.letter, "Z")
        self.assertEqual(scrabble_game.board.grid[8][7].letter.letter, "A")
        self.assertEqual(scrabble_game.board.grid[8][8].letter.letter, "P")
        self.assertEqual(scrabble_game.board.grid[8][9].letter.letter, "A")
        self.assertEqual(scrabble_game.board.grid[8][10].letter.letter, "T")
        self.assertEqual(scrabble_game.board.grid[8][11].letter.letter, "O")


class TestCalculateWordValue(unittest.TestCase):
    def test_simple(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "V"
        location = (7,7)
        scrabble_game.put_word(word, location, orientation)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 5)

    def test_none_letter(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = ""
        orientation = "V"
        location = (7,7)
        scrabble_game.put_word(word, location, orientation)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 0)

    def test_with_letter_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "H"
        location = (8,7)
        scrabble_game.put_word(word, location, orientation)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 6)

    def test_with_word_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "H"
        location = (1,1)
        scrabble_game.put_word(word, location, orientation)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 10)

    def test_with_letter_word_multiplier(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        word = "CASA"
        orientation = "V"
        location = (0,0)
        scrabble_game.put_word(word, location, orientation)
        value = scrabble_game.calculate_word_value(word, location, orientation)
        self.assertEqual(value, 18)

    def test_with_letter_word_multiplier_2_word(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        scrabble_game.current_player.tiles = [Tiles("M", 2), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1), Tiles("Y", 4), Tiles("O", 1), Tiles("N", 1), Tiles("E", 1)]
        word = "MAYONESA"
        orientation = "V"
        location = (0,0)
        scrabble_game.put_word(word, location, orientation)
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
        scrabble_game.put_word(word, location, orientation)
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
        self.assertEqual(check, [['CASAS', (7,7), "V"]])

    def test_check_vertical_adding_right(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("ASA", (7,7), "H") 
        word = "MAS"
        location = (7, 6)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, [['MASA', (7,6), "H"]])

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
        self.assertEqual(check, [['MA', (8,6), "H" ], ['AS', (9,6), "H"]])

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
        self.assertEqual(check, [['AL', (7,7), "H"], ['SI', (8,7), "H"]])

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
        self.assertEqual(check, ["MAS", (8,6), "H"])
    
    def test_check_vertical_making_words_both_sides_fine(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[2]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1), Tiles("A", 1),  Tiles("A", 1), Tiles("N", 4)]
        scrabble_game.put_word("ASA", (7,7), "V")
        scrabble_game.put_word("ANA", (7,9), "V")
        word = "LI"
        location = (7,8)
        check = scrabble_game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, [['ALA', (7,7), "H"], ['SIN', (8,7), "H"], ])
    
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
        self.assertEqual(check, [['CINTAS', (7,7), "V"]])


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
        self.assertEqual(check, [['COSA', (6,7), "V"]])
    
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
        self.assertEqual(check, [['NO', (6,7), "V"], ['AL', (6,8), "V"]])
    
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
        self.assertEqual(check, [['MI', (7,7), "V"], ['AL', (7,8), "V"], ['LO', (7,9), "V"]])
    
    def test_check_horizontal_new_word_up_wrong(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[0]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("M", 1), Tiles("L", 1), Tiles("A", 1)]
        scrabble_game.put_word("MAL", (7,7), "H")
        word = "HOLA"
        location = (6,7)
        with self.assertRaises(WordDoesntExists):
            scrabble_game.horizontal_word_check_for_sum(word, location)

    def test_check_horizontal_no_words_horizontal(self):
        game = ScrabbleGame(3)
        game.current_player = game.players[0]
        players_tiles = game.current_player.tiles = [Tiles("M", 1), Tiles("L", 1), Tiles("A", 1)]
        word = "MAL"
        location = (7,7)
        check = game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, None)
    
    def test_check_horizontal_no_words_vertical(self):
        game = ScrabbleGame(3)
        game.current_player = game.players[0]
        players_tiles = game.current_player.tiles = [Tiles("M", 1), Tiles("L", 1), Tiles("A", 1)]
        word = "MAL"
        location = (7,7)
        check = game.vertical_word_check_for_sum(word, location)
        self.assertEqual(check, None)


    def test_check_horizontal_new_word_both_sides(self):
        scrabble_game = ScrabbleGame(players_count=3)
        scrabble_game.current_player = scrabble_game.players[0]
        players_tiles = scrabble_game.current_player.tiles = [Tiles("S", 1), Tiles("L", 1), Tiles("A", 1), Tiles("S", 1), Tiles("O", 1), Tiles("N", 1)]
        scrabble_game.put_word("LAS", (7,7), "H")
        scrabble_game.put_word("SON", (9,7), "H")
        word = "AMAN"
        location = (8,7)
        check = scrabble_game.horizontal_word_check_for_sum(word, location)
        self.assertEqual(check, [['LAS', (7,7), "V"], ['AMO', (7,8), "V"], ['SAN', (7,9), "V"]])
    
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
        self.assertEqual(check, ['MAL', (7,7), "V"])

    

class TestValidatePlaceBoard(unittest.TestCase):
    def test_place_word_empty_board_horizontal_fine(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        word = "FACULTAD"
        location = (7, 5)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_empty_board_horizontal_wrong(self):
        game = ScrabbleGame(2)
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        word = "Facultad"
        location = (2, 4)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_place_word_empty_board_vertical_fine(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        word = "FACULTAD"
        location = (5, 7)
        orientation = "V"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_empty_board_vertical_wrong(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        word = "FACULTAD"
        location = (2, 4)
        orientation = "V"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_place_word_not_empty_board_horizontal_fine(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[8][7].add_letter(Tiles('A', 1)) 
        game.board.grid[9][7].add_letter(Tiles('S', 1)) 
        game.board.grid[10][7].add_letter(Tiles('A', 1)) 
        word = "FACULTAD"
        location = (8, 6)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_not_empty_board_horizontal_wrong(self):
        game = ScrabbleGame(2)
        game.board.grid[5][7].add_letter(Tiles('S', 1)) 
        game.board.grid[6][7].add_letter(Tiles('A', 1))
        game.board.grid[7][7].add_letter(Tiles('L', 1))
        word = "FACULTAD"
        location = (1, 1)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_place_word_not_empty_board_vertical_fine(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[7][8].add_letter(Tiles('A', 1)) 
        game.board.grid[7][9].add_letter(Tiles('S', 1)) 
        game.board.grid[7][10].add_letter(Tiles('A', 1)) 
        word = "PAZ"
        location = (6, 8)
        orientation = "V"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_place_word_not_empty_board_vertical_wrong(self):
        game = ScrabbleGame(2)
        game.board.grid[7][5].add_letter(Tiles('S', 1)) 
        game.board.grid[7][6].add_letter(Tiles('A', 1))
        game.board.grid[7][7].add_letter(Tiles('L', 1))
        word = "PAZ"
        location = (9, 6)
        orientation = "V"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False
    
    def test_validate_word_place_board_add_letter_to_existing_word_fine_v(self):
        game = ScrabbleGame(2)
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[7][8].add_letter(Tiles('A', 1)) 
        game.board.grid[7][9].add_letter(Tiles('S', 1)) 
        game.board.grid[7][10].add_letter(Tiles('A', 1)) 
        word = "MAS"
        location = (5, 11)
        orientation = "V"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_validate_word_place_board_add_letter_to_existing_word_wrong_v(self):
        game = ScrabbleGame(2)
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[7][8].add_letter(Tiles('A', 1)) 
        game.board.grid[7][9].add_letter(Tiles('S', 1)) 
        game.board.grid[7][10].add_letter(Tiles('A', 1)) 
        word = "MA"
        location = (5, 11)
        orientation = "V"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False
    
    def test_validate_word_place_board_add_letter_to_existing_word_fine_h(self):
        game = ScrabbleGame(2)
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[8][7].add_letter(Tiles('A', 1)) 
        game.board.grid[9][7].add_letter(Tiles('S', 1)) 
        game.board.grid[10][7].add_letter(Tiles('A', 1)) 
        word = "MAS"
        location = (11, 5)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True

    def test_validate_word_doesnt_exist(self):
        game = ScrabbleGame(2)
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[8][7].add_letter(Tiles('A', 1)) 
        game.board.grid[9][7].add_letter(Tiles('S', 1)) 
        game.board.grid[10][7].add_letter(Tiles('A', 1)) 
        word = "MAS"
        location = (11, 5)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == True
    
    def test_validate_word_place_board_add_letter_to_existing_word_wrong_h(self):
        game = ScrabbleGame(2)
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[8][7].add_letter(Tiles('A', 1)) 
        game.board.grid[9][7].add_letter(Tiles('S', 1)) 
        game.board.grid[10][7].add_letter(Tiles('A', 1)) 
        word = "MA"
        location = (11, 5)
        orientation = "H"
        word_is_valid = game.validate_word_place_board(word, location, orientation)
        assert word_is_valid == False

    def test_validate_word_place_board_raises(self):
        game = ScrabbleGame(2)
        word = "MA"
        location = (11, 5)
        orientation = "H"
        with self.assertRaises(NotInTheMiddle):
            game.validate_word_place_board(word, location, orientation)

class ForMain(unittest.TestCase):
    def test_validate_word_place_board_add_tile(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[8][7].add_letter(Tiles('A', 1)) 
        game.board.grid[9][7].add_letter(Tiles('S', 1)) 
        game.board.grid[10][7].add_letter(Tiles('A', 1)) 
        game.current_player.tiles = [Tiles("M", 2), Tiles("A", 2)]
        word = "MAS"
        location = (9, 5)
        orientation = "H"
        game.validate_word_place_board(word, location, orientation)
        self.assertEqual(len(game.current_player.tiles), 3)
        self.assertEqual(game.current_player.tiles[2].letter, "S")

    def test_validate_word_place_board_raises(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('C', 1))
        game.board.grid[8][7].add_letter(Tiles('A', 1)) 
        game.board.grid[9][7].add_letter(Tiles('S', 1)) 
        game.board.grid[10][7].add_letter(Tiles('A', 1)) 
        game.current_player.tiles = [Tiles("M", 2), Tiles("A", 2)]
        word = "MAS"
        location = (9, 6)
        orientation = "H"
        with self.assertRaises(WrongCross):
            game.validate_word_place_board(word, location, orientation)

    def test_validate_word_place_board_add_tile(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.current_player.tiles = [Tiles('C', 1),(Tiles('A', 1)),(Tiles('S', 1)),(Tiles('A', 1))]
        word = "CS"
        location = (7 , 7)
        orientation = "H"
        with self.assertRaises(InvalidWord):
            game.validate_word(word, location, orientation)

    def test_player_tiles_list(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.current_player.tiles = [Tiles('C', 1),(Tiles('A', 1)),(Tiles('S', 1)),(Tiles('A', 1))]
        lista = game.player_tiles_list()
        self.assertEqual(lista, ["C", "A", "S", "A"])

    def test_player_tiles_value(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.current_player.tiles = [Tiles('C', 1),(Tiles('A', 1)),(Tiles('S', 1)),(Tiles('A', 1))]
        lista = game.player_tiles_values()
        self.assertEqual(lista, [1,1,1,1])

    def test_validate_word_place_board_add_tile(self):
        game = ScrabbleGame(2)
        game.next_turn()
        game.board.grid[7][7].add_letter(Tiles('A', 1))
        game.board.grid[7][8].add_letter(Tiles('N', 1)) 
        game.board.grid[7][9].add_letter(Tiles('O', 1)) 
        game.current_player.tiles = [Tiles("N", 2)]
        word = "NANO"
        location = (7, 6)
        orientation = "H"
        game.validate_word_place_board(word, location, orientation)
        self.assertEqual(len(game.current_player.tiles), 4)
        self.assertEqual(game.current_player.tiles[1].letter, "A")
        self.assertEqual(game.current_player.tiles[2].letter, "N")
    
    def test_playin(self):
        game = ScrabbleGame(2)
        check = game.is_playing()
        self.assertEqual(check, True)



if __name__ == '__main__':
    unittest.main()