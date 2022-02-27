import a_search as search
import numpy as np
import random

DEBUG = True  # to print debug dialogue

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



""" Node -----------------------------------------
        This is creates a node, which is each cell
        within a grid..
"""
class Node:

    """ Initialize Node --------------------------------------- """
    def __init__(self, pos, start, final):
        self.position  = pos  # search current position
        self.neighbors = []   # search neighbors

        self.is_start  = start   # if is starting node
        self.is_final  = final   # if is final, goal node

        self.actions = []  # actions available at node
        self.r       = 0   # node reward

""" ------------------------------------------ """



""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""
class Q_Learn_Agent:

    """ Initialize Agent ----------------------- """
    def __init__(self, game, alpha, epsilon, gamma):
        self.game    = game
        self.alpha   = alpha
        self.epsilon = epsilon
        self.gamma   = gamma

        self.grid_x = self.game.grid_size[0]  # grid x len
        self.grid_y = self.game.grid_size[1]  # grid y len

        # filled squares
        self.orig_filled    = np.zeros((self.grid_x, self.grid_y), dtype=bool)
        self.current_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)

        self.start_pos = self.game.start_position  # start grid tile
        self.final_pos = self.game.final_position  # goal grid tile

        self.q_values = []  # q-vals for each edge
        self.r_values = []  # r-vals for each edge

        self.grid_nodes = []       # store all grid-nodes here
        self.generate_nodes()      # get nodes
        self.generate_neighbors()  # get node-neighbors

        # get the start node
        self.start_node = [x for x in self.grid_nodes if x.is_start]
        self.start_node = self.start_node[0]

        # get the final node
        self.final_node = [x for x in self.grid_nodes if x.is_final]
        self.final_node = self.final_node[0]

        self.loop = 1000   # search tries
        self.switcher = {  # switcher for path finding
            'L': 0,
            'R': 1,
            'U': 2,
            'D': 3
        }

    """ ---------------------------------------- """



    """ Generate Nodes -- """
    def generate_nodes(self):
        # for every square in the grid
        for x in range(self.grid_x):
            for y in range(self.grid_y):

                # if start node
                if [x, y] == self.game.start_position:
                    self.grid_nodes.append(Node([x, y], True, False))
                    self.orig_filled[x][y]    = True
                    self.current_filled[x][y] = True

                # if goal node
                elif [x, y] == self.final_pos:
                    self.grid_nodes.append(Node([x, y], False, True))

                # if empty node
                else:
                    self.grid_nodes.append(Node([x, y], False, False))
    """ ------------------ """



    """ Generate Neighbors -- """
    def generate_neighbors(self):
        # for every node, get neighbors
        for i in range(len(self.grid_nodes)):

            # get position of self and neighbors
            [x, y] = self.grid_nodes[i].position
            neighbor_nodes = [
                [x - 1, y, 'L'],  # left
                [x + 1, y, 'R'],  # right
                [x, y - 1, 'U'],  # up
                [x, y + 1, 'D']   # down
            ]

            # go over every neighbor
            for node in neighbor_nodes:

                # skip if out of range
                if self.skip_neighbor(node[0:2]):
                    continue

                # else accept neighbor
                else:
                    neighbor = [z for z in self.grid_nodes if z.position == node[0:2]]
                    neighbor = neighbor[0]
                    self.grid_nodes[i].neighbors.append(neighbor)
                    self.grid_nodes[i].actions.append(node[2])

    """ ---------------------- """



    """ Skip Neighbor -------------- """
    def skip_neighbor(self, next_state):
        # skip if out of bounds
        if next_state[0] > self.grid_x - 1 \
                or next_state[1] > self.grid_y - 1 \
                or next_state[0] < 0 \
                or next_state[1] < 0:
            return True

        # don't skip
        else:
            return False
    """ ---------------------------- """



    """ Search Algo -- """
    def search_algo(self):
        # starting node
        current_node = self.start_node

        # reset filled squares
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                self.current_filled[x][y] = self.orig_filled[x][y]

        # for many tries
        for i in range(10):
            # if no more paths
            if not self.has_moves(current_node):
                if DEBUG:
                    print("Ran out of moves!")
                return

            # find a not-filled node
            while True:
                action = random.choice(current_node.actions)       # get a random action
                action_index = current_node.actions.index(action)  # get neighbor index from action
                next_node = current_node.neighbors[action_index]    # set neighbor as temp node

                # if the new node is the goal, success!
                if next_node.is_final:
                    if DEBUG:
                        print("Reached the final node!\n")
                    q_val = 0
                    return

                # see if this position is filled
                [x, y] = next_node.position
                if not self.current_filled[x][y]:
                    if DEBUG:
                        print(action + ": " + str(current_node.position) + " --> " + str(next_node.position))

                    # set new node and draw it in
                    current_node = next_node
                    self.game.draw_dot(
                        x,
                        y,
                        self.game.current_color
                    )
                    self.current_filled[x][y] = True
                    break


                q_col_index = self.switcher.get(action, "nothing")   # get index for Q-Table



        a = 1
    """ -------------- """



    """ Has Moves -------- """
    def has_moves(self, node):
        no_move     = 0
        n_neighbors = len(node.neighbors)

        # see if all neighbors are filled
        for n in node.neighbors:
            [x, y] = n.position
            if self.current_filled[x][y]:
                no_move += 1

        # if all filled: fail
        if no_move == n_neighbors:
            return False
        else:
            return True
    """ ------------------ """


""" ----------------------------------- """












"""
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

"""

   # """ Play Game """
"""
    def play_game(self):
        if self.game.grid_size[0] != 3:
            print("Can only solve with 3x3 grids!")
            return

        self.current_state = self.states[0]            # starting state
        self.current_node  = self.game.start_position  # starting position

        # while not reach the goal node
        search.a_search(self.game)



    # TODO: set reward (R) and Q values for each node-edge action
    def set_reward(self, current_node, next_node, reward):
        if current_node[0] != next_node[0]:
            self.rValues[0][]
        return



    # TODO: set Q value for each node-edge action
    def set_qval(self, current_node, next_node, val):
        # TODO: uhm
        return

"""

""" ----------------------------------- """







