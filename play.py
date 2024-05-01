from mcts.searcher.mcts import MCTS
from othello_state import OthelloState

from AlphaOthello.OthelloGame import OthelloGame
from AlphaOthello.OthelloPlayers import HumanOthelloPlayer

from policies import component_policy

def main():
    game = OthelloGame(8)
    board = game.getInitBoard()
    print()
    print("-----------------------------")
    print("Player v Component Policy MCTS")
    print("Available actions are shown in format [row col]")
    print("-----------------------------")
    print()
    game.display(board)

    player = HumanOthelloPlayer(game, display_moves=True)
    def mcts_move(board, player):
        searcher = MCTS(time_limit=5000, rollout_policy=component_policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action

    curr_player, turn = 1, 1
    while game.getGameEnded(board, 1) == 0:
        p = 'MCTS (O) choosing...'
        if curr_player == -1: p = 'Player (X) move'
        print("Turn %i, %s" % (turn, p))
        if curr_player == 1:
            action = mcts_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        else:
            action = player.play(board)
            board, curr_player = game.getNextState(board, curr_player, action)
        game.display(board)
        turn += 1
    
    score = game.getScore(board, 1)
    if score > 0:
        print("MCTS wins")
    elif score < 0:
        print("Player wins")
    else:
        print("Tie game")
    print("Player Score: " + str(-score))
    print("Turns: " + str(turn))

if __name__=='__main__':
    main()