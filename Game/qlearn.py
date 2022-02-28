import a_search as search
import numpy as np
import random

DEBUG = False  # to print debug dialogue

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
    def __init__(self, game, alpha, epsilon, gamma, loops):
        self.game    = game
        self.alpha   = alpha
        self.epsilon = epsilon
        self.gamma   = gamma

        self.learning_loops = loops  # how many times to learn

        self.grid_x = self.game.grid_size[0]  # grid x len
        self.grid_y = self.game.grid_size[1]  # grid y len

        # filled squares
        self.orig_filled    = np.zeros((self.grid_x, self.grid_y), dtype=bool)
        self.current_filled = np.zeros((self.grid_x, self.grid_y), dtype=bool)

        # path of nodes for current iteration
        self.node_path = []

        self.start_pos = self.game.start_position  # start grid tile
        self.final_pos = self.game.final_position  # goal grid tile

        self.grid_nodes = []       # store all grid-nodes here
        self.generate_nodes()      # get nodes
        self.generate_neighbors()  # get node-neighbors

        # get the start node
        self.start_node = [x for x in self.grid_nodes if x.is_start]
        self.start_node = self.start_node[0]

        # get the final node
        self.final_node = [x for x in self.grid_nodes if x.is_final]
        self.final_node = self.final_node[0]

        # switcher for path finding
        self.switcher = {
            'L': 0,
            'R': 1,
            'U': 2,
            'D': 3
        }

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



    """ Learning Algo -- """
    def learning_algo(self):
        # starting node
        current_node = self.start_node
        self.node_path = [current_node]

        # reset filled squares
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                self.current_filled[x][y] = self.orig_filled[x][y]

        # while not solved path
        while True:
            # if no more paths
            if not self.has_moves(current_node):
                if False:
                    print("Ran out of moves!")
                    self.update_r(False)
                return

            # find a not-filled node
            while True:

                if self.game.tries % 10 == 0:
                    self.epsilon = self.epsilon - 0.001

                if np.random.uniform(0, 1) < np.exp(self.gamma - 1):
                    action = random.choice(current_node.actions)  # get a random action
                    action_index = current_node.actions.index(action)  # get neighbor index from action
                    next_node = current_node.neighbors[action_index]  # set neighbor as temp node
                else:
                    action = max(current_node.edges['r'])
                    action_index = current_node.edges['r'].index(action)
                    next_node = current_node.neighbors[action_index]

                # if the new node is the goal, success!
                if next_node.is_final:
                    if False:
                        print("Reached the final node!\n")
                    self.node_path.append(next_node)

                    # update q and r values and return
                    self.update_q(current_node, next_node)
                    if len(self.node_path) == (len(self.grid_nodes)):
                        self.update_r(True)
                    else:
                        self.update_r(False)
                    return

                # see if this position is filled
                [x, y] = next_node.position
                if not self.current_filled[x][y]:
                    if False:
                        print(action + ": " + str(current_node.position) + " --> " + str(next_node.position))

                    # update q value
                    self.update_q(current_node, next_node)

                    # set new node and draw it in
                    self.node_path.append(next_node)
                    current_node = next_node
                    self.game.draw_dot(
                        x,
                        y,
                        self.game.current_color
                    )
                    self.current_filled[x][y] = True
                    break
    """ --- End Learning Algo ----------- """



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
    """ --- End Has Moves --------------- """


    """ Get R -- """
    def get_r(self, current_node, next_node):
        # return r val of edge from current to next node
        index = current_node.neighbors.index(next_node)
        return current_node.edges["r"][index]
    """ --- End Get R ----- """


    """ Get Q -- """
    def get_q(self, current_node, next_node):
        # we should skip the current node index
        index = next_node.neighbors.index(current_node)

        # get the max q values
        maxq = [-1]
        maxi = [-1]
        q_vals = next_node.edges["q"]
        for i in range(len(q_vals)):
            # skip current node
            if i == index:
                continue

            # find max q values
            else:
                if q_vals[i] > maxq[0]:
                    maxq = [q_vals[i]]
                    maxi = [i]
                elif q_vals[i] == maxq[0]:
                    maxq.append(q_vals[i])
                    maxi.append(i)

        # return a random maximum index
        return random.choice(maxi)
    """ --- End Get Q ----- """



    """ Update Q --------------------------- """
    def update_q(self, current_node, next_node):
        """
        Q(current_node, next_node) =
        R(current_node, next_node) + Gamma * Max[Q(next_node, edges from next node)]
        """

        # computed values
        r       = self.get_r(current_node, next_node)
        q_index = self.get_q(current_node, next_node)

        # new q value
        q = r + self.gamma * next_node.edges["q"][q_index]

        # get array indices
        current_index = next_node.neighbors.index(current_node)
        next_index    = current_node.neighbors.index(next_node)

        # update the edge q-val for BOTH nodes! (as they are the same edge)
        current_node.edges["q"][next_index] = q
        next_node.edges["q"][current_index] = q
    """ --- End Update Q --------------------------------- """



    """ Update R --------------------------- """
    def update_r(self, is_success):
        if is_success:
            reward = 10
        else:
            reward = -1

        # for every move, give reward
        for i in range(len(self.node_path)):
            # get nodes
            current_node = self.node_path[i]
            if current_node.is_final:
                break
            else:
                next_node = self.node_path[i+1]

            # get array indices
            current_index = next_node.neighbors.index(current_node)
            next_index    = current_node.neighbors.index(next_node)

            # add reward
            current_node.edges["r"][next_index] += reward
            next_node.edges["r"][current_index] += reward

            #self.update_q(current_node, next_node)

    """ --- Update R --------------------------------- """



    """ Best Result -- """
    def best_result(self):
        # starting node
        current_node = self.start_node

        # reset filled squares
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                self.current_filled[x][y] = self.orig_filled[x][y]

        # while not solved path
        while True:

            # get node with the maximum q value
            qvals  = current_node.edges["q"].copy()

            # if no more paths
            if not self.has_moves(current_node):
                if DEBUG:
                    print("Ran out of moves!")
                return

            print(qvals)
            bestq  = max(qvals)
            indexq = qvals.index(bestq)
            next_node = current_node.neighbors[indexq]

            # if the new node is the goal, success!
            if next_node.is_final:
                if DEBUG:
                    print("Reached the final node!\n")
                return

            # see if this position is filled
            [x, y] = next_node.position
            while self.current_filled[x][y]:

                # remove filled value, check if no more moves
                qvals.pop(indexq)
                if len(qvals) == 0:
                    if DEBUG:
                        print("Ran out of moves!")
                    return

                # else set new next node
                bestq  = max(qvals)
                indexq = qvals.index(bestq)
                next_node = current_node.neighbors[indexq]
                [x, y] = next_node.position

                # if the new node is the goal, success!
                if next_node.is_final:
                    if DEBUG:
                        print("Reached the final node!\n")
                    return

            # set new node and draw it in
            current_node = next_node
            self.game.draw_dot(
                x,
                y,
                self.game.current_color
            )
            self.current_filled[x][y] = True
    """ -------------- """

""" --- End Q Learning Agent ----------------------------------------------------- """