from game.models import Cell, Tiles

def calculate_word_value(word):
        counter = 0
        word_multiplier = 1
        for i in range(len[word]):
            if word[i].letter is None:
                    return 0
            if word[i].multiplier_type == 'letter':
                counter = counter + (word[i].letter.value * word[i].multiplier * word_multiplier)
            if word[i].multiplier_type == 'word' and word_multiplier == 1:
                counter = counter * word_multiplier
                word_multiplier = word[i].multiplier
            if word[i].multiplier_type == 'word' and word_multiplier != 1:
                    word_multiplier = word_multiplier * word[i].multiplier
        return counter