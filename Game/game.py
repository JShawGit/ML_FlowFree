# external libraries
import pygame
import numpy
import json

# written programs
import global_vars as g
import solver as s
"""
    Game code referenced from Github Flow Free repository:
    https://github.com/hreso110100/FlowFree-Solver
"""

# test file to run, change this
TO_RUN = "test.json"


""" Main Program --------------------------
        Run this to run the entire program.
"""
def main_program(level_file):

    g.init_global()
    init_game(level_file)

    while g.RUNNING:
        gen_fonts()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g.RUNNING = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_button(level_file)
        pygame.display.flip()
        g.GAME_VARS["clock"].tick(g.FPS)
""" ------------------------------------ """



""" Init Game ----------------------------------------------
        Initializes the Flow Free game with a specifc level.
"""
def init_game(level_file):
    # initialize the game window
    pygame.init()
    pygame.display.set_caption(g.PROGRAM_NAME)
    g.GAME_VARS["clock"] = pygame.time.Clock()
    g.FONT_LG = pygame.font.SysFont(g.FONT, 28)
    g.FONT_SM = pygame.font.SysFont(g.FONT, 16)

    # load game interface
    load_level(level_file)
""" ------------------------------------ """



""" Load Level
        Loads a level from a file.
"""
def load_level(level_file):

    # initialize game variables
    g.GAME_VARS["actual_color"]    = ""
    g.GAME_VARS["backtrack_index"] = 0
    g.GAME_VARS["grid_array"]      = numpy.empty((g.GRID_SIZE[0], g.GRID_SIZE[1]), dtype="U10")
    g.GAME_VARS["solve_value"]     = 0
    g.GAME_VARS["solved_index"]    = 0
    g.GAME_VARS["visited_cells"]   = []

    # set window
    surface = pygame.display.set_mode((g.WINDOW_WIDTH, g.WINDOW_HEIGHT))
    surface.fill(g.CYAN)
    g.GAME_WINDOW["main_surface"] = surface

    # set grid
    surface = pygame.Surface((g.GRID_WIDTH, g.GRID_HEIGHT))
    surface.fill(g.GREY)
    g.GAME_WINDOW["grid_surface"] = surface

    # solve button
    button_text = g.FONT_SM.render("Solve", False, g.PURPLE)
    pygame.draw.rect(g.GAME_WINDOW["main_surface"], g.WHITE, (400, 240, 150, 30))
    g.GAME_WINDOW["main_surface"].blit(button_text, (453, 245))

    # restart button
    button_text = g.FONT_SM.render("Restart", False, g.WHITE)
    pygame.draw.rect(g.GAME_WINDOW["main_surface"], g.PURPLE, (400, 290, 150, 30))
    g.GAME_WINDOW["main_surface"].blit(button_text, (445, 295))

    # open this level's json file
    with open("levels/" + level_file) as file:
        file = json.load(file)
        level = file

        for dot in level["dots"]:
            pygame.draw.circle(g.GAME_WINDOW["grid_surface"], parse_color(dot["color"]), (dot["x"], dot["y"]), 25)
            g.GAME_VARS["grid_array"][dot["index_y"]][dot["index_x"]] = dot["color"]

        text_level_indicator = g.FONT_LG.render("{id}".format(id=level["name"]), False, g.BLACK)
        g.GAME_WINDOW["main_surface"].blit(text_level_indicator, (430, 0))

    g.GAME_VARS["actual_color"]   = g.DOT_COLORS[g.GAME_VARS["solved_index"]]
    g.GAME_VARS["start_position"] = numpy.argwhere(g.GAME_VARS["grid_array"] == g.GAME_VARS["actual_color"]).tolist()[0]
    g.GAME_VARS["final_position"] = numpy.argwhere(g.GAME_VARS["grid_array"] == g.GAME_VARS["actual_color"]).tolist()[1]
    g.GAME_VARS["visited_cells"].append(g.GAME_VARS["start_position"])
""" ------------------------------------ """



""" Gen Fonts
        Generates game overlay fonts.
"""
def gen_fonts():

    text_moves_label = g.FONT_LG.render("Tries", False, g.WHITE)
    g.GAME_TEXT["moves_value"] = g.FONT_LG.render(str(g.GAME_VARS["tries"]), False, g.PURPLE)
    g.GAME_TEXT["cant_solve"]  = g.FONT_LG.render("CANNOT SOLVE !", False, g.RED)

    g.GAME_WINDOW["main_surface"].blit(g.GAME_WINDOW["grid_surface"], (10, 10))
    g.GAME_WINDOW["main_surface"].blit(text_moves_label, (400, 50))
    g.GAME_WINDOW["main_surface"].blit(g.GAME_TEXT["moves_value"], (500, 50))
""" ------------------------------------ """


""" Click Button
        Activates when a button is clicked
"""
def click_button(level_file):
    # get click location
    mouse_pos = pygame.mouse.get_pos()

    # restart button
    if 550 > mouse_pos[0] > 400 and 320 > mouse_pos[1] > 290:
        tries = 0
        load_level(level_file)

    # solve button
    elif 550 > mouse_pos[0] > 400 and 270 > mouse_pos[1] > 240:
        while g.GAME_VARS["solve_value"] == 0:
            s.solver(g.GAME_VARS["start_position"], level_file)
""" ------------------------------------ """



""" Parse Color --------------------------------
        Parse color string to RGB tuple.
"""
def parse_color(color):
    if color == "RED":
        return g.RED
    elif color == "GREEN":
        return g.GREEN
    elif color == "BLUE":
        return g.BLUE
    elif color == "YELLOW":
        return g.YELLOW
    elif color == "PURPLE":
        return g.PURPLE
""" ------------------------------------ """



""" ------------------------------------ """
"""     run if this file is executed     """
if __name__ == "__main__":
    main_program(TO_RUN)
""" ------------------------------------ """
