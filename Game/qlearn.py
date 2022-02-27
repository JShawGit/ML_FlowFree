import a_search as search
import numpy as np
import random

""" Q Learn ----------------------------
    This file contains the RL algorithm.
""" """

https://serengetitech.com/tech/using-q-learning-for-pathfinding/
https://towardsdatascience.com/q-learning-algorithm-from-explanation-to-implementation-cdbeda2ea187

[ R | - | - ]
[ - | - | - ]
[ R | - | - ]

States: 
    Unconnected, not filled (UN)
    Connected, not filled   (CN)
    Connected, filled       (CF)

Actions:
    Left  (L)
    Right (R)
    Up    (U)
    Down  (D)

"""

""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""
class Q_Learn_Agent():

    """ Initialize Agent ----------------------- """
    def __init__(self, game, alpha, epsilon, gamma):
        self.game    = game
        self.alpha   = alpha
        self.epsilon = epsilon
        self.gamma   = gamma

        # board state and possible tile actions
        self.states  = ["UN", "CN", "CF"]
        self.actions = ["L",  "R", # x
                        "U",  "D"  # y
                        ]

        # TODO: is this good?
        # every tile (minus the dots) will have 2-4 possible actions (edges)
        # each of these node-actions will have a q and r value
        # two nodes share every node-action
        x = self.game.grid_size[0]
        y = self.game.grid_size[1]
        self.num_nodes = x * y
        self.num_edges = x * (x-1) + y * (y-1)
        self.qValues = np.zeros((x * (x-1),  # x -
                                 y * (y-1)   # y |
                                 ))
        self.rValues = np.zeros((x * (x-1),  # x -
                                 y * (y-1)   # y |
                                 ))

        # possible rewards
        self.rewards = {
            self.states[0]: -100,
            self.states[1]: -100,
            self.states[2]:  100,
            "move":            1,
            "start":        -100
        }

        self.current_state = None
        self.current_node  = None
        self.current_color = ""

        self.backtrack_index  = 0
        self.solved_index     = 0
        self.solve_value      = 0
        self.tries            = 0



    """ Play Game """
    def play_game(self):
        self.current_state = self.states[0]           # starting state
        self.current_node  = self.game.start_position # starting position

        # while not reach the goal node
        res = search.a_search(self.game)
        print(str(res))



    # TODO: set reward (R) and Q values for each node-edge action
    def set_reward(self, current_node, next_node, reward):
        # TODO: uhm
        return



""" ----------------------------------- """







