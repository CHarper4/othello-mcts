# MCTS from https://github.com/kstruempf/MCTS/tree/main
# Othello environment and greedy/random players from https://github.com/suragnair/alpha-zero-general
#
# @misc{thakoor2016learning,
#   title={Learning to play othello without human knowledge},
#   author={Thakoor, Shantanu and Nair, Surag and Jhunjhunwala, Megha},
#   year={2016},
#   publisher={Stanford University, Final Project Report}
# }

from mcts.searcher.mcts import MCTS
from mcts.base.base import BaseState
from othello_state import OthelloState

from AlphaOthello.OthelloGame import OthelloGame
from AlphaOthello.OthelloPlayers import HumanOthelloPlayer, GreedyOthelloPlayer

from policies import actual_mobility_policy, potential_mobility_policy

import time
from tqdm import tqdm
import ast
import numpy as np

#TODO: stability, corner policies
#TODO: alpha-beta search to test against
#TODO: test runs for policies

def policy_test(search_time, policy=None):

    game = OthelloGame(6)

    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action

    def mcts_move(board, player):
        searcher = MCTS(time_limit=search_time, rollout_policy=policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action

    scores = []
    mcts_player = 1 #1/O, -1/X, tracks who mcts is playing as

    #testing loop, 100 iterations
    for i in tqdm(range(100)):
        board = game.getInitBoard()
        turns = 0

        #first turn alternation
        if mcts_player == 1:
            p1, p2 = mcts_move, greedy_move
        else:
            p1, p2 = greedy_move, mcts_move

        #game loop
        curr_player = 1
        while game.getGameEnded(board, 1) == 0:
            if curr_player == 1:
                action = p1(board, curr_player)
                board, curr_player = game.getNextState(board, curr_player, action)
            else:
                action = p2(board, curr_player)
                board, curr_player = game.getNextState(board, curr_player, action)
            turns += 1
        scores.append((game.getScore(board, mcts_player), turns))
        mcts_player *= -1
    
    return scores

def policy_debug(policy=None):
    game = OthelloGame(6)

    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action

    def mcts_move(board, player):
        searcher = MCTS(time_limit=1000, rollout_policy=actual_mobility_policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action

    curr_player = 1
    board = game.getInitBoard()
    game.display(board)
    while game.getGameEnded(board, 1) == 0:
        if curr_player == 1:
            print("MCTS")
            action = mcts_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        else:
            print("greedy")
            action = greedy_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        game.display(board)
    print("score: %i " % game.getScore(board, 1))  

def main():
    policy_debug(policy=potential_mobility_policy)
        
    # print("mobility policy at 3 secs")
    # games = config_test(3000, actual_mobility_policy)
    # mcts_wins = [s for s in games if s[0] > 0]
    # print("%i mcts wins" % len(mcts_wins))
    # with open('output/mobMCTS_3.txt', 'w') as f:
    #     f.write(str(games))

    #get number of wins and average score from file record
    # with open('output/randMCTS_5.txt', 'r') as f:
    #     games = ast.literal_eval(f.readline())
    #     total = 0
    #     wins = [w[0] for w in games if w[0] > 0]
    #     print(len(wins))
    #     for game in games:
    #         total += game[0]
    #     print(total/100)


    #-----------LOG-----------
    # random mcts vs greedy
    # 1 sec - 60 mcts wins
    # 3 sec - 72 mcts wins - 1:22:10
    # 5 sec - 70 mcts wins - 2:15:49 - 8.85 avg score

    # simple mobility mcts vs greedy
    # 1 sec - 67 mcts wins - 27:27
    # 3 sec - 93 mcts wins - 1:20:40 - 7.48 avg score
    # 5 sec - 100 mcts wins - 2:16:12 - 18.04 avg score


if __name__ == "__main__":
    main()
