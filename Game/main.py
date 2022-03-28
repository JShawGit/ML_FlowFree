import traceback
import pygame

from global_vars import get_val
import test_overall as t
import qlearn_MOD as q
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
LAMBDA    = 0.6
LOOPS     = 10000
items = [ALPHA, EPSILON, GAMMA, LAMBDA]

# tally the learning outcomes, for science
res = {
    "filled":   0,  # board is filled
    "empty":    0,  # board is filled
}

# can change this for experiments :)
rewards = {
    "move":       0,  # a grid space is filled
    "stuck":     -1,  # no more moves are left
    "block":    -20,  # if a path blocks another color
    "reached":   30,  # if a path blocks another color
    "empty":      0,  # goal is reached without filling the board
    "filled":     0,  # goal is reached, board is filled

    "reached_empty":  -5,
    "reach_filled":  1000
}



""" Main ----------------------------------
        This is the main program's function
"""
def main(file):
    # create the game
    game = g.Game(file)
    for color in game.colors:
        res[color] = {
                "stuck":   0,  # no more moves are left
                "block":   0,  # if path blocks another path
                "reached": 0   # goal is reached
            }

    # create learning agent
    agent = q.Q_Learn_Agent(game, ALPHA, EPSILON, GAMMA, LAMBDA, rewards)

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
        res["filled"] += run_res["filled"]
        res["empty"] += run_res["empty"]

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
    #main(GAME_FILE)

    # Test files to use ----------- #
    FILES_1 = [  # 1 dot pair
        'levels/1/1_2x2.json',
        'levels/1/1_3x3.json'
    ]

    try:
        #        num_games,   files,      types,      iter_array, rewards, items,  prefix
        t.multiple_games(1, FILES_1, ["Q", "S"], [10, 10], rewards, items, "./test_results/test1_")
    except Exception as err:
        traceback.print_exc()
        print("Error testing for one pair.")
        exit(-1)
""" --------------------------- """
