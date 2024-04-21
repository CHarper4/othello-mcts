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

import time
import random
from tqdm import tqdm

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

#TODO: implement other policies
    # greedy
    # stability
    # potential mobility
    # corners

#TODO: testing suite

def game_loop(p1, p2, game):
    
    game = OthelloGame(6)

    board = game.getInitBoard()
    #game.display(board)
    player = 1 #1/O, -1/X
    turns = 0
    while game.getGameEnded(board, 1) == 0:
        if player == 1: #greedy turn
            action = p1(board, player)
            board, player = game.getNextState(board, player, action)
        else:   #mcts turn
            action = p2(board, player)
            board, player = game.getNextState(board, player, action)
        #game.display(board)
        turns += 1

    return game.getScore(board, 1), turns

def main():

    game = OthelloGame(6)

    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action
    def mcts_move(board, player):
        searcher = MCTS(time_limit=1000)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action

    scores = []
    player = 1  #which player mcts is playing as, used to alternate who gets first turn

    #CURRENT: greedy vs mcts, alternating first move, mcts is using random policy

    #testing loop, 100 iterations
    for i in tqdm(range(100)):
        if player == 1:
            score, turn = game_loop(mcts_move, greedy_move, game)
        else:
            score, turn = game_loop(greedy_move, mcts_move, game)
            score *= -1 #reverse to get mcts score
        scores.append((score, turn))
        player *= -1

    mcts_wins = [s[0] for s in scores if s[0] > 0]
    print("mcts wins: %i" % len(mcts_wins))

    with open('output/greedy_randMCTS_3.txt', 'w') as f:
        f.write(str(scores))


    #-----------LOG-----------
    #100 games - 1 sec random policy mcts vs greedy player - 77 mcts wins - mcts going second, no alternating
    #100 games - 1 sec random policy mcts vs greedy player - 67, 62 mcts wins - alternating starting move


if __name__ == "__main__":
    main()
