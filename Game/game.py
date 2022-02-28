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

    """ Initialize Class """
    def __init__(self, file):
        # initialize game
        pygame.init()
        pygame.display.set_caption(get_val("title"))
        icon = pygame.image.load(get_val("icon"))
        pygame.display.set_icon(icon)

        # game variables
        self.clock            = pygame.time.Clock()
        self.file             = file
        self.grid_array       = []
        self.running          = True

        # file variables
        self.colors      = []
        self.name        = ""
        self.grid_size   = [0, 0]
        self.grid_window = [0, 0]
        self.grid_mult   = 60

        # solver variables
        self.current_color    = ""
        self.tries            = 0
        self.backtrack_index  = 0
        self.solved_index     = 0
        self.solve_value      = 0

        # solver lists
        self.start_position   = []
        self.final_position   = []
        self.connected_colors = []
        self.visited_cells    = []

        # window variables
        self.main_surface = None
        self.grid_surface = None

        # text variables
        self.moves_value = ""
        self.font_lg = pygame.font.SysFont(get_val("font"), get_val("font_sz"))
        self.font_sm = pygame.font.SysFont(get_val("font"), int(get_val("font_sz")/2))

        # load level
        self.load_level()
    """ ---------------- """



    """ Load a Level From a File """
    def load_level(self):

        # reset values
        self.grid_array         = []
        self.visited_cells      = []
        self.connected_colors   = []
        self.current_color      = ""
        self.backtrack_index    = 0
        self.solved_index       = 0
        self.solve_value        = 0

        # open level file
        with open(self.file) as level:
            level = json.load(level)
            self.name = level["name"]
            self.grid_size = [level["width"], level["height"]]
            self.grid_window = [self.grid_size[0]*self.grid_mult, self.grid_size[1]*self.grid_mult]
            self.grid_array  = numpy.empty(self.grid_size, dtype="U10")

            # regenerate window
            self.generate_surfaces()
            self.generate_buttons()

            # get colors
            self.colors = []
            for color in level["colors"]:
                self.colors.append(color)

            # draw dots
            for dot in level["dots"]:
                x = dot["x"]
                y = dot["y"]
                self.draw_dot(dot["x"], dot["y"], self.parse_color_from_json(dot["color"]))
                self.grid_array[x][y] = dot["color"]

            # draw level label
            text_level_indicator = self.font_lg.render("{}".format(self.name), False, get_val("cyan"))
            self.main_surface.blit(text_level_indicator, (380, 20))

        # get starting level values
        self.current_color   = self.colors[self.solved_index]
        self.start_position = numpy.argwhere(self.grid_array == self.current_color).tolist()[0]
        self.final_position = numpy.argwhere(self.grid_array == self.current_color).tolist()[1]
        self.visited_cells.append(self.start_position)
    """ ------------------------ """



    """ Generate Surfaces """
    def generate_surfaces(self):
        # main window
        self.main_surface = pygame.display.set_mode((get_val("window_width"), get_val("window_height")))
        self.main_surface.fill(get_val("black"))

        # game grid
        self.grid_surface = pygame.Surface((self.grid_window[0], self.grid_window[1]))
        self.grid_surface.fill(get_val("grey"))

        # generate grid
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                pygame.draw.rect(self.grid_surface, get_val("cyan"), [60 * y, 60 * x, 60, 60], 1)
    """ ----------------- """



    """ Generate Buttons """
    def generate_buttons(self):

        # clear button
        clear_button_text = self.font_sm.render("Learn", False, get_val("white"))
        pygame.draw.rect(self.main_surface, get_val("cyan"), (400, 195, 150, 30))
        self.main_surface.blit(clear_button_text, (443, 195))

        # solve button
        solve_button_text = self.font_sm.render("Result", False, get_val("purple"))
        pygame.draw.rect(self.main_surface, get_val("white"), (400, 245, 150, 30))
        self.main_surface.blit(solve_button_text, (440, 245))

        # quit button
        quit_button_text = self.font_sm.render("Quit", False, get_val("purple"))
        pygame.draw.rect(self.main_surface, get_val("white"), (400, 295, 150, 30))
        self.main_surface.blit(quit_button_text, (450, 295))
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

        ww = get_val("window_width")
        wh = get_val("window_width")

        gw = self.grid_window[0]
        gh = self.grid_window[1]

        w = int((ww-gw)/(self.grid_size[0]*2))
        h = int((wh-gh)/(self.grid_size[1]*2))

        # set labels
        self.main_surface.blit(self.grid_surface, (w, h))
        self.main_surface.blit(text_moves_label,  (415, 80))
        self.main_surface.blit(text_moves_value,  (415, 125))
    """ -------------- """



    """ Draw Dot -----------------------
            Based on the reference code,
            will draw a dot on the grid.
    """
    def draw_dot(self, x, y, color):
        pygame.draw.circle(
            self.grid_surface,
            color,
            (x * 60 + 30, y * 60 + 30),
            25
        )

    """ ---------------------------- """



""" -------------------------------- """
