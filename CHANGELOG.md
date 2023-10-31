Changelog

All notable changes to this project will be documented in this file.

2023-30-10

### Fixed 

- change_tiles in Player

### Added

- Game's rules to readme.md

### Change

- Deleted RR, CH and LL from tiles, added 2 L, 2 R, 1 C, 1 H

2023-25-10

### Change

- horizontal_word_check_for_sum, vertical_word_check_for_sum, if the list is empty it returns None.

- add_word, added the calculation of points

- get_player_info

- change_tile

- validate_word_place_board

### Added

- change_player_tiles

2023-23-10

### Fixed

- horizontal_word_check_for_sum, vertical_word_check_for_sum. There was an error when the word was crossing another, fixed it.

### Change

- validate_word_place_board is now in ScrabbleGame. This fixes the problem where a word crosses another word, and there's a letter that's already on the board, so the player shouldn't have that letter.

2023-22-10

### Added

- File back.py, and moved get_word_main, get_location, get_orientation and get_task

- test_back.py

### Change

- add_word
- main
- board, print_board

2023-20-10

- Tried to fix add_word


2023-18-10

### Added

- File test_scrabble_game_for_main
- Exceptions to validate_word
- Added take_to_7, player_tiles_list, printbb, get_player_info

### Fixed

- Fixed calculated_word_value and tests
- add_word, get_word_main, get_orientation

2023-14-10

### Added

- To scrabble_game, functions, get_word_main, get_location, get_orientation, add_word and get_task

### Change

- scrabble_main

- calculate_word_value

2023-12-10

### Change

- horizontal_word_check_for_sum, vertical_word_check_for_sum
- get_horizontal_word, get_vertical_word

2023-10-10

### Change

- function print_board

2023-06-11

### Added

- horizontal_word_check_for_sum
- Test for horizontal_word_check_for_sum

### Deleted

- playing from scrabble_game


2023-05-10

### Change

- get_horizontal_word

- vertical_word_check_for_sum, almost done


2023-04-10

### Change

- get_word, now it doesnt show on the terminal

- vertical_word_check_for_sum_1 to vertical_word_check_for_sum

- vertical_word_check_for_sum now works. But not done yet


2023-02-10

### Change 

- Function get_word, now if theres an error it returns an exception

### Deleted

- case_of_sum

### Added

- vertical_word_check_for_sum_1, not done yet

- get_horizontal_word

- get_word_from_cell

2023-29-09

### Fixed

- Function list_of_words

### Change

- Tried to make function case_of_sum, still can't
- list_of_words

2023-28-09

### Added

- Function change_tiles to class Player and a test for it
- Function playing

### Change

- Change name main.py to scrabble.main.py
- Added some things to scrabble_main.py

2023-27-09

### Change

- Function player_tiles moved to file models

2023-26-09

### Soon to be delete

- validate_word_when_not_empty

### Added

- case_1_sum, not done yet



2023-25-09

### Added

- Function calculate_word_without_any_multiplier

- Dictionary cell_values to ScrabbleGame


2023-21-09

### Fixed 

- validate word_when not_empty (I don't like it, will probably change it again)

2023-19-09


### Change 

- Player Class now has a point counter.

- Function calculate_word_value now assigns points to the player

- Function validate_word uses other functions

- Realized validate_word_when_not_empty was wrong and tried to fixed it

### Added

- Test for the changes

- player_tiles to Class ScrabbleGame, it validates if a player has the same tiles as the word they put.

2023-17-09

### Added

- Function words_on_board and tests

- validate_word_when_not_empty, now the game can validate if when adding a word, the word is adding letters to an existing word.

2023-15-09

### Fixed

- Function validate_word_place_board now works

### Changed

- Shorten the function validate_word_place_board

2023-13-09

### Added

- Function is_empty to Board.

- Function validate_word_place_board to Board

2023-12-09

### Change

- Function calculate_word_value is now in scrabble_game

- Test for caculated_word_value now in test_scrabble_game

- calculate_word_value now calculates the word value from a string instead of a list

- put_word now the letter in the board is a Tile instead of a string like before

- Tests for calculated_word_value and put_word

2023-11-09

### Added

- Files test_board and board

- put_word on scrabble_game

- get_tile_from_player

- Test for get_tile

### Delete 

- Class Board from models

- Class TestBoard from test_models

### Fixed

- validate_word on scrabble_game, fixed validation method and added the validation of the word in the dictonary

2023-10-09

### Added

- Validate word on Scrabble Game. And tests

- File test_scrabble_game.

- pyrae, and function get_word, now the game can validate if the word is in the RAE dictionary

### Delete

- Class TestScrabbleGame from test_models, moved to test_scrabble_game

2023-09-08

### Added

- Print function to Board

### Fixed

- Scrabble Game Next Turn. Now it works.

### Deleted

- Calculate word value file, and function on its own. Added to cell Board.

2023-09-07

### Added

- Next_turn to class ScrabbleGame.

- Tests for the mentioned addition.

- Validate_word_inside_board to class Board. Now the game is able to determine if a word would fit on the board.

### Change

-Main

2023-09-01

### Change

- README.md, added CircleCi and CodeClimate badges

### Fixed

- Calculate_word_value and tests


2023-08-29

### Added

- Set letter multipliers positions on Board and tests

2023-08-28

### Added

- Tried to calculate word value, needs to be fixed

2023-08-24

### Added

- env

- Branch develop

- .circleci and config.yml

- requirements.txt

- Set word multipliers positions on Board and tests

### Fixed
- config.yml file

- Error in multipliers positions

2023-08-23 

### Added

- Class Board(grid), Player(tiles), Cell(add_letter, calculate_value)

- Init test classes

- File scrabble_game, with class ScrabbleGame. Tests for ScrabbleGame

2023-08-21

### Added

- Changlog file

- .coveragerc

### Fixed

- TestTiles, TestBagTiles(test_put and test_take)

### Change

- Clase Tiles, added missing tiles


2023-08-16

### Added

- Clase Tiles, BagTiles

- Tests, TestTiles, TestBagTiles, test_put, test_take


