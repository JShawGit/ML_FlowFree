import pygame

from global_vars import get_val
import tester as t
import sarsalearn as q
import game as g

""" Main -------------------------------------
    This file is the main file of the program.
    Game code is based on Github project:
    https://github.com/hreso110100/FlowFree-Solver
"""

# game constants
GAME_FILE = 'levels/test.json'
ALPHA     = 0.6
EPSILON   = 1.0
GAMMA     = 0.6
LOOPS     = 1000

# tally the learning outcomes, for science
res = {}

# can change this for experiments :)
rewards = {
    "move":              0,  # a grid space is filled
    "stuck":            -5,  # no more moves are left
    "block":           -10,  # if a path blocks another color
    "reached_empty":    75,
    "reached_filled":  100

    # "reached":        1000,  # if a path blocks another color
    # "empty": 0,  # goal is reached without filling the board
    # "filled": 0,  # goal is reached, board is filled
}



""" Main ----------------------------------
        This is the main program's function
"""
def main(file):
    # create the game
    game = g.Game(file)
    for color in game.colors:
        res[color] = {
                "block":          0,
                "stuck":          0,
                "reached_empty":  0,
                "reached_filled": 0
            }

    # create learning agent
    agent = q.Sarsa_Learn_Agent(game, ALPHA, EPSILON, GAMMA, rewards)

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
    if 550 > mouse_position[0] > 400 and 225 > mouse_position[1] > 195:
        train_agent(agent, game)
        pygame.display.flip()
        game.load_level()

    # result button click handling
    elif 550 > mouse_position[0] > 400 and 270 > mouse_position[1] > 245:
        optimal_agent(agent, game)

    # exit button click handling
    elif 550 > mouse_position[0] > 400 and 325 > mouse_position[1] > 295:
        print("Game exited!")
        exit(0)


""" -------------------- """



""" Train Agent -------- """
def train_agent(agent, game):
    # iter through learning loops
    for i in range(LOOPS):
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
        run_res = agent.iterate(True)
        for color in game.colors:
            for key in run_res[color]:
                res[color][key] += run_res[color][key]
        # res["filled"] += run_res["filled"]
        # res["empty"] += run_res["empty"]

        game.clock.tick(get_val("fps"))
        game.generate_fonts()
""" ----------------------- """



""" Optimal Agent --------- """
def optimal_agent(agent, game):
    # reset board
    pygame.display.flip()
    game.load_level()

    # learn
    res = agent.iterate(False)
    for key in res:
        print(str(key) + ": " + str(res[key]))

    # show results
    game.clock.tick(get_val("fps"))
    game.generate_fonts()
""" ------------------- """



""" Run this if this file is ran """
if __name__ == "__main__":
    main(GAME_FILE)
""" --------------------------- """
