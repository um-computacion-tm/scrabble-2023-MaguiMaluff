#!/usr/bin/env python3.10
from game.scrabble_game import ScrabbleGame
from back import Back


def main():
    while True:
            try:
                players_count = input('Number of players:')
                if not players_count.isnumeric():
                     raise ValueError
                players_count = int(players_count)
                if players_count < 1 or players_count > 4:
                    raise ValueError
                break
            except ValueError:
                print("Invalid value")
    game = ScrabbleGame(players_count)
    back = Back()
    while(game.is_playing()):
        game.next_turn()
        game.printbb()
        game.get_player_info()
        task = back.get_task()
        if task == "A":
                try:
                    word = back.get_word_main()
                    location = back.get_location()
                    orientation = back.get_orientation()
                    game.check_white()
                    game.add_word(word, location, orientation)
                except Exception as e:
                    print(e)
        elif task == "C":
            game.change_tiles_player()
        elif task == "P":
            pass
        elif task == 'E':
            pass

            

if __name__ == '__main__':
    main()
