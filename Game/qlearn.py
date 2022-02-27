import numpy as np

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
        self.actions = ["L",  "R",  "U",  "D"]

        # every tile (minus the dots) will have 4 possible actions
        # each of these node-actions will have a q and r value
        self.qValues = np.zeros((
            self.game.grid_size[0] * self.game.grid_size[1] - len(self.game.colors)*2,
            len(self.actions)
        ))
        self.rValues = np.zeros((
            self.game.grid_size[0] * self.game.grid_size[1] - len(self.game.colors)*2,
            len(self.actions)
        ))

        # possible rewards
        self.rewards = {
            self.states[0]: -100,
            self.states[1]: -100,
            self.states[2]:  100,
            "move":            1
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
        while not np.array_equal(self.current_node, self.game.final_position):

            # while the nodes equal, randomly select next node
            next_state = self.current_state
            while np.array_equal(self.current_node, self.game.final_position):





""" ----------------------------------- """







