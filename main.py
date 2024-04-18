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

import numpy as np
import time
import random


#default random rollout policy in MCTS library
def random_policy(state: BaseState) -> float:
    while not state.is_terminal():
        try:
            action = random.choice(state.get_possible_actions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(action)
    return state.get_reward()

#prioritizes maximizing own mobility and minimizing opponent's
def mobility_policy(state: BaseState) -> float:
    print("mmp")
    while not state.is_terminal():
        try:
            #find action that results in position with most available moves
            actions = state.get_possible_actions()
            most_moves, best_action = -1, -1
            for action in actions:
                next_state = state.take_action(action)
                num_moves = len(next_state.get_possible_actions())
                if num_moves > most_moves:
                    most_moves = num_moves
                    best_action = action
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(best_action)
    return state.get_reward()

def greedy_policy(state: BaseState) -> float:
    #TODO: implement heuristic that chooses move that results in greatest number of self chips on the board
    pass

#TODO: implement test suite for testing policies

def main():

    game = OthelloGame(6)
    human_player = HumanOthelloPlayer(game, display_moves=True)
    greedy_player = GreedyOthelloPlayer(game)
    searcher = MCTS(time_limit=1000, rollout_policy=mobility_policy)
    board = game.getInitBoard()
    player = 1 # 1 is black/O, -1 is white/X
    turn = 1

    game.display(board)

    while True:
        if player == -1: #mcts/white/X move
            state = OthelloState(board, player)

            start = time.time()
            action = searcher.search(initial_state=state) #run mcts
            end = time.time()
            print("time: " + str(end-start))
            board, player = game.getNextState(board, player, action) #execute move
        else:   #greedy/black/O move
            action = greedy_player.play(board)
            board, player = game.getNextState(board, player, action)

        game.display(board)
        end = game.getGameEnded(board, player)
        if end != 0:
            match end:
                case -1:
                    print("Game over, X wins in %i turns" % turn)
                case 1:
                    print("Game over, O wins in %i turns" % turn)
            return
        turn += 1


if __name__ == "__main__":
    main()
