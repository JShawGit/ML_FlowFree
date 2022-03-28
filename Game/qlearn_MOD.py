import numpy

from node import Node

import numpy as np
import random

DEBUG = True  # to print debug dialogue
""" Q Learning ----------------------------
        Will learn how to connect the dots.
"""


class Q_Learn_Agent:
    """ Initialize Agent ------------------------------------------------------------------------------------------- """

    def __init__(self, game, alpha, epsilon, gamma, llambda, rewards):
        global DEBUG
        self.game = game
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.llambda = llambda
        self.rewards = rewards

        self.grid_x = self.game.grid_size[0]  # grid x len
        self.grid_y = self.game.grid_size[1]  # grid y len

        # filled squares
        self.orig_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)
        self.all_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)
        self.current_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)

        # how many squares already filled
        self.orig_size = 0
        self.current_size = 0

        # square colors
        self.orig_colors = np.zeros((self.grid_x, self.grid_y), dtype=int)
        self.current_colors = np.zeros((self.grid_x, self.grid_y), dtype=int)
        self.colors = {
            "EMPTY": 0,
            "RED": 1,
            "YELLOW": 2,
            "GREEN": 3,
            "BLUE": 4
        }

        # path of nodes for current iteration
        self.node_paths = {
            "RED": [],
            "YELLOW": [],
            "GREEN": [],
            "BLUE": []
        }
        self.ends = {
            "RED": {"start": None, "end": None},
            "YELLOW": {"start": None, "end": None},
            "GREEN": {"start": None, "end": None},
            "BLUE": {"start": None, "end": None}
        }

        self.start_pos = self.game.start_position  # start grid tile
        self.final_pos = self.game.final_position  # goal grid tile

        # Q learning
        self.qtables = {
            "RED": {},
            "YELLOW": {},
            "GREEN": {},
            "BLUE": {}
        }
        self.etables = {
            "RED": {},
            "YELLOW": {},
            "GREEN": {},
            "BLUE": {}
        }

        # list of nodes to not fill
        self.start_nodes = []
        self.final_nodes = []

        self.grid_nodes = []  # store all grid-nodes here
        self.generate_nodes()  # get nodes
        self.generate_neighbors(False)  # get node-neighbors

        # get the start node
        self.start_node = [x for x in self.grid_nodes if x.is_start]
        self.start_node = self.start_node[0]

        # get the final node
        self.final_node = [x for x in self.grid_nodes if x.is_final]
        self.final_node = self.final_node[0]

    """ --- End Init --- """

    """ Reset Nodes ------------------------------------------------------------------------------------------------ """

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

    """ --- End Init --- """

    """ Generate Nodes --------------------------------------------------------------------------------------------- """

    def generate_nodes(self):
        # Clearing the Visited Cells
        self.game.visited_cells = []
        self.orig_size = 0

        # Looping through all the colors
        for color in self.game.colors:
            # Setting local object start/final positions
            self.start_pos = np.argwhere(self.game.grid_array == color).tolist()[0]
            self.final_pos = np.argwhere(self.game.grid_array == color).tolist()[1]
            self.orig_size += 1

            # for every square in the grid
            for x in range(self.grid_x):
                for y in range(self.grid_y):

                    # if start node
                    if [x, y] == self.start_pos:
                        self.grid_nodes.append(Node([x, y], True, False))
                        self.orig_colors[x][y] = self.colors[color]
                        self.orig_filled[x][y] = True
                        self.ends[color]["start"] = (x, y)
                        self.start_nodes.append(self.grid_nodes[-1])

                    # if goal node
                    elif [x, y] == self.final_pos:
                        self.grid_nodes.append(Node([x, y], False, True))
                        self.orig_colors[x][y] = self.colors[color]
                        self.orig_filled[x][y] = True
                        self.ends[color]["end"] = (x, y)
                        self.final_nodes.append(self.grid_nodes[-1])

                    # if empty node
                    else:
                        self.grid_nodes.append(Node([x, y], False, False))

        # Resetting local object start/final position to be with starting color
        self.start_pos = self.game.start_position
        self.final_pos = self.game.final_position

    """ --- End Gen Nodes --- """

    """ Generate Neighbors ----------------------------------------------------------------------------------------- """

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
                for color in self.game.colors:
                    self.qtables[color][(x, y)] = {}
                    self.etables[color][(x, y)] = {}

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
                        for color in self.game.colors:
                            self.qtables[color][(x, y)][(neighbor.position[0], neighbor.position[1])] = 0
                            self.etables[color][(x, y)][(neighbor.position[0], neighbor.position[1])] = 0

    """ --- End Gen Neighbors --- """

    """ Skip Neighbor ---------------------------------------------------------------------------------------------- """

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

    """ --- End Skip Neighbor --- """

    """ Iterate ---------------------------------------------------------------------------------------------------- """

    def iterate(self, learning):
        # Check to see if its the First Run
        if self.game.tries > 1:
            self.reset_nodes()

        # Increase greediness as we learn
        if learning:
            if (self.game.tries % 1000 == 0) and (self.epsilon >= 0):
                self.epsilon = self.epsilon - 0.01

        # reset filled squares
        self.current_filled = self.orig_filled.copy()
        self.current_colors = self.orig_colors.copy()

        # results to return
        return_vals = {}

        # node positions to start/end from
        starting_nodes = {}
        final_nodes = {}
        for color in self.game.colors:
            start_pos = np.argwhere(self.game.grid_array == color).tolist()[0]
            final_pos = np.argwhere(self.game.grid_array == color).tolist()[1]
            starting_nodes[color] = self.grid_nodes[start_pos[0] * self.grid_y + start_pos[1]]
            final_nodes[color] = self.grid_nodes[final_pos[0] * self.grid_y + final_pos[1]]

        # status of colors
        status = {}

        # prime node paths
        for color in self.game.colors:
            self.node_paths[color] = [starting_nodes[color]]
            status[color] = None

        # Start looping through colors
        col = random.sample(self.game.colors, len(self.game.colors))
        for color in col:

            # Reset node path and current color
            current_node = starting_nodes[color]
            self.game.current_color = color

            # prime return array
            return_vals[color] = {
                "stuck": 0,  # no more moves are left
                "block": 0,  # if path blocks another path
                "reached": 0  # goal is reached
            }

            # while not solved path
            while True:
                # flag for if path is blocking
                is_blocking = False

                # Get playable neighbors
                neighboring_nodes = np.copy(current_node.neighbors)
                for node in neighboring_nodes:
                    x, y = node.position
                    if node.position != final_nodes[color].position and self.current_filled[x][y]:
                        neighboring_nodes = np.delete(neighboring_nodes, np.where(neighboring_nodes == node))
                    for c in self.game.colors:
                        if c != color and (node == starting_nodes[c] or node == final_nodes[c]):
                            neighboring_nodes = np.delete(neighboring_nodes, np.where(neighboring_nodes == node))

                # if no playable actions, failure
                if len(neighboring_nodes) == 0:
                    if learning:
                        self.set_q_path("stuck", color)
                    return_vals[color]["stuck"] += 1
                    status[color] = "stuck"
                    break

                # if a neighbor node is the final node, always finish
                if final_nodes[color].position in [x.position for x in neighboring_nodes]:
                    next_node = final_nodes[color]
                    is_blocking = self.is_blocking(color, starting_nodes, final_nodes, status)
                    self.node_paths[color].append(next_node)

                # if not learning, get optimal node
                elif not learning:
                    next_node = self.find_optimal(current_node.position, neighboring_nodes, color)
                    self.node_paths[color].append(next_node)

                # else get random or optimal
                else:
                    # determine if greedy or exploratory
                    prob = random.random()

                    # get optimal node
                    if prob > self.epsilon:
                        next_node = self.find_optimal(current_node.position, neighboring_nodes, color)
                        self.node_paths[color].append(next_node)

                    # get random node
                    else:
                        next_node = random.choice(neighboring_nodes)
                        self.node_paths[color].append(next_node)

                # check if new node is blocking a path
                if not is_blocking and self.is_blocking(color, starting_nodes, final_nodes, status):
                    self.current_filled[next_node.position[0]][next_node.position[1]] = True
                    is_blocking = True
                    status[color] = "block"

                # check if the next node is the final node
                if next_node == final_nodes[color]:
                    self.current_filled[next_node.position[0]][next_node.position[1]] = True
                    if is_blocking:
                        res = ["block", "reached"]
                    else:
                        res = ["move", "reached"]
                        status[color] = "reached"
                    if learning:
                        self.set_q(current_node, next_node, res[0], color)
                        self.set_q_path(res[1], color)
                    return_vals[color][res[1]] += 1
                    break

                # else move to the next node
                else:
                    # move to next node
                    if learning and not is_blocking:
                        self.set_q(current_node, next_node, "move", color)
                    self.game.draw_dot(next_node.position[0], next_node.position[1], self.game.current_color)
                    self.current_filled[next_node.position[0]][next_node.position[1]] = True
                    self.current_colors[next_node.position[0]][next_node.position[1]] = self.colors[color]

                    # move on
                    current_node = next_node

        if self.is_filled():
            return_vals["filled"] = 1
            return_vals["empty"] = 0
            flag = "filled"
        else:
            return_vals["filled"] = 0
            return_vals["empty"] = 1
            flag = "empty"

        for color in self.game.colors:
            if status[color] == "reached" and flag == "filled":
                self.set_q_path(flag, color)
            else:
                self.set_q_path(flag, color)

        return return_vals

    """ --- End Iterate --- """

    """ Has Moves -------------------------------------------------------------------------------------------------- """

    def has_moves(self, node, color):
        no_move = 0
        n_neighbors = len(node.neighbors)
        nb = numpy.copy(node.neighbors)

        # see if all neighbors are filled
        for n in nb:
            [x, y] = n.position
            if self.current_filled[x][y]:
                no_move += 1
            elif (n.is_start or n.is_final) and self.game.grid_array[x][y] != color:
                no_move += 1

        # if all filled: fail
        if no_move >= n_neighbors:
            return False
        else:
            return True

    """ --- End Has Moves --- """

    """ Is Blocked ------------------------------------------------------------------------------------------------- """

    def is_blocked(self, new_node, check_color, final_nodes):
        path = self.node_paths[check_color]
        path_last = path[-1]
        grid = self.current_filled.copy()
        # this path is completed, no blockage
        if path_last.is_final:
            return False

        grid_up = [[0] * len(grid) for _ in range(len(grid))]

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j]:
                    grid_up[i][j] = 0
                else:
                    grid_up[i][j] = 3

        grid_up[path_last.position[0]][path_last.position[1]] = 1
        grid_up[final_nodes[check_color].position[0]][path_last.position[1]] = 2

        # Find number of unique paths in a matrix with obstacles.
        # code referenced from: geeksforgeeks.org/check-if-a-path-exists-from-start-to-end-cell-in-given-matrix-with-obstacles-in-at-most-k-moves/
        def canReach(grid, end_node):
            N = len(grid)

            # Method for finding and printing
            # whether the path exists or not
            def isPath(matrix, n):

                # Defining visited array to keep
                # track of already visited indexes
                visited = [[False for x in range(n)]
                           for y in range(n)]

                # Flag to indicate whether the
                # path exists or not
                flag = False

                for i in range(n):
                    for j in range(n):

                        # If matrix[i][j] is source
                        # and it is not visited
                        if (matrix[i][j] == 1 and not
                        visited[i][j]):

                            # Starting from i, j and
                            # then finding the path
                            if (checkPath(matrix, i,
                                          j, visited)):
                                # If path exists
                                flag = True
                                break
                return flag

            # Method for checking boundaries
            def isSafe(i, j, matrix):

                if (i >= 0 and i < len(matrix) and
                        j >= 0 and j < len(matrix[0])):
                    return True
                return False

            # Returns true if there is a
            # path from a source(a
            # cell with value 1) to a
            # destination(a cell with
            # value 2)
            def checkPath(matrix, i, j,
                          visited):

                # Checking the boundaries, walls and
                # whether the cell is unvisited
                if (isSafe(i, j, matrix) and
                        matrix[i][j] != 0 and not
                        visited[i][j]):

                    # Make the cell visited
                    visited[i][j] = True

                    # If the cell is the required
                    # destination then return true
                    if (matrix[i][j] == 2):
                        return True

                    # traverse up
                    up = checkPath(matrix, i - 1,
                                   j, visited)

                    # If path is found in up
                    # direction return true
                    if (up):
                        return True

                    # Traverse left
                    left = checkPath(matrix, i,
                                     j - 1, visited)

                    # If path is found in left
                    # direction return true
                    if (left):
                        return True

                    # Traverse down
                    down = checkPath(matrix, i + 1,
                                     j, visited)

                    # If path is found in down
                    # direction return true
                    if (down):
                        return True

                    # Traverse right
                    right = checkPath(matrix, i,
                                      j + 1, visited)

                    # If path is found in right
                    # direction return true
                    if (right):
                        return True

                # No path has been found
                return False

            return isPath(grid, N)

        return canReach(grid_up, final_nodes[check_color])

    """ --- End Is Blocked --- """

    """ Is Blocking ------------------------------------------------------------------------------------------------ """

    def is_blocking(self, in_color, starting_nodes, final_nodes, status):
        # get path of checked node, return if only starter node
        in_path = self.node_paths[in_color]
        in_last = in_path[-1]

        # not blocking if first/last node
        if in_last.is_final or in_last.is_start:
            return False

        # check other paths against node
        for color in self.game.colors:
            if in_color == color:
                continue

            # if skip
            stat = status[color]
            if stat is not None:
                return False

            # check if blocking this color
            if self.is_blocked(in_last, color, final_nodes):
                return True
        return False

    """ --- End Is Blocking --- """

    """ Is Filled -------------------------------------------------------------------------------------------------- """

    def is_filled(self):
        size = self.grid_x * self.grid_y
        true = 0
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if self.current_filled[x][y]:
                    true += 1
        return size == true

    """ --- End Is Filled --- """

    """ Reward Function -------------------------------------------------------------------------------------------- """

    def reward_function(self, reward):
        size = self.grid_x * self.grid_y
        # Finding How many Filled nodes
        fill = self.current_size
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                if self.current_filled[x][y]:
                    fill += 1

        ratio = float(fill / size)

        reward_val = self.rewards[reward]

        return reward_val * ratio

    """ --- End Is Filled --- """

    """ Get Temp Diff ---------------------------------------------------------------------------------------------- """

    def get_temp_diff(self, color, reward, cur_pos, next_pos, optimal_pos):
        return (  # r_t + gamma * argmax_a(Q(s_{t+1}, a)) - Q(s_t, a_t)
                reward +  # reward
                self.gamma *  # discount factor
                self.qtables[color][(cur_pos[0], cur_pos[1])][(optimal_pos[0], optimal_pos[1])] -  # optimal value
                self.qtables[color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]  # old value
        )

    """ --- End Get Temp Diff --- """

    """ Set Q ------------------------------------------------------------------------------------------------------ """

    def set_q(self, current_node, next_node, reward, current_color):
        """ https://en.wikipedia.org/wiki/Q-learning """

        # error check
        if current_color not in self.qtables:
            print('Error: color ' + current_color + " not valid!")
            return

        cur_pos = current_node.position  # current pos
        next_pos = next_node.position  # next pos

        # update eligibility
        self.etables[current_color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += 1

        # find optimal value, argmax_a(Q(s_{t+1}, a))
        optimal_pos = self.find_optimal(cur_pos, current_node.neighbors, current_color).position

        # handle if next node(s) don't exist
        if (next_pos[0], next_pos[1]) not in self.qtables[current_color][(cur_pos[0], cur_pos[1])]:
            return
        elif (optimal_pos[0], optimal_pos[1]) not in self.qtables[current_color][(cur_pos[0], cur_pos[1])]:
            return

        # temporal difference
        temp_diff = self.get_temp_diff(
            current_color,
            self.reward_function(reward),
            cur_pos,
            next_pos,
            optimal_pos
        )

        # set the new q value
        self.qtables[current_color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] += (
                self.alpha * temp_diff
                * self.etables[current_color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]
        )

        # set eligibility
        if cur_pos == optimal_pos:
            self.etables[current_color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] = (
                    self.gamma * self.etables[current_color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])]
            )
        else:
            self.etables[current_color][(cur_pos[0], cur_pos[1])][(next_pos[0], next_pos[1])] = 0

    """ --- End Set Q ---- """

    """ Set Q Path ------------------------------------------------------------------------------------------------- """

    def set_q_path(self, reward, current_color):

        # set new q-values for completed path
        for i in range(len(self.node_paths[current_color]) - 1):
            # nodes
            current_node = self.node_paths[current_color][i]
            next_node = self.node_paths[current_color][i + 1]

            # set q values
            self.set_q(current_node, next_node, reward, current_color)

    """ --- End Set Q Path --- """

    """ Find Optimal ----------------------------------------------------------------------------------------------- """

    def find_optimal(self, cur_pos, neighbors, current_color):

        # error check
        if current_color not in self.qtables:
            print('Error: color ' + current_color + " not valid!")
            return

        optimal = np.NINF
        optimal_node = None
        for neighbor in neighbors:
            neigh_pos = neighbor.position

            # Q-Table Selection
            q = self.qtables[current_color][(cur_pos[0], cur_pos[1])][(neigh_pos[0], neigh_pos[1])]

            # find max
            if q > optimal:
                optimal = q
                optimal_node = neighbor
            elif q == optimal:
                Rand_choices = [optimal_node, neighbor]
                optimal_node = random.choice(Rand_choices)

        return optimal_node

    """ --- End Find Optimal --- """
