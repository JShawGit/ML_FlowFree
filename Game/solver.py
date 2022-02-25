# external libraries
import pygame
import random
import numpy

# written programs
import global_vars as g
import game

""" Solver -------------------------------
        This is the program's RL solution.
"""
def solver(start_position, level_file):
    old_solver(start_position, level_file)
""" ------------------------------------ """



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #



""" Old Solver ----------------------------------
        This is an existing solver for reference.
"""
def old_solver(start_position, level_file):
    if (g.GAME_VARS["current_position"][0] == g.GAME_VARS["final_position"][0]
            and g.GAME_VARS["current_position"][1] == g.GAME_VARS["final_position"][1]):
        if g.GAME_VARS["solved_index"] < len(g.DOT_COLORS) - 1:
            g.GAME_VARS["solved_index"] += 1

        g.GAME_VARS["connected_colors"].append(g.GAME_VARS["actual_color"])
        actual_color = g.DOT_COLORS[g.GAME_VARS["solved_index"]]
        visited_cells = []
        g.GAME_VARS["backtrack_index"] = 0
        start_position = numpy.argwhere(g.GAME_VARS["grid_array"] == actual_color).tolist()[0]
        g.GAME_VARS["final_position"] = numpy.argwhere(g.GAME_VARS["grid_array"] == actual_color).tolist()[1]
        visited_cells.append(start_position)

        if len(g.GAME_VARS["connected_colors"]) == 5 and check_full_board():
            g.GAME_VARS["solve_value"] = 1
        elif len(g.GAME_VARS["connected_colors"]) == 5 and not check_full_board():
            game.load_level(level_file)
        return

    options = find_possible_options(g.GAME_VARS["current_position"])

    if len(options) != 0:
        option = random.choice(options)
        g.GAME_VARS["grid_array"][option[0]][option[1]] = g.GAME_VARS["actual_color"]
        pygame.draw.circle(g.GAME_WINDOW["grid_surface"], game.parse_color_from_json(g.GAME_VARS["actual_color"]),
                           (option[1] * 60 + 30, option[0] * 60 + 30), 25)
        g.GAME_VARS["bacltrack_index"] = 0

    else:
        if len(g.GAME_VARS["visited_cells"]) != 0:
            if g.GAME_VARS["current_position"] == start_position:
                game.load_level(level_file)
                g.GAME_VARS["tries"] += 1
                return

            g.GAME_VARS["grid_array"][g.GAME_VARS["current_position"][0]][g.GAME_VARS["current_position"][1]] = ""
            pygame.draw.circle(g.GAME_WINDOW["grid_surface"], g.GREY,
                               (g.GAME_VARS["current_position"][1] * 60 + 30, g.GAME_VARS["current_position"][0] * 60 + 30), 25)
            g.GAME_VARS["backtrack_index"] -= 1
            option = g.GAME_VARS["visited_cells"][g.GAME_VARS["backtrack_index"]]
        else:
            print("CANNOT SOLVE THAT LEVEL")
            return

    game.generate_fonts()
    pygame.display.flip()
    old_solver(option)
    return
""" ------------------------------------ """



""" Find Possible Options
        Old reference search algo.
"""
def find_possible_options(position):
    options = []

    # adding visited position to list

    if position not in g.GAME_VARS["visited_cells"]:
        g.GAME_VARS["visited_cells"].append(position)

    # x axis checking, yep indexes are swapped :(

    if 0 < position[1] < len(g.GAME_VARS["grid_array"]) - 1:
        if [position[0], position[1] + 1] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0], position[1] + 1] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] and g.GAME_VARS["final_position"][1] == position[1] + 1)):
            options.append([position[0], position[1] + 1])
        if [position[0], position[1] - 1] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0], position[1] - 1] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] and g.GAME_VARS["final_position"][1] == position[1] - 1)):
            options.append([position[0], position[1] - 1])

    elif position[1] == 0:
        if [position[0], position[1] + 1] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0], position[1] + 1] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] and g.GAME_VARS["final_position"][1] == position[1] + 1)):
            options.append([position[0], position[1] + 1])

    elif position[1] == len(g.GAME_VARS["grid_array"]) - 1:
        if [position[0], position[1] - 1] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0], position[1] - 1] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] and g.GAME_VARS["final_position"][1] == position[1] - 1)):
            options.append([position[0], position[1] - 1])

    # # y axis checking, yep indexes are swapped :(

    if 0 < position[0] < len(g.GAME_VARS["grid_array"]) - 1:
        if [position[0] + 1, position[1]] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0] + 1, position[1]] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] + 1 and g.GAME_VARS["final_position"][1] == position[1])):
            options.append([position[0] + 1, position[1]])
        if [position[0] - 1, position[1]] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0] - 1, position[1]] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] - 1 and g.GAME_VARS["final_position"][1] == position[1])):
            options.append([position[0] - 1, position[1]])

    elif position[0] == 0:
        if [position[0] + 1, position[1]] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0] + 1, position[1]] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] + 1 and g.GAME_VARS["final_position"][1] == position[1])):
            options.append([position[0] + 1, position[1]])

    elif position[0] == len(g.GAME_VARS["grid_array"]) - 1:
        if [position[0] - 1, position[1]] not in g.GAME_VARS["visited_cells"] \
                and (g.GAME_VARS["grid_array"][position[0] - 1, position[1]] == "" or (
                g.GAME_VARS["final_position"][0] == position[0] - 1 and g.GAME_VARS["final_position"][1] == position[1])):
            options.append([position[0] - 1, position[1]])

    return options
""" ------------------------------------ """



""" Check Full Board
        Old reference checks for full grid.
"""
def check_full_board() -> bool:
    for x in range(g.GRID_SIZE[0]):
        for y in range(g.GRID_SIZE[1]):
            if g.GAME_VARS["grid_array"][x][y] == "":
                return False
    return True
