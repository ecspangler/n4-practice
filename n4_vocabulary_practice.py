import csv
import argparse
import pandas as pd
import numpy as np
import random
import glob
import os
import re
import shutil

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def practice(set_number, split_lists):
    practice_set = split_lists[int(set_number)]
    set_row_count = len(practice_set.index)
    print("\nPractice set",set_number,":",set_row_count,"words")
    action = ""

    while True:
        for x in range(set_row_count):
            print("\n=================================================================")
            row = practice_set.iloc[x]

            practice_list = ["hiragana","english"]
            if row["kanji"] and str(row["kanji"]) != "nan" and str(row["kanji_required"]) == "x":
                practice_list.append("kanji")

            random_select_list = []
            for x in range(len(practice_list)):
                random_select_list.append(x)
            selected_index = random.choice(random_select_list)
            random_select_list.remove(selected_index)

            print(row[practice_list[selected_index]])

            action = input("\nEnter to see answer, \'s\' to scramble, or \'q\' to quit this set: ")
            if action == "s":
                practice_set = practice_set.sample(frac=1).reset_index(drop=True)
                break
            if action == "q":
                break
            else:
                print("\nAnswer:")
                for x in range(len(random_select_list)):
                    print(row[practice_list[random_select_list[x]]])
        if action == "q":
            break


parser = argparse.ArgumentParser(description='Arg parser')
parser.add_argument('--number_practice_sets', action="store", dest="number_practice_sets", type=int)
parser.add_argument('--scramble', action="store_true", default=False)

args = parser.parse_args()
number_practice_sets = args.number_practice_sets
full_vocab_list = pd.read_csv('vocab/N5-N4_vocab_list.csv', names=['kanji','hiragana','english','kanji_required'])
row_count = len(full_vocab_list.index)
vocab_file_path = "./vocab_lists"
split_lists = []

selection = input("\nEnter to generate practice sets, or \'prev\' to use previous: ")

if selection == "prev":
    number_practice_sets = 0
    for file in sorted(glob.glob(os.path.join(vocab_file_path, "*.csv")),key=numericalSort):
        print("Reading file:", os.path.splitext(os.path.basename(file))[0])
        df = pd.read_csv(file)
        split_lists.append(df)
        number_practice_sets += 1
else:
    if args.scramble:
        full_vocab_list = full_vocab_list.sample(frac=1).reset_index(drop=True)

    split_lists = np.array_split(full_vocab_list,number_practice_sets)

    for file in os.listdir(vocab_file_path):
        file_path = os.path.join(vocab_file_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    for x in range(len(split_lists)):
        file_path = vocab_file_path + "/vocab_list_" + str(x) + ".csv"
        split_lists[x].to_csv(file_path,index=False)

while True:
    print("\n\nThere are", row_count, "vocabulary words in", number_practice_sets, "practice sets:")
    for x in range(0, number_practice_sets):
        print(x)

    action = input("\nSelect a set number to practice or type \'exit\' to end: ")
    if action == "exit":
        break
    else:
        practice(action, split_lists)
