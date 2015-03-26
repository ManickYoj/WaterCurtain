"""
hardwareiface.py
----------------

The interface which allows patterns to be played on the
water curtain.

IDEA: Clients for submitting patterns in democratized way.
"""

# ----- IMPORTS ----- #
import serial
import queue as q

# ----- HARDWARE CONSTANTS ----- #
COLS = 20  # Number of solenoids available
ON_DURATION = 0.25  # Duration on per pattern row
OFF_DURATION = 0.5  # Duration off between pattern rows

# ----- PATTERN CLASS ----- #
class Pattern:
    PLAY = {
        "loop" : -1
        "stop" : 0
    }

    def __init__ (pattern, invert=true, alignment=None):
        """
        Takes in a pattern (list of lists, formatted [row][column])
        of true/false or 1/0 values and loads it in for use by the
        play or loop functions.
        """

        self.pattern = align(pattern)
        self.pattern = self.pattern[::-1] # Reverse the vertical alignment of the pattern
        self.play_counter = 0


    def align (self, pattern, alignment=None):
        """
        Takes a pattern and shifts it to the left, right, or center if
        the number of columns is less than the number of available
        solenoids. Also raises an exception if the pattern is too large
        for the number of solenoids available.
        """

        cols = len(self.pattern[0])

        #  Center the
        if cols >= COLS:
            raise Exception("Columns in pattern exceed the number of solenoids available.")
        elif cols == COLS-1:  # If the pattern is the same length as the number of available solenoids
            return pattern
        else:
             # TODO: Align pattern by pushing it left, right, or centered if undersized
            if alignment:
                pattern = pattern
            else:
                return pattern

    def play (self, times=1):
        self.play_counter = Pattern.PLAY[times]

    def loop (self):
        self.play_counter = Pattern.PLAY["loop"]

# ----- HARDWARE FUNCTIONS ----- #
pattern_queues = []

def register (pattern):
    pattern_queues.append(pattern)

def unregister (pattern):
    del pattern_queues[pattern]

def runpattern (pattern):
    # TODO: Link this to hardware here
    for row in pattern:
        rowstr = ""

        for col in row:
            if col: rowstr += "X"
            else: rowstr += " "

        print(rowstr)

def run ():
    counter = 0;

    while True:
        if counter == len(pattern_queues): counter = 0
        else:
            # If the play-counter has a finite number of plays
            if pattern_queues[counter].play_counter > 0:
                runpattern(pattern_queues[counter].pattern)
                pattern_queues[counter].play_counter -= 1

            # If the play-counter is looping
            elif pattern_queues[counter].play_counter < 0:
                runpattern(pattern_queues[counter].pattern)

        counter += 1


# ----- SCRIPT ---- #
run()

# ----- TESTING CODE ----- #
if __name__ == "__main__":
    #
    p = [[True for cols in range(COLS)] for rows in range(COLS)]
    pattern = Pattern(p)
    pattern.play(1)


