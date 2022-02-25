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
    "actual_color":     "",
    "backtrack_index":  0,
    "clock":            0,
    "connected_colors": [],
    "final_position":   [],
    "grid_array":       [],
    "solve_value":      0,
    "solved_index":     0,
    "start_position":   [],
    "tries":            0,
    "visited_cells":    []
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


""" Init Global
        Initialize the global variables.
"""
def init_global():
    global GAME_VARS, GAME_WINDOW, GAME_VARS, DOT_COLORS, CANT_SOLVE, RUNNING, PROGRAM_NAME, GRID_SIZE, GRID_WIDTH, \
           GRID_HEIGHT, WINDOW_HEIGHT, WINDOW_WIDTH, FONT_SM, FONT_LG, FONT, FPS, \
           BLACK, GREY, WHITE, YELLOW, GREEN, CYAN, BLUE, PURPLE, RED
""" ------------------------------------ """
