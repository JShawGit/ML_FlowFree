import pygame
""" Q Learn ----------------------------
    This file contains the RL algorithm.
"""



""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""
def q_learning(game):
    print("Q Learn!")
""" ----------------------------------- """



""" A* Search ------------------------
        Will find a path between dots.
"""
def a_search(game):
    print("A Search!")
""" ----------------------------------- """



""" Draw Dot -----------------------
        Based on the reference code,
        will draw a dot on the grid.
"""
def draw_dot(game, x, y):
    pygame.draw.circle(
        game.grid_surface,
        game.parse_color_from_json(game.current_color),
        (x * 60 + 30, y * 60 + 30),
        25
    )
""" ---------------------------- """


