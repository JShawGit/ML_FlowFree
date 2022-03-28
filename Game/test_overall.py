import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
import threading
import traceback

import sarsalearn_MOD as s
import qlearn_MOD as q
import game as g

# Test files to use ----------- #
FILES_1 = [  # 1 dot pair
    'levels/1/1_2x2.json',
    'levels/1/1_3x3.json',
    'levels/1/1_4x4.json'
]

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
    for i in range(iterate):
        try:
            run_res = agent.iterate(True)
        except:
            traceback.print_exc()
            print("Error learning.")
            exit(-1)
        for color in game.colors:
            for key in run_res[color]:
                res[color][key] += run_res[color][key]
        res["filled"] += run_res["filled"]
        res["empty"]  += run_res["empty"]
""" --- End Learn --- """


""" Run ----------------------------------------------------------------------------------------------------------------
    Runs the optimal path
    
    Takes in:
        Agent
"""
def run(agent):
    return agent.iterate(False)
""" --- End Learn --- """



""" Test One Pair ------------------------------------------------------------------------------------------------------
    Test all test files in FILES_1, with one pair of dots.
    
    Takes in:
        Type: 0-Q, 1-S, 3-QS
        Iteration array: ex. [100, 500, 1000]
        Rewards: ex. stuck or filled
        Items: Alpha, Epsilon, Gamma, Lambda
        Filename prefix: ex. "/results/test1_game1_"
"""
def test_one_pair(type, iter_array, rewards, items, prefix):
    global FILES_1
    # play game for each file in the one-pair files
    for file in FILES_1:
        res     = {}
        run_res = {}
        games   = {}
        agents  = {}

        # create agents and their games
        if type == 0 or type == 3:
            run_res["Q"] = []
            tmp = init_game(file)
            games["Q"] = tmp[0]
            res["Q"]   = tmp[1]
            agents["Q"] = q.Q_Learn_Agent(games["Q"], items[0], items[1], items[2], items[3], rewards)
        if type == 1 or type == 3:
            run_res["S"] = []
            tmp = init_game(file)
            games["S"] = tmp[0]
            res["S"]   = tmp[1]
            agents["S"] = s.Sarsa_Learn_Agent(games["S"], items[0], items[1], items[2], items[3], rewards)

        # iterate through the learning-iterations
        # log the results for the optimal path after each iter
        for iterate in iter_array:
            for agent in agents:
                learn(iterate, games[agent], agents[agent], res[agent])
                run_res[agent].append(run(agents[agent]))

        # print to file
        for r in res:
            df_res = pd.DataFrame.from_dict([res[r]])
            df_res.to_csv(prefix + r + '_total_results.txt', header=False, index=True, mode='a')
            for i in range(len(iter_array)):
                df_run_res = pd.DataFrame.from_dict([run_res[r][i]])
                df_run_res.to_csv(prefix + r + '_' + str(i) + '_total_results.txt', header=False, index=True, mode='a')













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

