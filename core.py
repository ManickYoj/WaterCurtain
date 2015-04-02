"""
core.py
----------------

The interface which allows patterns to be played on the
water curtain. It uses the config.ini file to load in
user configuration.

"""

# ----- IMPORTS ----- #
import arduino
import time
import queue as q
import configloader

# ---- IMPORT CONFIG ----- #
config = configloader.loadconfig()
config['cols'] = int(config['cols'])
config['pin_offset'] = int(config['pin_offset'])

# -----  GLOBAL VARIABLES ----- #
empty_row = [False for i in range(config['cols'])]
if not config['test_mode']:
    board = arduino.Arduino(config['usb_port'])
    board.output([i for i in range(config['pin_offset'], config['pin_offset']+config['cols'])])

# ----- PATTERN CLASS ----- #
class Pattern:
    PLAY = {
        "loop" : -1,
        "stop" : 0
    }

    def __init__ (self, pattern, invert=True, alignment=None):
        """
        Takes in a pattern (list of lists, formatted [row][column])
        of true/false or 1/0 values and loads it in for use by the
        play or loop functions.
        """

        self.pattern = self.align(pattern)
        self.pattern = self.pattern[::-1] # Reverse the vertical alignment of the pattern
        self.play_counter = 0
        register(self)


    def align (self, pattern, alignment=None):
        """
        Takes a pattern and shifts it to the left, right, or center if
        the number of columns is less than the number of available
        solenoids. Also raises an exception if the pattern is too large
        for the number of solenoids available.
        """

        cols = len(pattern[0])

        if cols > config['cols']:
            raise Exception("Columns in pattern exceed the number of solenoids available.")
        elif cols == config['cols']:  # If the pattern is the same length as the number of available solenoids
            return pattern
        else:
             # TODO: Align pattern by pushing it left, right, or centered if undersized
            if alignment:
                pattern = pattern
            else:
                return pattern

    def play (self, times=1):
        self.play_counter = times

    def loop (self):
        self.play_counter = Pattern.PLAY["loop"]

# ----- HARDWARE FUNCTIONS ----- #
pattern_queues = []

def register (pattern):
    pattern_queues.append(pattern)

def unregister (pattern):
    del pattern_queues[pattern]

def run ():
    patternop = testpattern if config['test_mode'] else runpattern
    counter = 0;

    while True:
        if len(pattern_queues) > 0:
            # If the play-counter has a finite number of plays
            if pattern_queues[counter].play_counter > 0:
                patternop(pattern_queues[counter].pattern)
                pattern_queues[counter].play_counter -= 1

            # If the play-counter is looping
            elif pattern_queues[counter].play_counter < 0:
                patternop(pattern_queues[counter].pattern)

            counter += 1
            if counter == len(pattern_queues): counter = 0

def testpattern (pattern):
    for row in pattern:
        rowstr = ""

        for col in row:
            if col: rowstr += "X"
            else: rowstr += " "

        print(rowstr)
        # Turn on
        time.sleep(config['on_duration'])
        # Turn off
        time.sleep(config['off_duration'])

def runpattern (pattern):
    for row in pattern:
        print(row)
        # Turn on
        setPins(row)
        time.sleep(config['on_duration'])

        # Turn off
        setPins(empty_row)
        time.sleep(config['off_duration'])


def setPins(row):
    for i in range(len(row)):
        pin = i + config['pin_offset']
        if row[i]: board.setHigh(pin)
        else: board.setLow(pin)


# ----- TESTING CODE ----- #
if __name__ == "__main__":
    import threading
    threading.Thread(target=run).start()

    # Test play method directly
    p = [[True for cols in range(config['cols'])] for rows in range(5)]
    pattern = Pattern(p)
    pattern.play(10)

    # Test CSV Imports
    import patterninputs as csvi
    import os
    csvpattern = Pattern(csvi.load(os.path.join('patterns','alternating.csv')))
    csvpattern.play(10)

    csvpattern2 = Pattern(csvi.load(os.path.join('patterns','diagonal.csv')))
    csvpattern2.play(10)
