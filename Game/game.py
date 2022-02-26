from global_vars import get_val
import pygame
import numpy
import json

""" Game -------------------------------------
    This file contains the FlowFree game code.
    Game code is based on Github project:
    https://github.com/hreso110100/FlowFree-Solver
"""


""" Game Class
        This contains all of the game-data and functions.
        It runs the game itself.
"""
class Game:

    """ Initialize Class
            Initializes a game 'object'.
    """
    def __init__(self, file):
        pygame.init()

        # game variables
        self.actual_color     = ""
        self.backtrack_index  = 0
        self.clock            = pygame.time.Clock()
        self.connected_colors = []
        self.current_level    = file
        self.final_position   = []
        self.game_array       = []
        self.running          = True
        self.solve_value      = 0
        self.solved_index     = 0
        self.start_position   = []
        self.tries            = 0
        self.visited_cells    = []

        # window variables
        self.main_surface = None
        self.grid_surface = None

        # text variables
        self.moves_value = ""
        self.cant_solve  = ""
        self.font_lg = None
        self.font_sm = None

        pygame.display.set_caption(get_val("title"))
        self.load_level(file)
    """ ---------------- """



    """ Load a Level From a File """
    def load_level(self, file):
        # reset values
        self.font_lg            = pygame.font.SysFont(get_val("font"), get_val("font_sz"))
        self.game_array         = numpy.empty(get_val("grid_size"), dtype="U10")
        self.visited_cells      = []
        self.connected_colors   = []
        self.actual_color       = ""
        self.backtrack_index    = 0
        self.solved_index       = 0
        self.solve_value        = 0

        # regenerate window
        self.generate_surfaces()
        self.generate_buttons()

        # open level file
        with open(file) as levels_file:
            levels_file = json.load(levels_file)
            level_one = levels_file["levels"][1]

            # draw dots
            for dot in level_one["dots"]:
                pygame.draw.circle(self.grid_surface, self.parse_color_from_json(dot["color"]), (dot["x"], dot["y"]), 25)
                self.game_array[dot["index_y"]][dot["index_x"]] = dot["color"]

            # draw level label
            text_level_indicator = self.font_lg.render(
                "LEVEL {id}".format(id=level_one["id"]), False, get_val("cyan")
            )
            self.main_surface.blit(text_level_indicator, (430, 0))

        # get starting level values
        self.actual_color   = get_val("available_colors")[self.solved_index]
        self.start_position = numpy.argwhere(self.game_array == self.actual_color).tolist()[0]
        self.final_position = numpy.argwhere(self.game_array == self.actual_color).tolist()[1]
        self.visited_cells.append(self.start_position)
    """ ------------------------ """



    """ Generate Surfaces """
    def generate_surfaces(self):
        # main window
        self.main_surface = pygame.display.set_mode((get_val("window_width"), get_val("window_height")))
        self.main_surface.fill(get_val("grey"))

        # game grid
        self.grid_surface = pygame.Surface((get_val("grid_width"), get_val("grid_height")))
        self.grid_surface.fill(get_val("grey"))

        # generate grid
        for x in range(get_val("grid_size")[0]):
            for y in range(get_val("grid_size")[1]):
                pygame.draw.rect(self.grid_surface, get_val("cyan"), [60 * y, 60 * x, 60, 60], 1)
    """ ----------------- """



    """ Generate Buttons """
    def generate_buttons(self):
        self.font_sm = pygame.font.SysFont(get_val("font"), int(get_val("font_sz")/2))

        # solve button
        solve_button_text = self.font_sm.render("Solve", False, get_val("purple"))
        pygame.draw.rect(self.main_surface, get_val("white"), (400, 240, 150, 30))
        self.main_surface.blit(solve_button_text, (453, 245))

        # restart button
        restart_button_text = self.font_sm.render("Restart", False, get_val("white"))
        pygame.draw.rect(self.main_surface, get_val("purple"), (400, 290, 150, 30))
        self.main_surface.blit(restart_button_text, (445, 295))

        # quit button
        quit_button_text = self.font_sm.render("Quit", False, get_val("purple"))
        pygame.draw.rect(self.main_surface, get_val("white"), (400, 340, 150, 30))
        self.main_surface.blit(quit_button_text, (445, 345))
    """ ---------------- """



    """ Parse Color From Json """
    def parse_color_from_json(self, color):
        if color == "RED":
            return get_val("red")
        elif color == "GREEN":
            return get_val("green")
        elif color == "BLUE":
            return get_val("blue")
        elif color == "YELLOW":
            return get_val("yellow")
        elif color == "PURPLE":
            return get_val("purple")
    """ --------------------- """



    """ Generate Fonts """
    def generate_fonts(self):
        # create labels
        text_moves_label = self.font_lg.render("Tries", False, get_val("white"))
        text_moves_value = self.font_lg.render(str(self.tries), False, get_val("purple"))
        self.cant_solve  = self.font_lg.render("CANNOT SOLVE !", False, get_val("red"))

        # set labels
        self.main_surface.blit(self.grid_surface, (10, 10))
        self.main_surface.blit(text_moves_label,  (400, 50))
        self.main_surface.blit(text_moves_value,  (500, 50))
    """ -------------- """



    """ ------------------------ """
