import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
import threading
import traceback

import sarsalearn_MOD as s
import qlearn_MOD as q
import game as g

""" Init Game ----------------------------------------------------------------------------------------------------------
    Inits a game and results, returns them
    Takes in:
        A game file
"""
def init_game(file):
    game = g.Game(file)
    res = {
        "filled": 0,
        "empty": 0,
    }
    for color in game.colors:
        res[color] = {
            "stuck": 0,
            "block": 0,
            "reached": 0
        }
    return [game, res]
""" --- End Init Game --- """


""" Learn --------------------------------------------------------------------------------------------------------------
    Learn for num iterations given some agent
    
    Takes in:
        Iter: ex. 100
        Agent
        Res
"""
def learn(iterate, game, agent, res):
    try:
        for i in range(iterate):
            run_res = agent.iterate(True)
            for color in game.colors:
                for key in run_res[color]:
                    res[color][key] += run_res[color][key]
            res["filled"] += run_res["filled"]
            res["empty"]  += run_res["empty"]
        return res
    except:
        traceback.print_exc()
        print("Error learning.")
        exit(-1)
""" --- End Learn --- """


""" Run ----------------------------------------------------------------------------------------------------------------
    Runs the optimal path
    
    Takes in:
        Agent
"""
def run(agent):
    return agent.iterate(False)
""" --- End Learn --- """



""" Test One Game ------------------------------------------------------------------------------------------------------
    Test all test files in an array of file-paths.
    
    Takes in:
        File: file name for the game
        Types: an array, ex["S", "Q"]
        Iteration array: ex. [100, 100, 100] for 100 learning-passes 3 times
        Rewards: ex. stuck or filled
        Items: Alpha, Epsilon, Gamma, Lambda
"""
def test_one_game(file, types, iter_array, rewards, items):
    # play game for each file in the one-pair files
    res      = {}
    iter_res = {}
    run_res  = {}
    games    = {}
    agents   = {}

    # create agents and their games
    for type in types:
        run_res[type] = []
        tmp = init_game(file)
        games[type] = tmp[0]
        res[type]   = tmp[1]
        iter_res[type] = {
            "filled":  [],
            "empty":   [],
            "stuck":   [],
            "block":   [],
            "reached": []
        }
        if type == "Q":
            agents[type] = q.Q_Learn_Agent(games[type], items[0], items[1], items[2], items[3], rewards)
        else:
            agents[type] = s.Sarsa_Learn_Agent(games[type], items[0], items[1], items[2], items[3], rewards)

    # iterate through the learning-iterations
    # log the results for the optimal path after each iter
    for iterate in iter_array:
        for type in agents:
            l = learn(iterate, games[type], agents[type], res[type])
            r = run(agents[type])
            run_res[type].append(r.copy())
            for color in games[type].colors:
                for key in l[color]:
                    iter_res[type][key] += run_res[color][key]
        res["filled"] += run_res["filled"]
        res["empty"] += run_res["empty"]

    # return overall and optimal res
    return [res, run_res, iter_res]
""" --- End Test One Game --- """



""" Multiple Games -----------------------------------------------------------------------------------------------------
    Tests multiple games 
    
    Takes in:
        Num games: ex. 100
        Files: game files
        Type: ["Q", "S"]
        Iteration array: ex. [100, 100, 100]
        Rewards: ex. stuck or filled
        Items: Alpha, Epsilon, Gamma, Lambda
        Filename prefix: ex. "/results/test1_game1_"
"""
def multiple_games(num_games, files, types, iter_array, rewards, items, prefix):
    res      = {}
    run_res  = {}
    iter_res = {}

    # prepare results
    for file in files:
        run_res[file]  = {}
        res[file]      = {}
        iter_res[file] = {}
        for type in types:
            run_res[file][type]  = []
            res[file][type]      = []
            iter_res[file][type] = []
            for game in range(num_games):
                tmp = test_one_game(file, type, iter_array, rewards, items)
                for key in tmp[0]:
                    res[file][key].append(tmp[0][key])
                    run_res[file][key].append(tmp[1][key])
                    iter_res[file][key].append(tmp[2][key])

        plot_learning_curve(num_games, types, iter_array, res[file], run_res[file], iter_res[file], prefix, files, items)
""" --- End Multiple Games --- """



""" Plot Learning Curve ------------------------------------------------------------------------------------------------
    Plots learning curves for the given data.
    The learning curve will be the number of successes/stucks/etc after each iteration
"""
def plot_learning_curve(num_games, types, iter_array, res, run_res, iter_res, prefix, files, items):
    for type in types:
        for file in range(len(files)):
            x_vals = iter_array.copy()
            xy_vals = {
                "filled":  [],
                "empty":   [],
                "stuck":   [],
                "block":   [],
                "reached": []
            }

            # append values
            for i in range(len(iter_array)):
                for key in iter_res[type][file][i]:
                    if key in xy_vals:
                        xy_vals[key].append(iter_res[type][file][i][key][i])
                    else:
                        for subkey in iter_res[type][file][i][key]:
                            xy_vals[subkey].append(iter_res[type][file][i][key][subkey][i])

            # graph




