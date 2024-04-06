# MCTS from https://github.com/kstruempf/MCTS/tree/main
from mcts.searcher.mcts import MCTS
from othello_state import OthelloState


# https://github.com/suragnair/alpha-zero-general
#
# @misc{thakoor2016learning,
#   title={Learning to play othello without human knowledge},
#   author={Thakoor, Shantanu and Nair, Surag and Jhunjhunwala, Megha},
#   year={2016},
#   publisher={Stanford University, Final Project Report}
# }
from AlphaOthello.OthelloGame import OthelloGame
from AlphaOthello.OthelloPlayers import HumanOthelloPlayer

import numpy as np
import time

def main():

    game = OthelloGame(6)
    human_player = HumanOthelloPlayer(game, display_moves=True)
    searcher = MCTS(time_limit=5000)
    board = game.getInitBoard()
    player = 1

    print("player is O, bot is X")
    game.display(board)


    while True:
        if player == -1: #bot move
            state = OthelloState(board, player)

            start = time.time()
            action = searcher.search(initial_state=state) #run mcts
            end = time.time()

            board, player = game.getNextState(board, player, action) #execute move
        else:   #player move
            action = human_player.play(board)
            board, player = game.getNextState(board, player, action)

        game.display(board)
        end = game.getGameEnded(board, player)
        if end != 0:
            print("Game over, player " + str(end) + " wins")
            return


if __name__ == "__main__":
    main()
