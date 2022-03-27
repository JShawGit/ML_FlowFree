
""" Node -----------------------------------------
        This is creates a node, which is each cell
        within a grid.
"""
class Node:
    """ Initialize Node --------------------------------------- """
    def __init__(self, pos, start, final):
        self.position  = pos  # search current position
        self.neighbors = []   # search neighbors

        self.is_start = start  # if is starting node
        self.is_final = final  # if is final, goal node

        self.actions = []  # actions available at node
""" --- End Node --------------------------------------- """
