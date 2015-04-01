"""
patterninputs.py
----------------

A place to create new input methods which can load in
patterns to be used by the core module.

"""


import csv

def load (filename):
    pattern = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            pattern.append([bool(int(i)) for i in row])

    return pattern


# ----- TESTING CODE ----- #
if __name__ == "__main__":
    print(load('testpattern.csv'))
