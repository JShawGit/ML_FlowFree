import pygame
import random
import numpy

from global_vars import get_val
""" Solver ----------------------------------------
    This file contains the RL and original solvers.
    Solver code is taken from Github project:
    https://github.com/hreso110100/FlowFree-Solver
"""



""" Solve """
def solve(game, current_position):

    if current_position[0] == game.final_position[0] and current_position[1] == game.final_position[1]:
        if game.solved_index < len(game.colors) - 1:
            game.solved_index += 1

        game.connected_colors.append(game.current_color)
        game.current_color = game.colors[game.solved_index]
        game.visited_cells = []
        game.backtrack_index = 0
        game.start_position = numpy.argwhere(game.grid_array == game.current_color).tolist()[0]
        game.final_position = numpy.argwhere(game.grid_array == game.current_color).tolist()[1]
        game.visited_cells.append(game.start_position)

        if len(game.connected_colors) == 5 and check_full_board(game):
            game.solve_value = 1
        elif len(game.connected_colors) == 5 and not check_full_board(game):
            game.load_level()

        return

    options = find_possible_options(game, current_position)

    if len(options) != 0:
        option = random.choice(options)
        game.grid_array[option[0]][option[1]] = game.current_color
        pygame.draw.circle(game.grid_surface, game.parse_color_from_json(game.current_color),
                           (option[1] * 60 + 30, option[0] * 60 + 30), 25)
        game.backtrack_index = 0
    else:
        if len(game.visited_cells) != 0:
            if current_position == game.start_position:
                game.load_level(game.file)
                game.tries += 1
                return

            game.grid_array[current_position[0]][current_position[1]] = ""
            pygame.draw.circle(game.grid_surface, get_val("grey"),
                               (current_position[1] * 60 + 30, current_position[0] * 60 + 30), 25)
            game.backtrack_index -= 1
            option = game.visited_cells[game.backtrack_index]
        else:
            print("CANNOT SOLVE THAT LEVEL")
            return
    game.generate_fonts()
    pygame.display.flip()
    solve(game, option)
    return
""" ------------------ """



""" Check Full Board """
def check_full_board(game) -> bool:
    for x in range(game.grid_size[0]):
        for y in range(game.grid_size[1]):
            if game.grid_array[x][y] == "":
                return False
    return True
""" ---------------- """



""" Find Possible Options """
def find_possible_options(game, position):
    options = []

    # adding visited position to list

    if position not in game.visited_cells:
        game.visited_cells.append(position)

    # x axis checking, yep indexes are swapped :(

    if 0 < position[1] < len(game.grid_array) - 1:
        if [position[0], position[1] + 1] not in game.visited_cells \
                and (game.grid_array[position[0], position[1] + 1] == "" or (
                game.final_position[0] == position[0] and game.final_position[1] == position[1] + 1)):
            options.append([position[0], position[1] + 1])
        if [position[0], position[1] - 1] not in game.visited_cells \
                and (game.grid_array[position[0], position[1] - 1] == "" or (
                game.final_position[0] == position[0] and game.final_position[1] == position[1] - 1)):
            options.append([position[0], position[1] - 1])

    elif position[1] == 0:
        if [position[0], position[1] + 1] not in game.visited_cells \
                and (game.grid_array[position[0], position[1] + 1] == "" or (
                game.final_position[0] == position[0] and game.final_position[1] == position[1] + 1)):
            options.append([position[0], position[1] + 1])

    elif position[1] == len(game.grid_array) - 1:
        if [position[0], position[1] - 1] not in game.visited_cells \
                and (game.grid_array[position[0], position[1] - 1] == "" or (
                game.final_position[0] == position[0] and game.final_position[1] == position[1] - 1)):
            options.append([position[0], position[1] - 1])

    # # y axis checking, yep indexes are swapped :(

    if 0 < position[0] < len(game.grid_array) - 1:
        if [position[0] + 1, position[1]] not in game.visited_cells \
                and (game.grid_array[position[0] + 1, position[1]] == "" or (
                game.final_position[0] == position[0] + 1 and game.final_position[1] == position[1])):
            options.append([position[0] + 1, position[1]])
        if [position[0] - 1, position[1]] not in game.visited_cells \
                and (game.grid_array[position[0] - 1, position[1]] == "" or (
                game.final_position[0] == position[0] - 1 and game.final_position[1] == position[1])):
            options.append([position[0] - 1, position[1]])

    elif position[0] == 0:
        if [position[0] + 1, position[1]] not in game.visited_cells \
                and (game.grid_array[position[0] + 1, position[1]] == "" or (
                game.final_position[0] == position[0] + 1 and game.final_position[1] == position[1])):
            options.append([position[0] + 1, position[1]])

    elif position[0] == len(game.grid_array) - 1:
        if [position[0] - 1, position[1]] not in game.visited_cells \
                and (game.grid_array[position[0] - 1, position[1]] == "" or (
                game.final_position[0] == position[0] - 1 and game.final_position[1] == position[1])):
            options.append([position[0] - 1, position[1]])

    return options
""" --------------------- """
