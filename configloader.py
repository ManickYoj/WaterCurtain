"""
configloader.py
---------------
Provides the utility loadconfig function to
load the configuration into a python dictionary
for ease of use.

"""

import configparser

def loadconfig(filename="config.ini"):
    config = configparser.ConfigParser()
    config.read(filename)
    sections = config.sections()
    loaded_config = {}

    for section in sections:
        for option in config[section]:

            # Attempt to load variables as booleans
            try:
                loaded_config[option] = config[section].getboolean(option)
            except:
                # Attempt to load variables as ints
                try:
                    loaded_config[option] = float(config[section][option])

                # Load variables as strings
                except:
                    loaded_config[option] = config[section][option]


    return loaded_config

# ----- Testing Code ----- #
if __name__ == "__main__":
    print(loadconfig())
