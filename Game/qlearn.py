from node import Node

import numpy as np
import random

DEBUG = True  # to print debug dialogue
""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""
class Q_Learn_Agent:
    """ Initialize Agent ----------------------- """
    def __init__(self, game, alpha, epsilon, gamma, rewards):
        global DEBUG
        self.game = game
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.rewards = rewards

        self.grid_x = self.game.grid_size[0]  # grid x len
        self.grid_y = self.game.grid_size[1]  # grid y len

        # filled squares
        self.orig_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)
        self.current_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)

        # path of nodes for current iteration
        self.node_path = []

        self.start_pos = self.game.start_position  # start grid tile
        self.final_pos = self.game.final_position  # goal grid tile

        # Q learning
        self.qtable_red = {}  # a state-action dictionary
        self.qtable_blue = {}  # a state-action dictionary
        self.qtable_green = {}  # a state-action dictionary
        self.qtable_yellow = {}  # a state-action dictionary

        self.grid_nodes = []  # store all grid-nodes here
        self.generate_nodes()  # get nodes
        self.generate_neighbors(False)  # get node-neighbors

        # get the start node
        self.start_node = [x for x in self.grid_nodes if x.is_start]
        self.start_node = self.start_node[0]

        # get the final node
        self.final_node = [x for x in self.grid_nodes if x.is_final]
        self.final_node = self.final_node[0]
    """ --- End Init ------------------------------ """



    """ Reset Nodes -- """
    def reset_nodes(self):
        self.grid_nodes = []  # store all grid-nodes here
        self.generate_nodes()  # get nodes
        self.generate_neighbors(True)  # get node-neighbors

        # get the start node
        self.start_node = [x for x in self.grid_nodes if x.is_start]
        self.start_node = self.start_node[0]

        # get the final node
        self.final_node = [x for x in self.grid_nodes if x.is_final]
        self.final_node = self.final_node[0]
    """ --- End Init ------------------------------ """



    """ Generate Nodes -- """
    def generate_nodes(self):

        # Clearing the Visited Cells
        self.game.visited_cells = []

        # Looping through all the colors
        for color in self.game.colors:
            # Setting local object start/final positions
            self.start_pos = np.argwhere(self.game.grid_array == color).tolist()[0]
            self.final_pos = np.argwhere(self.game.grid_array == color).tolist()[1]
            self.game.visited_cells.append(self.start_pos)

            # for every square in the grid
            for x in range(self.grid_x):
                for y in range(self.grid_y):

                    # if start node
                    if [x, y] == self.start_pos:
                        self.grid_nodes.append(Node([x, y], True, False))
                        self.orig_filled[x][y] = True
                        self.current_filled[x][y] = True

                    # if goal node
                    elif [x, y] == self.final_pos:
                        self.grid_nodes.append(Node([x, y], False, True))
                        self.orig_filled[x][y] = True
                        self.current_filled[x][y] = True

                    # if empty node
                    else:
                        self.grid_nodes.append(Node([x, y], False, False))

        # Resetting local object start/final position to be with starting color
        self.start_pos = self.game.start_position
        self.final_pos = self.game.final_position
    """ --- End Gen Nodes --------------- """



    """ Generate Neighbors -- """
    def generate_neighbors(self, re_init):

        # for every node, get neighbors
        for i in range(len(self.grid_nodes)):

            # get position of self and neighbors
            [x, y] = self.grid_nodes[i].position
            neighbor_nodes = [
                [x - 1, y, 'L'],  # left
                [x + 1, y, 'R'],  # right
                [x, y - 1, 'U'],  # up
                [x, y + 1, 'D']  # down
            ]

            # append node to q-val table
            if not re_init:
                self.qtable_red[(x, y)] = {}
                self.qtable_blue[(x, y)] = {}
                self.qtable_green[(x, y)] = {}
                self.qtable_yellow[(x, y)] = {}

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

                    # append state-action to Q-table
                    if not re_init:
                        self.qtable_red[(x, y)][(neighbor.position[0], neighbor.position[1])] = 0
                        self.qtable_blue[(x, y)][(neighbor.position[0], neighbor.position[1])] = 0
                        self.qtable_green[(x, y)][(neighbor.position[0], neighbor.position[1])] = 0
                        self.qtable_yellow[(x, y)][(neighbor.position[0], neighbor.position[1])] = 0
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



    """ Iterate ------------------- """
    def iterate(self, learning):

        # Check to see if its the First Run
        if self.game.tries > 1:
            self.reset_nodes()

        # Get current node
        current_node = self.start_node  # starting node

        # Increase Greedyness as we learn
        if learning:
            if (self.game.tries % 1000 == 0) and (self.epsilon >= 0):
                self.epsilon = self.epsilon - 0.1

        # reset filled squares
        self.current_filled = self.orig_filled.copy()

        # Start looping through colors
        return_vals = {}
        for color in self.game.colors:

            # prime return array
            return_vals[color] = {
                "stuck":   0,         # no more moves are left
                "block":   0,         # if path blocks another path
                "reached_filled": 0,  # goal is reached
                "reached_empty": 0    # goal is reached
            }

            # Reset node path
            self.node_path = [current_node]

            # Changing Current Color and starting/ending positions
            # self.game.solved_index = self.game.solved_index + 1
            self.game.current_color = color
            self.start_pos = np.argwhere(self.game.grid_array == color).tolist()[0]
            self.final_pos = np.argwhere(self.game.grid_array == color).tolist()[1]

            # while not solved path
            while True:
                # get all playable actions (open nodes)
                neighboring_nodes = np.copy(current_node.neighbors)

                for node in neighboring_nodes:
                    x, y = node.position
                    if (node.position != self.final_pos) and self.current_filled[x][y]:
                        neighboring_nodes = np.delete(neighboring_nodes, np.where(neighboring_nodes == node))

                # if no playable actions, failure
                if len(neighboring_nodes) == 0:
                    self.set_q_path("stuck", color)
                    return_vals[color]["stuck"] += 1
                    break

                # determine if greedy or exploratory
                prob = random.random()

                # get random node
                if learning or prob <= self.epsilon:
                    next_node = random.choice(neighboring_nodes)
                    self.node_path.append(next_node)

                # get optimal node
                elif prob > self.epsilon:
                    next_node = self.find_optimal(current_node.position, neighboring_nodes, color)
                    self.node_path.append(next_node)

                # check if goal is reached
                if next_node == self.final_node:
                    self.current_filled[next_node.position[0]][next_node.position[1]] = True
                    if self.is_filled():
                        if learning:
                            self.set_q(current_node, next_node, "move", color)
                            self.set_q_path("reached_filled", color)
                        return_vals[color]["reached_filled"] += 1
                        break
                    else:
                        if learning:
                            self.set_q_path("reached_empty", color)
                        return_vals[color]["reached_empty"] += 1
                        break
                else:
                    if learning:
                        self.set_q(current_node, next_node, "move", color)
                    self.game.draw_dot(next_node.position[0], next_node.position[1], self.game.current_color)
                    self.current_filled[next_node.position[0]][next_node.position[1]] = True
                    current_node = next_node

            self.start_node.is_start = False
            self.final_node.is_final = False

            # get the start node
            self.start_node = [x for x in self.grid_nodes if x.is_start]

            # Checking to See if we are out of colors
            if self.start_node:
                self.start_node = self.start_node[0]
                current_node = self.start_node

            # get the final node
            self.final_node = [x for x in self.grid_nodes if x.is_final]

            # Checking to See if we are out of colors
            if self.final_node:
                self.final_node = self.final_node[0]

            # reset filled squares
            self.current_filled = self.orig_filled.copy()

        return return_vals
    """ --- End Iterate ----------- """



    """ Has Moves -------- """
    def has_moves(self, node):
        no_move = 0
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
    """ End Has Moves ------------------- - """



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
        ratio = float(fill / size)

        reward_val = self.rewards[reward]

        return reward_val * ratio
    """ --- End Is Filled --------------- """



    """ Set Q ------------------------------------ """
    def set_q(self, current_node, next_node, reward, current_color):
        """ https://en.wikipedia.org/wiki/Q-learning """
        cur_pos = current_node.position  # current pos
        next_pos = next_node.position  # next pos
        r = self.reward_function(reward)  # reward

        # find optimal value, argmax_a(Q(s_{t+1}, a))
        optimal_pos = self.find_optimal(cur_pos, current_node.neighbors, current_color).position

        if current_color == 'RED':
            # temporal difference
            temp_diff = (
                    r +  # reward
                    self.gamma *  # discount factor
                    self.qtable_red[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                    self.qtable_red[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
            )

            # set the new q value
            self.qtable_red[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

        elif current_color == 'BLUE':
            # temporal difference
            temp_diff = (
                    r +  # reward
                    self.gamma *  # discount factor
                    self.qtable_blue[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                    self.qtable_blue[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
            )

            # set the new q value
            self.qtable_blue[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

        elif current_color == 'GREEN':
            # temporal difference
            temp_diff = (
                    r +  # reward
                    self.gamma *  # discount factor
                    self.qtable_green[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                    self.qtable_green[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
            )

            # set the new q value
            self.qtable_green[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

        elif current_color == 'YELLOW':
            # temporal difference
            temp_diff = (
                    r +  # reward
                    self.gamma *  # discount factor
                    self.qtable_yellow[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                    self.qtable_yellow[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
            )

            # set the new q value
            self.qtable_yellow[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

        else:
            print('===== Error in Qtable Set========')
    """ --- End Set Q ----- """



    """ Set Q Path ----------------------------------- """
    def set_q_path(self, reward, current_color):
        # set new q-values for completed path
        for i in range(len(self.node_path) - 1):
            # nodes
            current_node = self.node_path[i]
            next_node = self.node_path[i + 1]

            # positions
            cur_pos = current_node.position
            next_pos = next_node.position

            # reward
            r = self.reward_function(reward)

            # find optimal value, argmax_a(Q(s_{t+1}, a))
            optimal_pos = self.find_optimal(cur_pos, current_node.neighbors, current_color).position

            # temporal difference
            if current_color == 'RED':
                # temporal difference
                temp_diff = (
                        r +  # reward
                        self.gamma *  # discount factor
                        self.qtable_red[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                        self.qtable_red[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
                )

                # set the new q value
                self.qtable_red[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

            elif current_color == 'BLUE':
                # temporal difference
                temp_diff = (
                        r +  # reward
                        self.gamma *  # discount factor
                        self.qtable_blue[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                        self.qtable_blue[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
                )

                # set the new q value
                self.qtable_blue[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

            elif current_color == 'GREEN':
                # temporal difference
                temp_diff = (
                        r +  # reward
                        self.gamma *  # discount factor
                        self.qtable_green[(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                        self.qtable_green[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
                )

                # set the new q value
                self.qtable_green[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

            elif current_color == 'YELLOW':
                # temporal difference
                temp_diff = (
                        r +  # reward
                        self.gamma *  # discount factor
                        self.qtable_yellow[(cur_pos[0], cur_pos[1])][
                            (optimal_pos[0], optimal_pos[1])] -  # optimal value
                        self.qtable_yellow[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
                )

                # set the new q value
                self.qtable_yellow[(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += self.alpha * temp_diff

            else:
                print('===== Error in Qtable Path ========')
    """ --- End Set Q ----- """



    """ Find Optimal ----------------------- """
    def find_optimal(self, cur_pos, neighbors, current_color):
        optimal = np.NINF
        optimal_node = None
        for neighbor in neighbors:
            neigh_pos = neighbor.position

            # Q-Table Selection
            if current_color == 'RED':
                q = self.qtable_red[(cur_pos[0], cur_pos[1])][(neigh_pos[0], neigh_pos[1])]
            elif current_color == 'BLUE':
                q = self.qtable_blue[(cur_pos[0], cur_pos[1])][(neigh_pos[0], neigh_pos[1])]
            elif current_color == 'GREEN':
                q = self.qtable_green[(cur_pos[0], cur_pos[1])][(neigh_pos[0], neigh_pos[1])]
            elif current_color == 'YELLOW':
                q = self.qtable_yellow[(cur_pos[0], cur_pos[1])][(neigh_pos[0], neigh_pos[1])]
            else:
                print('============ Error in find Optimal =========')



            # find max
            if q > optimal:
                optimal = q
                optimal_node = neighbor
            elif q == optimal:
                Rand_choices = [optimal_node, neighbor]
                optimal_node = random.choice(Rand_choices)


        return optimal_node
    """ --- End Find Optimal ---------------- """



""" --- End Q Learning Agent ----------------------------------------------------- """
