from mcts.base.base import BaseState
from AlphaOthello.OthelloGame import OthelloGame

import numpy as np

class OthelloState(BaseState):

    def __init__(self, board, player):
        self.game = OthelloGame(6)
        self.board = board
        self.player = player
    
    #returns an iterable of all possible actions
    def get_possible_actions(self):
        valid_moves = self.game.getValidMoves(self.board, self.player)
        valid_moves = np.where(valid_moves==1)[0]   #convert binary array to indices/acceptable moves
        return valid_moves
        
    #returns the state which results from taking action
    def take_action(self, action) -> 'BaseState':
        board, player = self.game.getNextState(self.board, self.player, action)
        return OthelloState(board, player)
        
    #returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimizer player
    def get_current_player(self):
        return self.player
    
    #returns `True` if this state is a terminal state
    def is_terminal(self):
        game_ended = self.game.getGameEnded(self.board, self.player)
        return game_ended != 0

    #returns the reward for this state; only needed for terminal states
    def get_reward(self):
        return self.game.getScore(self.board, self.player)
