import serial


# ----- HARDWARE CONSTANTS ----- #
COLS = 20  # Number of solenoids available
ON_DURATION = 0.25  # Duration on per pattern row
OFF_DURATION = 0.5  # Duration off between pattern rows


# ----- HARDWARE CLASSES ----- #
class Pattern:
    _hardware_locked = False

    def __init__ (pattern, invert=true, alignment=None):
        """
        Takes in a pattern (list of lists, formatted [row][column])
        of true/false or 1/0 values and loads it in for use by the
        play or loop functions.
        """

        self.pattern = align(pattern)
        self.pattern = pattern[::-1] # Reverse the vertical alignment of the pattern



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
