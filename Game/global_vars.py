# external libraries
import pygame

""" ------------------------------------ """
# colors
BLACK  = (0,   0,   0)
GREY   = (38,  50,  56)
WHITE  = (255, 255, 255)
YELLOW = (255, 234, 0)
GREEN  = (76,  175, 80)
CYAN   = (0,   230, 118)
BLUE   = (0,   145, 234)
PURPLE = (103, 58,  183)
RED    = (211, 47,  47)

# default variables for the game
FPS     = 60
FONT    = "impact"
FONT_LG = None
FONT_SM = None
WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 400
GRID_WIDTH    = 360
GRID_HEIGHT   = 360
GRID_SIZE     = [6, 6]
PROGRAM_NAME  = "Flow Free RL Project"
RUNNING       = True
CANT_SOLVE    = ""
DOT_COLORS    = ["RED", "BLUE", "GREEN", "PURPLE", "YELLOW"]

# this will be changed throughout the program
GAME_VARS = {
    "actual_color":     None,
    "backtrack_index":  None,
    "clock":            None,
    "connected_colors": None,
    "final_position":   None,
    "grid_array":       None,
    "solve_value":      None,
    "solved_index":     None,
    "start_position":   None,
    "tries":            None,
    "visited_cells":    None
}

# this includes items that are within the game window
GAME_WINDOW = {
    "main_surface": None,
    "grid_surface": None
}

# this gives the game's display text
GAME_TEXT = {
    "moves_value": "",
    "cant_solve":  ""
}
""" ------------------------------------ """