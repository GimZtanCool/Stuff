import nltk
from nltk.corpus import words
import tkinter as tk
from tkinter import simpledialog

def get_word_length():
    word_length = int(input("Size of the word: "))
    return word_length

def run(word_length, word_list):
    red_clues, yellow_clues, green_clues = [], [], []
    filter_words = word_list
    

    def get_input():
        inputs = list(input().strip())
        for i in range(word_length):
            color = int(input(f"Enter color for letter {inputs[i]} (1=green, 2=yellow, 3=red): "))
            # green
            if color == 1:
                green_clues.append((inputs[i], i))
            # yellow
            elif color == 2:
                yellow_clues.append((inputs[i], i))
            # red
            elif color == 3:
                red_clues.append((inputs[i],i))

    current_row = 0
    for i in range(5):
        get_input()
        filter_words = filter_word_by_clues(filter_words, green_clues, yellow_clues, red_clues)
        best_words = find_best_posible_first_word(filter_words)
        for word, score in best_words[:10]:
            print(word, ' score: ', score)
        current_row += 2
        red_clues, yellow_clues, green_clues = [], [], []  # Clear clues for the next iteration


def filter_word_by_clues(words_list, green_clues, yellow_clues, red_clues):
    # las clues son 
    # verde - en esa posicion esa letra
    # amarillo - esa letra en otra posicion
    # amarillo - verificar si al menos hay una de esa letra en otra posicion
    # rojo esa letra no
    
    filtered_words = []

    for word in words_list:
        if word == "stair": 
            print('found')
        # green
        green_match = all(word[clue_index] == clue for clue, clue_index in green_clues)
        if not green_match:
            continue

        # yellow
        # check  word is not in the position in clue_index
        yellow_sub_match = 0
        yellow_match = 0
        for clue, clue_index in yellow_clues:
            if word[clue_index]==clue:
                yellow_match = 1
                break
            # only counts different than green clues
            exclude = []
            for i in range(len(green_clues)):
                if green_clues[i][0]==clue:
                    exclude.append(i)

            for i in range(len(word)):
                if word[i] == clue and i not in exclude:
                    yellow_sub_match+=1
                    break
                
        if yellow_match or yellow_sub_match!=len(yellow_clues):
            continue
        
        # red
        # if its a red clue which letter dont appear in the other clues then that letter must not appear
        # if not then that letter in that word[clue_index]
        red_match = 0
        for clue, clue_index in red_clues:
            useless = []
            for i in range(len(yellow_clues)):
                if clue == yellow_clues[i][0]:
                    useless.append(yellow_clues[i][1])

            if not useless:  
                for i in range(len(green_clues)):
                    if clue == green_clues[i][0]:
                        useless.append(green_clues[i][1])

                        
            if useless:
                for i in range(len(word)):
                   if word[i]==clue and i not in useless:
                       red_match=1
                       break
            else:
                if clue in word:
                    red_match=1

            
        if red_match:
            continue

        filtered_words.append(word)

    return filtered_words

def find_best_posible_first_word(words_list):
    letter_frequencies = {
        'e': 12.02,
        't': 9.10,
        'a': 8.12,
        'o': 7.68,
        'i': 7.31,
        'n': 6.95,
        's': 6.28,
        'r': 6.02,
        'h': 5.92,
        'd': 4.32,
        'l': 3.98,
        'u': 2.88,
        'c': 2.71,
        'm': 2.61,
        'f': 2.30,
        'y': 2.11,
        'w': 2.09,
        'g': 2.03,
        'p': 1.82,
        'b': 1.49,
        'v': 1.11,
        'k': 0.69,
        'x': 0.17,
        'q': 0.11,
        'j': 0.10,
        'z': 0.07
    }
    words_list = list(words_list) 
    word_scores = [0] * len(words_list)
    for i in range(len(words_list)):
        for c in words_list[i]:
            word_scores[i] += letter_frequencies.get(c, 0)/words_list[i].count(c)
    scored_words = sorted(zip(words_list, word_scores), key=lambda x: x[1], reverse=True)
    return scored_words
            
def main():
    with open('input.txt', 'r') as file:
        words_list = file.read().splitlines()
    word_set = {word.lower() for word in words_list}
    #word_length = get_word_length()
    word_length = 5
    words_list = [word for word in word_set if len(word) == word_length]
    best_words = find_best_posible_first_word(words_list)
    for word, score in best_words[:10]:
        print(word, ' score: ', score)

    run(word_length, words_list)

    

if __name__ == "__main__":
    main()



