import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import threading

import qlearn as q
import game


""" Test Runs
        Take in array of iterations, ex[100, 1000, 5000]
        Choose how many games to run over these runs
"""
def test_runs(num_games, iter_arr, game_file, a, e, g, l, img):

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
    graph_res(results, iter_arr, img)



""" Graph Res 
    Reference: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
        Graphs results where it is:
        [col1, col2, col3]
     i1 [val1, val2, val3]
     i2 [      ...       ]
     ...
"""
def graph_res(results, columns, img):

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
    axis.set_title('Results Per Learning Iterations')
    axis.set_ylabel('Number Occurrences')
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



