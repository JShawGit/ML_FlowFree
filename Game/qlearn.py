import numpy as np
import random
import sys

DEBUG = True  # to print debug dialogue

""" Q Learn ----------------------------
    This file contains the RL algorithm.
""" """

https://serengetitech.com/tech/using-q-learning-for-pathfinding/
https://towardsdatascience.com/q-learning-algorithm-from-explanation-to-implementation-cdbeda2ea187

https://towardsdatascience.com/implement-grid-world-with-q-learning-51151747b455

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

        self.edges = {  # edges leading from/to neighbors
            "q": [],
            "r": []
        }

        self.is_start  = start   # if is starting node
        self.is_final  = final   # if is final, goal node

        self.actions = []  # actions available at node
        self.r       = 0   # node reward

""" --- End Node --------------------------------------- """



""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""
class Q_Learn_Agent:

    """ Initialize Agent ----------------------- """
    def __init__(self, game, alpha, epsilon, gamma, rewards):
        global DEBUG
        self.game    = game
        self.alpha   = alpha
        self.epsilon = epsilon
        self.gamma   = gamma
        self.rewards = rewards

        self.grid_x = self.game.grid_size[0]  # grid x len
        self.grid_y = self.game.grid_size[1]  # grid y len

        # filled squares
        self.orig_filled    = np.zeros((self.grid_x, self.grid_y), dtype=bool)
        self.current_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)

        # path of nodes for current iteration
        self.node_path = []

        self.start_pos = self.game.start_position  # start grid tile
        self.final_pos = self.game.final_position  # goal grid tile

        # Q learning
        self.qtable = {}  # a state-action dictionary

        self.grid_nodes = []       # store all grid-nodes here
        self.generate_nodes()      # get nodes
        self.generate_neighbors()  # get node-neighbors

        # get the start node
        self.start_node = [x for x in self.grid_nodes if x.is_start]
        self.start_node = self.start_node[0]

        # get the final node
        self.final_node = [x for x in self.grid_nodes if x.is_final]
        self.final_node = self.final_node[0]

    """ --- End Init ------------------------------ """



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
                    self.orig_filled[x][y]    = True
                    self.current_filled[x][y] = True

                # if empty node
                else:
                    self.grid_nodes.append(Node([x, y], False, False))
    """ --- End Gen Nodes --------------- """



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

            # append node to q-val table
            self.qtable[(x, y)] = {}

            # go over every neighbor
            for node in neighbor_nodes:

                # skip if out of range
                if self.skip_neighbor(node[0:2]):
                    continue

                # else accept neighbor
                else:
                    # get neighbor
                    neighbor = [z for z in self.grid_nodes if z.position == node[0:2]]
                    neighbor = neighbor[0]

                    # append neighbor and action
                    self.grid_nodes[i].neighbors.append(neighbor)
                    self.grid_nodes[i].actions.append(node[2])

                    # append edge values leading from node to neighbor
                    self.grid_nodes[i].edges["q"].append(1)
                    self.grid_nodes[i].edges["r"].append(0)

                    # append state-action to Q-table
                    self.qtable[(x, y)][(neighbor.position[0], neighbor.position[1])] = 0
    """ --- End Gen Neighbors ------------------- """



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
    """ --- End Skip Neighbor ------------------------- """



    """ Learning ------------------- """
    def learning(self):
        current_node = self.start_node  # starting node
        self.node_path = [current_node]  # keep a list of nodes in this path

        # reset filled squares
        self.current_filled = self.orig_filled.copy()

        # while not solved path
        while True:
            # get all playable actions (open nodes)
            neighboring_nodes = np.copy(current_node.neighbors)
            for node in neighboring_nodes:
                x, y = node.position
                if node != self.final_node and self.current_filled[x][y]:
                    neighboring_nodes = np.delete(neighboring_nodes, np.where(neighboring_nodes == node))

            # if no playable actions, failure
            if len(neighboring_nodes) == 0:
                if DEBUG:
                    print("Ran out of moves!")
                last_node = self.node_path[-2]
                #self.set_q(last_node, current_node, "move")
                self.set_q_path("stuck")
                return "stuck"

            # determine if greedy or exploratory
            prob = random.random()

            # get optimal node
            if prob > self.epsilon:
                next_node = self.find_optimal(current_node.position, neighboring_nodes)
                self.node_path.append(next_node)

            # get random node
            else:
                next_node = random.choice(neighboring_nodes)
                self.node_path.append(next_node)

            # check if goal is reached
            if next_node == self.final_node:
                self.current_filled[next_node.position[0]][next_node.position[1]] = True
                if self.is_filled():
                    print("Reached goal, filled!")
                    self.set_q(current_node, next_node, "move")
                    self.set_q_path("reached_filled")
                    return "reached_filled"
                else:
                    print("Reached goal, empty.")
                    #self.set_q(current_node, next_node, "move")
                    self.set_q_path("reached_empty")
                    return "reached_empty"
            else:
                self.set_q(current_node, next_node, "move")
                self.game.draw_dot(next_node.position[0], next_node.position[1], self.game.current_color)
                self.current_filled[next_node.position[0]][next_node.position[1]] = True
                current_node = next_node
    """ --- End Learning ----------- """



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




    """ Count Filled ------------------- - """
    def count_filled(self):
        size = 0
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if self.current_filled[x][y]:
                    size += 1
        return size
    """ --- End Is Filled --------------- """



    """ Is Filled ------------------- - """
    def is_filled(self):
        size = self.grid_x * self.grid_y
        return size == self.count_filled()
    """ --- End Is Filled --------------- """



    """ Reward Function ------------------- - """
    def reward_function(self, reward):
        size = self.grid_x * self.grid_y
        fill = self.count_filled()
        ratio = float(fill/size)

        reward_val = self.rewards[reward]

        return reward_val * ratio
    """ --- End Is Filled --------------- """



    """ Set Q ------------------------------------ """
    def set_q(self, current_node, next_node, reward):
        """ https://en.wikipedia.org/wiki/Q-learning """
        cur_pos  = current_node.position      # current pos
        next_pos = next_node.position         # next pos
        r = self.reward_function(reward)      # reward

        # find optimal value, argmax_a(Q(s_{t+1}, a))
        optimal_pos = self.find_optimal(cur_pos, current_node.neighbors).position

        # temporal difference
        temp_diff = (
                r +           # reward
                self.gamma *  # discount factor
                self.qtable[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                self.qtable[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]          # old value
        )

        # set the new q value
        self.qtable[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff
    """ --- End Set Q ----- """



    """ Set Q Path ----------------------------------- """
    def set_q_path(self, reward):
        # set new q-values for completed path
        for i in range(len(self.node_path)-1):
            # nodes
            current_node = self.node_path[i]
            next_node    = self.node_path[i+1]

            # positions
            cur_pos  = current_node.position
            next_pos = next_node.position

            # reward
            r = self.reward_function(reward)

            # find optimal value, argmax_a(Q(s_{t+1}, a))
            optimal_pos = self.find_optimal(cur_pos, current_node.neighbors).position

            # temporal difference
            temp_diff = (
                    r +           # reward
                    self.gamma *  # discount factor
                    self.qtable[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                    self.qtable[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]          # old value
            )

            # set the new q value
            self.qtable[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff
    """ --- End Set Q ----- """



    """ Find Optimal ----------------------- """
    def find_optimal(self, cur_pos, neighbors):
        optimal      = -sys.maxsize - 1
        optimal_node = None
        for neighbor in neighbors:
            neigh_pos = neighbor.position
            q = self.qtable[(cur_pos[0], cur_pos[1])][(neigh_pos[0], neigh_pos[1])]

            # find max
            if q > optimal:
                optimal = q
                optimal_node = neighbor

        return optimal_node
    """ --- End Find Optimal ---------------- """



    """ Optimal Game ------------ """
    def optimal_game(self):
        current_node = self.start_node   # starting node
        self.node_path = [current_node]  # keep a list of nodes in this path

        # reset filled squares
        self.current_filled = self.orig_filled.copy()

        # while not solved path
        while True:
            # get all playable actions (open nodes)
            neighboring_nodes = np.copy(current_node.neighbors)
            for node in neighboring_nodes:
                x, y = node.position
                if node != self.final_node and self.current_filled[x][y]:
                    neighboring_nodes = np.delete(neighboring_nodes, np.where(neighboring_nodes == node))

            # if no playable actions, failure
            if len(neighboring_nodes) == 0:
                if DEBUG:
                    print("Ran out of moves!")
                return "stuck"

            # get random next node
            next_node = self.find_optimal(current_node.position, neighboring_nodes)
            self.node_path.append(next_node)

            # check if goal is reached
            if next_node == self.final_node:
                self.current_filled[next_node.position[0]][next_node.position[1]] = True
                if self.is_filled():
                    print("Reached goal, filled!")
                    return "reached_filled"
                else:
                    print("Reached goal, empty.")
                    return "reached_empty"
            else:
                self.set_q(current_node, next_node, "move")
                self.game.draw_dot(next_node.position[0], next_node.position[1], self.game.current_color)
                self.current_filled[next_node.position[0]][next_node.position[1]] = True
                current_node = next_node
    """ -- End Optimal Game ------------ """

""" --- End Q Learning Agent ----------------------------------------------------- """