import unittest
from game.models import Tiles, BagTiles, Player, Cell
from game.scrabble_game import ScrabbleGame
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
    
    def test_change_tiles(self):
        bag_tiles_player = BagTiles()
        bag_tiles = BagTiles()
        bag_tiles.tiles = [Tiles('A', 1), Tiles('B', 1), Tiles('C', 1), Tiles('D', 1),]
        player = Player(7 , bag_tiles_player)
        player.bag_tiles.tiles = [Tiles('A', 1), Tiles('B', 1), Tiles('C', 1), Tiles('D', 1),]
        player.change_tiles([1 , 2])
        self.assertEqual(len(bag_tiles.tiles), 4)
        self.assertEqual(len(player.bag_tiles.tiles), 4)

class TestPlayer(unittest.TestCase):
    def test_init(self):
        bag_tiles = BagTiles()
        player_1 = Player(1, bag_tiles)
        self.assertEqual(len(player_1.tiles),7,)

    def test_point_exists(self):
            bag_tiles = BagTiles()
            player_1 = Player(1, bag_tiles)
            player_1.points = 18
            self.assertEqual(player_1.points,18,)
    
    def test_point_from_calculation(self):
        scrabble_game = ScrabbleGame(players_count = 3)
        bag_tiles = BagTiles()
        scrabble_game.current_player = Player(1, bag_tiles)
        scrabble_game.current_player.tiles = [Tiles("C", 1), Tiles("A", 1), Tiles("S", 2), Tiles("A", 1)]
        scrabble_game.put_word("CASA", (7,7), "V")
        scrabble_game.calculate_word_value("CASA", (7,7), "V")
        self.assertEqual(scrabble_game.current_player.points, 5,)
    
    def test_validate_user_has_letters(self):
        bag_tile = BagTiles()
        bag_tile.tiles = [
            Tiles(letter='H', value=1),
            Tiles(letter='O', value=1),
            Tiles(letter='L', value=1),
            Tiles(letter='A', value=1),
            Tiles(letter='C', value=1),
            Tiles(letter='U', value=1),
            Tiles(letter='M', value=1),
        ]
        player = Player(4, bag_tile)
        is_valid = player.player_tiles("HOLA")

        self.assertEqual(is_valid, True)

    def test_validate_fail_when_user_has_not_letters(self):
        bag_tiles = BagTiles()
        bag_tiles.tiles = [
            Tiles(letter='P', value=1),
            Tiles(letter='O', value=1),
            Tiles(letter='L', value=1),
            Tiles(letter='A', value=1),
            Tiles(letter='C', value=1),
            Tiles(letter='U', value=1),
            Tiles(letter='M', value=1),
        ]
        player = Player(7 , bag_tiles)
        is_valid = player.player_tiles("MAYONESA")

        self.assertEqual(is_valid, False)

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



if __name__ == '__main__':
    unittest.main()