""" --- End Plot Learning Curve --- """







"""
# print to file
for r in res:
    df_res = pd.DataFrame.from_dict([res[r]])
    df_res.to_csv(prefix + r + '_total_results.txt', header=False, index=True, mode='a')
    for i in range(len(iter_array)):
        df_run_res = pd.DataFrame.from_dict([run_res[r][i]])
        df_run_res.to_csv(prefix + r + '_' + str(i) + '_total_results.txt', header=False, index=True, mode='a')
"""













""" Test Runs
        Take in array of iterations, ex[100, 1000, 5000]
        Choose how many games to run over these runs
"""
def test_TF(num_games, iter_arr, game_file, a, e, g, l, img):

    games   = []  # games to run
    agents  = []  # all game-agents
    threads = []  # all agent-threads
    results = []  # results from testing

    """ iterate for a given agent """
    def iterate_agent(agent, tid):
        res = []                             # results will have an array for each test
        for val in range(len(iter_arr)):     # for each iteration-value
            for i in range(iter_arr[val]):   # iterate through value
                agent.learning_algo()        # learn for i iterations
            res.append(agent.best_result())  # append final result to res
        results[tid] = res

    # create a game and agent for every test-run
    for n in range(num_games):
        results.append(None)
        games.append(game.Game(game_file))
        agents.append(q.Q_Learn_Agent(games[n], a, e, g, l))
        threads.append(threading.Thread(target=iterate_agent, args=(agents[n], n,)))
        threads[n].start()

    # end threads
    for thread in threads:
        thread.join()

    # graph results
    graph_TF(results, iter_arr, img)



""" Graph TF 
    Reference: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
        Graphs results where it is:
        [col1, col2, col3]
     i1 [val1, val2, val3]
     i2 [      ...       ]
     ...
"""
def graph_TF(results, columns, img):

    x = columns
    y = [[], []]

    # get results for each iter test
    for i in range(len(x)):
        true  = 0
        false = 0

        # count trues and falses
        for res in results:
            if res[i]:
                true += 1
            else:
                false += 1

        # append true false values
        y[0].append(true)
        y[1].append(false)

    # set up plot bars
    width  = 0.3
    figure, axis = plt.subplots()
    ar     = np.arange(len(x))
    bar_t  = axis.bar(ar - width / 2, y[0], width, label='True')
    bar_f  = axis.bar(ar + width / 2, y[1], width, label='False')

    # set up plot axis
    axis.set_title('Successes Per Learning Iterations')
    axis.set_ylabel('Successful Attempts')
    axis.set_xlabel('Learning Iterations')
    axis.set_xticks(ar)
    axis.set_xticklabels(x)
    axis.legend()

    # add height label
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            axis.annotate(
                '{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center',
                va='bottom'
            )

    autolabel(bar_t)
    autolabel(bar_f)
    figure.tight_layout()
    plt.savefig(img)




""" Test Lengths
        Take in array of iterations, ex[100, 1000, 5000]
        Graph how long average solution length is for each run
"""
def test_lengths(num_games, iter_arr, game_file, a, e, g, l, img):

    games   = []  # games to run
    agents  = []  # all game-agents
    threads = []  # all agent-threads
    results = []  # results from testing

    """ iterate for a given agent """
    def iterate_agent(agent, tid):
        res = []                             # results will have an array for each test
        for val in range(len(iter_arr)):     # for each iteration-value
            for i in range(iter_arr[val]):   # iterate through value
                agent.learning_algo()        # learn for i iterations
                res.append(len(agent.node_path))  # append final result to res
        results[tid] = res

    # create a game and agent for every test-run
    for n in range(num_games):
        results.append(None)
        games.append(game.Game(game_file))
        agents.append(q.Q_Learn_Agent(games[n], a, e, g, l))
        threads.append(threading.Thread(target=iterate_agent, args=(agents[n], n,)))
        threads[n].start()

    # end threads
    for thread in threads:
        thread.join()

    # graph results
    graph_len(results, iter_arr, img)


""" Graph Len 
    Reference: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
        Graphs results where it is:
        [col1, col2, col3]
     i1 [val1, val2, val3]
     i2 [      ...       ]
     ...
"""
def graph_len(results, columns, img):

    x = columns
    y = []

    # get results for each iter test
    for i in range(len(x)):

        # get avg
        val  = 0
        for res in results:
            val += res[i]
        y.append(val / len(results))

    # set up plot bars
    width  = 0.6
    figure, axis = plt.subplots()
    ar     = np.arange(len(x))
    bar    = axis.bar(ar - width / 2, y, width, label='Avg Length')

    # set up plot axis
    axis.set_title('Average Solution Length Per Learning Iterations')
    axis.set_ylabel('Number of Dots on Grid')
    axis.set_xlabel('Learning Iterations')
    axis.set_xticks(ar)
    axis.set_xticklabels(x)
    axis.legend()

    # add height label
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            axis.annotate(
                '{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center',
                va='bottom'
            )

    autolabel(bar)
    figure.tight_layout()
    plt.savefig(img)

