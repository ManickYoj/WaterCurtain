"""
hardwareiface.py
----------------

The interface which allows patterns to be played on the
water curtain. At present, the USB_PORT field will need
to be changed frequently.

IDEA: Clients for submitting patterns in democratized way.
"""

# ----- CONFIG ----- #
# Software Settings
COLS = 10  # Number of solenoids available
ON_DURATION = 1  # Duration on per pattern row
OFF_DURATION = 2  # Duration off between pattern rows
PIN_OFFSET = 2  # Number of first pin hooked up on the Arduino

# Hardware Settings
TEST_MODE = False  # Switches between testing and operation modes
USB_PORT = '/dev/ttyACM0'  # The port address of the Arduino

# ----- IMPORTS ----- #
import arduino
import time
import queue as q

# -----  CONSTANTS ----- #
CLEAR_ROW = [False for i in range(COLS)]
if not TEST_MODE:
    BOARD = arduino.Arduino(USB_PORT)
    BOARD.output([i for i in range(PIN_OFFSET, PIN_OFFSET+COLS)])

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

        if cols > COLS:
            raise Exception("Columns in pattern exceed the number of solenoids available.")
        elif cols == COLS:  # If the pattern is the same length as the number of available solenoids
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
    patternop = testpattern if TEST_MODE else runpattern
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
        time.sleep(ON_DURATION)
        # Turn off
        time.sleep(OFF_DURATION)

def runpattern (pattern):
    for row in pattern:
        print(row)
        # Turn on
        setPins(row)
        time.sleep(ON_DURATION)

        # Turn off
        setPins(CLEAR_ROW)
        time.sleep(OFF_DURATION)


def setPins(row):
    for i in range(len(row)):
        pin = i + PIN_OFFSET
        if row[i]: BOARD.setHigh(pin)
        else: BOARD.setLow(pin)


# ----- SCRIPT ---- #
import threading
threading.Thread(target=run).start()

# ----- TESTING CODE ----- #
if __name__ == "__main__":
    p = [[True for cols in range(COLS)] for rows in range(5)]
    pattern = Pattern(p)
    pattern.play(1)

    import csvinput as csvi
    csvpattern = Pattern(csvi.load('testpattern.csv'))
    csvpattern.play(1)
