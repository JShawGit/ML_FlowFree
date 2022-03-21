""" Global Vars ----------------------------------------
    This file contains global variables for the program.
    Game code is based on Github project:
    https://github.com/hreso110100/FlowFree-Solver
"""

""" ------------------------------------ """
VARS = {
    # colors
    "black":  (6,   18,  24),
    "grey":   (38,  50,  56),
    "white":  (255, 255, 255),
    "yellow": (255, 234, 0),
    "green":  (76,  175, 80),
    "cyan":   (0,   230, 118),
    "blue":   (0,   145, 234),
    "purple": (103, 58,  183),
    "red":    (211, 47,  47),

    # game constants, change for different results
    "font":             "arialblack",
    "font_sz":          40,
    "fps":              900,
    "icon":             "assets/icon.png",
    "title":            "Flow Free RL Project",
    "window_width":     600,
    "window_height":    400,
}
""" ------------------------------------ """



""" Get Val ----------------------------
        Gets an item from the dictionary
"""
def get_val(key):
    # check if string
    if not isinstance(key, str):
        print("ERROR: dictionary key value is not a string!")
        exit(-2)

    # check if in dictionary
    err = "Doesn't exist!"
    res = VARS.get(key, err)
    if res == err:
        print("ERROR: " + key + " is not a global variable!")
        exit(-3)

    # return result
    return res
""" ------------------------------------ """



""" Set Val --------------------------
        Sets an item in the dictionary
"""
def set_val(key, value):
    # check if string
    if not isinstance(key, str):
        print("ERROR: dictionary key value is not a string!")
        exit(-4)

    # set in dictionary
    VARS[key] = value
""" ------------------------------------ """
