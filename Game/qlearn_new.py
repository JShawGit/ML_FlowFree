import pygame
import numpy
import random
""" 
Q-Learning Algorithm
  This is an implementation of the Q-Learning algorithm
  to find a shortest path.
"""
class Node:

    # Initialize Node Class
    def __init__(self, current_position: (), start: (), final: ()):
        self.position = current_position
        self.neighbors = []
        # Is this final node
        self.final = final
        # Is this start node
        self.start = start
        # Actions available at node
        self.actions = []
        # Total reward associated with node
        self.r = 0

"""        
States: 
    Unconnected, not filled (UN)
    Connected, not filled   (CN)
    Connected, filled       (CF)

Actions:
    Left  (L)
    Right (R)
    Up    (U)
    Down  (D)
    
    
q_vale:
            L   R   U   D
    start |   |   |   |   |
    final |   |   |   |   |
    UN    |   |   |   |   |
    CN    |   |   |   |   |
"""


def Q_Learn(game):
    q_val = numpy.zeros([4, 4], dtype=int)

    grid_nodes = []
    # Generating nodes
    for x in range(game.grid_size[0]):
        for y in range(game.grid_size[1]):
            # Sorting if nodes are start or finish
            if [x, y] == game.start_position:
                grid_nodes.append(Node([x, y], True, False))
            elif [x, y] == game.final_position:
                grid_nodes.append(Node([x, y], False, True))
            else:
                grid_nodes.append(Node([x, y], False, False))

    # Generating neighbors
    for i in range(len(grid_nodes)):
        [x,y] = grid_nodes[i].position
        neighbor_states = [[x - 1, y,'L'], [x + 1, y,'R'], [x, y - 1,'U'], [x, y + 1,'D']]

        actions = [['L'], ['R'], ['U'], ['D']]
        for next_state in neighbor_states:

            if skip_neighbor(game,next_state[0:2]):
                continue
            else:
                neighbor_node = [z for z in grid_nodes if z.position == next_state[0:2]]
                neighbor_node = neighbor_node[0]
                grid_nodes[i].neighbors.append(neighbor_node)
                grid_nodes[i].actions.append(next_state[2])

    # Getting start Node
    start_node = [x for x in grid_nodes if x.start]
    start_node = start_node[0]

    # Getting Final Node
    final_node = [x for x in grid_nodes if x.final]
    final_node = final_node[0]

    switcher = {
        'L': 0,
        'R': 1,
        'U': 2,
        'D': 3
    }

    current_node = start_node
    for i in range(1000):
        if current_node.start:
            # Choosing random choice
            action = random.choice(current_node.actions)
            # Getting Index for which neighbor
            action_index = current_node.actions.index(action)
            #Changing current node to selected neighbor
            current_node = current_node.neighbors[action_index]
            # Getting index for Q-Table
            q_col_index = switcher.get(action, "nothing")

            # Added case for first selection is final node
            if current_node.final:
                q_val
        else:
            a =1


    a =1

def skip_neighbor(game,next_state):
    if next_state[0] > game.grid_size[0] - 1 or next_state[1] > game.grid_size[1] - 1 or next_state[0] < 0 or \
            next_state[1] < 0:
        return True
    else:
        return False