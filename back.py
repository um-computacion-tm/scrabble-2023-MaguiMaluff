from game.scrabble_game import ScrabbleGame, InvalidTask, IsNotNumber, OutOfRange, OutOfTiles

class Back:
    def __init__(self):
        self.end_count = 0

    def get_task(self):
        while True:
            try:
                print('A- Add word')
                print('C- Change tiles')
                print('P- Pass turn')
                print('E- End game')
                task = input('Your choice: ')
                task = task.upper()
                if task not in ["A", "C", "P", 'E']:
                    raise InvalidTask("Invalid Task")
                else:
                    return task
            except Exception as e:
                print(e)
    
    def get_word_main(self):
        while True:
            try:
                word = input("Word:")
                word = word.upper()
                for i in word:
                    if not i.isalpha():
                        raise ValueError
                    else:
                        return word
            except ValueError:
                print("Invalid")
    
    def get_location(self):
        while True:
            try:
                location_i = input("X: ")
                location_j = input("Y: ")
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
                orientation = input ("Orientation V or H: ")
                orientation = orientation.upper()
                ori = ["V", "H"]
                if orientation not in ori:
                    raise ValueError
                return orientation
            except ValueError:
                print("Please enter V o H")


    def check_ending(self, task, people):
        if task == "P":
            self.end_count += 1
        elif task != "P":
            self.end_count == 0
        if self.end_count == (people * 2):
            ScrabbleGame().end_game()





