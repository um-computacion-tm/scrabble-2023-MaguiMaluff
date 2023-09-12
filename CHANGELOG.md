Changelog

All notable changes to this project will be documented in this file.

2023-12-09

### Change

- Function calculate_word_value is now in scrabble_game

- Tried to make calculate_word_value calculate the word from a string insted of a list

- Test for caculated_word_value now in test_scrabble_game

2023-11-09

### Added

- Files test_board and board

- put_word on scrabble_game

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


