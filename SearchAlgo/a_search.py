# TODO: create search algorithm
import numpy
import pygame
""" 
A* Search Algorithm
  This is an implementation of the A* search algorithm
  to find a shortest path.
"""


class Node:

    # Initialize Node Class
    def __init__(self, current_position: (), parent: ()):
        self.position = current_position
        self.parent = parent
        # Distance to start node
        self.g = 0
        # Distance to Goal Node
        self.h = 0
        # Total Cost
        self.f = 0

    # Compare Nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort Nodes
    #def __lt__(self, other):
    #    return self.f < other.f

    def getKey(obj):
        return obj.f


def a_search(game):
    # Open nodes and closed nodes
    open = []
    closed = []

    start_node = Node(game.start_position, None)
    final_node = Node(game.final_position, None)

    open.append(start_node)

    while len(open) > 0:
        # Check and see if grid is equal size
        if game.grid_size[0] == game.grid_size[1]:
            # Sort the open list
            open.sort(key=lambda x: x.h, reverse=True)
        else:
            open.sort(key=lambda x: x.f, reverse=True)

        # Get node with smallest cost
        current_node = open.pop()

        # Drawing on Grid
        draw_on_grid(game,current_node)


        # Add curent_node to closed list
        closed.append(current_node)

        if current_node.position[0] == final_node.position[0] \
                and current_node.position[1] == final_node.position[1]:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
                game.solve_value = 1
            # Return reversed path
            return path[::-1]

        (x, y) = current_node.position

        neighbor_states = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        for next_state in neighbor_states:
            # Check if next nodes are out of grid
            if next_state[0] > game.grid_size[0]-1 or next_state[1] > game.grid_size[1]-1 or next_state[0] < 0 or next_state[1] < 0:
                continue

            neighbor_state = Node(next_state, current_node)

            if neighbor_state in closed:
                continue

            # Heuristics Calculations
            heuristics(neighbor_state,start_node,final_node)

            # Checking if Neighbor state should be added to open
            if (open_add(neighbor_state,open,game) == True):
                open.append(neighbor_state)





    return None


def draw_on_grid(game, current_node):
    # Drawing on Grid
    game.grid_array[current_node.position[0]][current_node.position[1]] = game.current_color
    pygame.draw.circle(
        game.grid_surface,
        game.parse_color_from_json(game.current_color),
        (30 + current_node.position[0] * 60, 30 + current_node.position[1] * 60), 25)

    return None



def heuristics(neighbor_state,start_node,final_node):
    neighbor_state.g = abs(neighbor_state.position[0] - start_node.position[0]) + \
                       abs(neighbor_state.position[1] - start_node.position[1])
    # Manhatten Distance Calc
    neighbor_state.h = abs(neighbor_state.position[0] - final_node.position[0]) + \
                       abs(neighbor_state.position[1] - final_node.position[1])
    # Final Cost Value
    neighbor_state.f = neighbor_state.g + neighbor_state.h

    return None

def open_add(neighbor_state,open,game):
    if game.grid_size[0] == game.grid_size[1]:
        for node in open:
            if neighbor_state == node and neighbor_state.h >= node.h:
                return False
    else:
        for node in open:
            if neighbor_state == node and neighbor_state.f >= node.f:
                return False

    return True




# This executes if this file is the main executor
if __name__ == "__main__":
    a_search("TODO: code this!")
