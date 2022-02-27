import pygame

from global_vars import get_val
import solver as s
import qlearn as q
import game as g

""" Main -------------------------------------
    This file is the main file of the program.
    Game code is based on Github project:
    https://github.com/hreso110100/FlowFree-Solver
"""

GAME_FILE = 'levels/4x4.json'
ALPHA   = 1
EPSILON = 1
GAMMA   = 1

""" Main ----------------------------------
        This is the main program's function
"""
def main(file):
    # create the game
    game = g.Game(file)

    # create learning agent
    agent = q.Q_Learn_Agent(game, ALPHA, EPSILON, GAMMA)

    # while the game is running
    while game.running:
        # update text
        game.generate_fonts()

        # listen for mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_click_buttons(game, agent)

        pygame.display.flip()
        game.clock.tick(get_val("fps"))
""" ----------------------------------- """



""" Handle Click Buttons --------- """
def handle_click_buttons(game, agent):

    mouse_position = pygame.mouse.get_pos()

    # restart button click handling
    if 550 > mouse_position[0]   > 400 and 225 > mouse_position[1] > 195:
        game.tries = 0
        game.load_level()

    # solve level button click handling
    elif 550 > mouse_position[0] > 400 and 270 > mouse_position[1] > 245:
        while game.solve_value == 0:
            agent.search_algo()

    # exit button click handling
    elif 550 > mouse_position[0] > 400 and 325 > mouse_position[1] > 295:
        print("Game exited!")
        exit(0)
""" -------------------- """



""" Run this if this file is ran """
if __name__ == "__main__":
    main(GAME_FILE)
""" --------------------------- """
