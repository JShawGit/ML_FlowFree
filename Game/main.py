import pygame
import time

from global_vars import get_val
import tester as t
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
LOOPS   = 100

""" Main ----------------------------------
        This is the main program's function
"""
def main(file):
    # create the game
    game = g.Game(file)

    # create learning agent
    agent = q.Q_Learn_Agent(game, ALPHA, EPSILON, GAMMA, LOOPS)

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

    # learn button click handling
    if 550 > mouse_position[0]   > 400 and 225 > mouse_position[1] > 195:
        for i in range(agent.learning_loops):
            teach_agent(agent, game)
        pygame.display.flip()
        game.load_level()

    # result button click handling
    elif 550 > mouse_position[0] > 400 and 270 > mouse_position[1] > 245:
        result_agent(agent, game)

    # exit button click handling
    elif 550 > mouse_position[0] > 400 and 325 > mouse_position[1] > 295:
        print("Game exited!")
        exit(0)
""" -------------------- """



""" Teach Agent --------- """
def teach_agent(agent, game):
    # sense exit
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
            mouse_position = pygame.mouse.get_pos()
            if 550 > mouse_position[0] > 400 and 325 > mouse_position[1] > 295:
                print("Game exited!")
                exit(0)

    # reset board
    game.tries += 1
    pygame.display.flip()
    game.load_level()

    # learn
    agent.learning_algo()

    # show results
    game.clock.tick(get_val("fps"))
    game.generate_fonts()
""" ------------------- """



""" Result Agent --------- """
def result_agent(agent, game):
    # sense exit
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
            mouse_position = pygame.mouse.get_pos()
            if 550 > mouse_position[0] > 400 and 325 > mouse_position[1] > 295:
                print("Game exited!")
                exit(0)

    # reset board
    pygame.display.flip()
    game.load_level()

    # learn
    agent.best_result()

    # show results
    game.clock.tick(get_val("fps"))
    game.generate_fonts()
""" ------------------- """



""" Test --------------------- """
def test(n_games, iter_arr, file):
    t.test_runs(
        n_games,
        iter_arr,
        file,
        ALPHA,
        EPSILON,
        GAMMA,
        LOOPS,
        "graph.png"
    )
""" ---------------------- """



""" Run this if this file is ran """
if __name__ == "__main__":
    yes = True
    if yes:
        test(
            100,
            [500, 1000, 5000],
            GAME_FILE
        )
    else:
        main(GAME_FILE)
""" --------------------------- """
