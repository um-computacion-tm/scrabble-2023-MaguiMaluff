# Scrabble

- Objective:

The main objective of Scrabble is to score the most points at the end of the game by forming words on the board.

- Gameplay:

Each player chooses seven tiles at random. Up to four players can play.

On each turn, a player must form a word on the board.

Words are formed by placing tiles on the board horizontally or vertically, connecting them to other tiles.

Multiple words can be formed in a single turn, as long as all words are valid.

At the end of the turn, the player receives new tiles, enough to reach 7.

- Scoring:

Each letter has a point value, and the squares on the board can multiply the point value of the letter or word.

The point value of a word is calculated by adding the point values of the letters and the board multipliers.

If the new word only crosses an existing word, only the new word is scored.

If the new word adds letters to an existing word, it counts towards the point value of the new word and is added to the point value of the existing word (only the sum of the point values of its letters, the multipliers are not taken again).

If the new word creates words with the existing ones, the new word and the ones created with it are counted.

- End of the Game:

The game continues until all the tiles have been used, until the players decide that they cannot form any more valid words, or when all the players have passed twice.

The player with the highest point value at the end of the game wins.

- Explanations:

"Only crosses an existing word" means that the new word only touches the existing word at one point.
"Adds letters to an existing word" means that the new word touches the existing word at two or more points.
"Creates words with the existing ones" means that the new word creates two or more new words by connecting to existing words.

- How to run on Docker:

To play you need to have Docker installed, and the dockerfile.
Once you have that, you need to build an image on docker using: docker build -t my_game .
To play run: docker run -it my_game
my_game is the name of the image, you can use another one.


# Author
Maria Magdalena Maluff Stabio 
Legajo: 62234

# Develop
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/um-computacion-tm/scrabble-2023-MaguiMaluff/tree/develop.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/um-computacion-tm/scrabble-2023-MaguiMaluff/tree/develop)

# Maintainability
[![Maintainability](https://api.codeclimate.com/v1/badges/d817cbf68e0470322a0d/maintainability)](https://codeclimate.com/github/um-computacion-tm/scrabble-2023-MaguiMaluff/maintainability)

# Test Coverage
[![Test Coverage](https://api.codeclimate.com/v1/badges/d817cbf68e0470322a0d/test_coverage)](https://codeclimate.com/github/um-computacion-tm/scrabble-2023-MaguiMaluff/test_coverage)


