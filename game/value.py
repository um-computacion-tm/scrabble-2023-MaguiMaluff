from game.models import Cell, Tiles

def calculate_word_value(word):
        
        counter = 0
        word_multiplier = 1

        for i in range(len(word)):
            cell = word[i]

            if cell.letter is None:
                    return 0
            if cell.multiplier_type == 'letter':
                counter = counter + (cell.letter.value * cell.multiplier * word_multiplier)

            if cell.multiplier_type == 'word' and word_multiplier != 1:
                counter = ((counter + cell.letter.value) * word_multiplier)
                word_multiplier = word_multiplier * cell.multiplier

            if cell.multiplier_type == 'word' and word_multiplier == 1 and cell.state == True:
                word_multiplier = cell.multiplier
                counter = ((counter + cell.letter.value) * word_multiplier)

            cell.used_cell() 
        return counter

        
