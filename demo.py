from mcts.searcher.mcts import MCTS
from othello_state import OthelloState

from AlphaOthello.OthelloGame import OthelloGame
from AlphaOthello.OthelloPlayers import GreedyOthelloPlayer

from policies import weight_table_policy

def main():
    game = OthelloGame(8)
    board = game.getInitBoard()
    game.display(board)

    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action
    def mcts_move(board, player):
        searcher = MCTS(time_limit=1000, rollout_policy=weight_table_policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action

    curr_player = 1
    turn = 1
    while game.getGameEnded(board, 1) == 0:
        print("Turn %i" % turn)
        if curr_player == 1:
            action = mcts_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        else:
            action = greedy_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        game.display(board)
        turn += 1
        input()
    print("Score: " + str(game.getScore(board, 1)))

if __name__=='__main__':
    main()