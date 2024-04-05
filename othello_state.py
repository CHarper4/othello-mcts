from mcts.base.base import BaseState
from env_operations import EnvOps as eo

from copy import deepcopy
import time

class OthelloState(BaseState):

    def __init__(self, env, observation=None):
        self.env = env
        self.current_player = 1  #player starts as white
        self.board = observation   #grayscale array representation of the board
        self.coords = (8,1)
        self.terminated = False
        self.reward = 0
    
    #returns an iterable of coordinates for all valid disc placements
    def get_possible_actions(self):
        print("getting possible actions")
        start = time.time()
        valid_actions = []
        empty_squares = eo.get_empty_squares(self.board)

        for square_coord in empty_squares:
            if eo.check_square_validity(self.env, self.coords, square_coord): #, self.board, self.current_player
                valid_actions.append(square_coord)
        if not valid_actions:
            return (-1, -1)
        end = time.time()
        print("finished getting actions, took " + str(end-start) + " secs")
        return valid_actions
        

    #returns the state which results from taking action
    def take_action(self, action_coord) -> 'BaseState':

        new_state = deepcopy(self)

        if action_coord == (-1, -1):
            print("No available actions, forfeiting turn")
            new_state.current_player *= -1
            return new_state
        
        moves = eo.get_moves_to_position(self.coords, action_coord)

        for move in moves:
            eo.nfs_step(new_state.env, move)
        observation, reward, terminated, trunc, info = eo.nfs_step(new_state.env, 1)

        new_state.board, new_state.reward, new_state.terminated = observation, reward, terminated
        new_state.current_player *= 1
        new_state.coords = action_coord

        print("move taken")
        return new_state
    
    #returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimizer player
    def get_current_player(self):
        return self.current_player
    
    #returns `True` if this state is a terminal state
    def is_terminal(self):
        return self.terminated

    #returns the reward for this state; only needed for terminal states
    def get_reward(self):
        #TODO: implement heuristic
        return self.reward
