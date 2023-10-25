from game.scrabble_game import ScrabbleGame, InvalidTask, IsNotNumber, OutOfRange, OutOfTiles

class Back:
    def get_task(self):
        while True:
            try:
                task = input("Para agregar palabra ingrese A, para cambiar letras ingrese C, para pasar de turno ingrese P")
                task = task.upper()
                if task not in ["A", "C", "P"]:
                    raise InvalidTask("Invalid Task")
                else:
                    return task
            except Exception as e:
                print(e)
    
    def get_word_main(self):
        while True:
            try:
                word = input("Ingrese Palabra:")
                word = word.upper()
                for i in word:
                    if not i.isalpha():
                        raise ValueError
                    else:
                        return word
            except ValueError:
                print("Palabra invalida")
    
    def get_location(self):
        while True:
            try:
                location_i = input("Ingrese X: ")
                location_j = input("Ingrese Y: ")
                if not location_i.isnumeric() or not location_j.isnumeric():
                    raise IsNotNumber()
                elif location_i.isnumeric() and location_j.isnumeric():
                    location_j = int(location_j)
                    location_i = int(location_i)
                if location_i > 14 or location_i < 0:
                    raise OutOfRange()
                elif location_j > 14 or location_j < 0:
                    raise OutOfRange()
                else:
                    location = (location_i, location_j)
                    return location
            except Exception as e:
                print(e)
                
    def get_orientation(self):
        while True:
            try:
                orientation = input ("Orientacion V o H: ")
                orientation = orientation.upper()
                ori = ["V", "H"]
                if orientation not in ori:
                    raise ValueError
                return orientation
            except ValueError:
                print("Ingrese V o H")






