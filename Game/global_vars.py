""" Global Vars ----------------------------------------
    This file contains global variables for the program.
    Game code is based on Github project:
    https://github.com/hreso110100/FlowFree-Solver
"""

""" ------------------------------------ """
VARS = {
    # colors
    "black":  (0,   0,   0),
    "grey":   (38,  50,  56),
    "white":  (255, 255, 255),
    "yellow": (255, 234, 0),
    "green":  (76,  175, 80),
    "cyan":   (0,   230, 118),
    "blue":   (0,   145, 234),
    "purple": (103, 58,  183),
    "red":    (211, 47,  47),

    # game constants, change for different results
    "available_colors": ["RED", "BLUE", "GREEN", "PURPLE", "YELLOW"],
    "grid_width":       360,
    "grid_height":      360,
    "grid_size":        [6, 6],
    "font":             "impact",
    "font_sz":          28,
    "fps":              60,
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
