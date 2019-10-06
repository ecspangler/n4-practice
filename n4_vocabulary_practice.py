import csv
import argparse
import pandas as pd
import numpy as np
import random

parser = argparse.ArgumentParser(description='Arg parser')
parser.add_argument('--number_practice_sets', action="store", dest="number_practice_sets", type=int)
parser.add_argument('--scramble', action="store_true", default=False)

args = parser.parse_args()
number_practice_sets = args.number_practice_sets
full_vocab_list = pd.read_csv('vocab/N5-N4_vocab_list.csv', names=['kanji','hiragana','english'])
row_count = len(full_vocab_list.index)

if args.scramble:
    full_vocab_list = full_vocab_list.sample(frac=1).reset_index(drop=True)

split_lists = np.array_split(full_vocab_list,number_practice_sets)


def practice(set_number):
    practice_set = split_lists[int(set_number)]
    set_row_count = len(practice_set.index)
    print("\nPractice set",set_number,":",set_row_count,"words")
    action = ""

    while True:
        for x in range(set_row_count):
            print("\n=================================================================")
            row = practice_set.iloc[x]

            practice_list = ["hiragana","english"]
            if row["kanji"]:
                practice_list.append("kanji")

            random_select_list = []
            for x in range(len(practice_list)):
                random_select_list.append(x)
            selected_index = random.choice(random_select_list)
            random_select_list.remove(selected_index)

            print(row[practice_list[selected_index]])

            action = input("\nEnter to see answer or \'q\' to quit this practice set: ")
            if action == "q":
                break
            else:
                print("\nAnswer:")
                for x in range(len(random_select_list)):
                    print(row[practice_list[random_select_list[x]]])
        if action == "q":
            break


while True:
    print("\n\nThere are", row_count, "vocabulary words in", number_practice_sets, "practice sets:")
    for x in range(0, number_practice_sets):
        print(x)

    action = input("\nSelect a set number to practice or type \'exit\' to end: ")
    if action == "exit":
        break
    else:
        practice( action )
