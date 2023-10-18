#!/usr/bin/env python3.10
from game.scrabble_game import ScrabbleGame


def main():
    while True:
            try:
                players_count = int(input('Cantidad de jugadores:'))
                if players_count < 1 or players_count > 4:
                    raise ValueError
                break
            except ValueError:
                print("Valor Invalido")
    game = ScrabbleGame(players_count)
    while(game.is_playing()):
        task = game.get_task()
        if task == "A":
            try:
                word = game.get_word()
                location = game.get_location()
                orientation = game.get_orientation()
                game.add_word(word, location, orientation)
            except Exception as e:
                print(e)
        elif task == "C":
            pass
        elif task == "P":
            game.next_turn()

if __name__ == '__main__':
    main()

    """

    El jugador puede:
    1- Agregar palabras
    2- Cambiar fichas
    3- Pasar de turno

    Despues de agregar la palabra
    1- Verifico que el board o este vacio o la palabara pase por (7, 7)
    2- Verifico que la palabra no este en el tablero
    3- Verifico el lugar en el board, que no este fuera de rango
    4- Verifico que el jugador tenga los Tiles
    5- Verifico que la palabra cruce o anada letras a otra palabra
    6- Verifico que la palabra/palabras existan
    7- Calculo el valor 
    8- Agrego la palabra al board y a la lista de palabras
    9- Cambio de turno 
    """