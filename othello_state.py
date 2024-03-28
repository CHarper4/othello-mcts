from copy import deepcopy

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS

class OthelloState(BaseState):
    
    #TODO: map board positions to pixels
    board_positions_to_pixels = {
        (1, 8): (21, 28), #top left
        (5, 5): (84, 94), #center top right
        (4, 5): (70, 94), #center top left

    }

    def __init__(self, env):
        self.env = env
        #self.done = False
        #self.reward = None
        self.current_player = 1
        self.coords = (8,8)  #player starts bottom left
    
    #returns coordinates of new position after taking moves
    #TODO: verify this works correctly
    def update_position(starting_coords, moves):
        x, y = starting_coords
        for move in moves:
            match move:
                case 2:
                    y += 1
                case 3:
                    x += 1
                case 4:
                    x -= 1
                case 5:
                    y -= 1
                case 6:
                    x += 1
                    y += 1
                case 7:
                    x -= 1
                    y += 1
                case 8:
                    x += 1
                    y -= 1
                case 9:
                    x -= 1
                    y -= 1

            #account for wraparound
            if y <= 0: y += 8
            elif y > 8: y -= 8
            if x <= 0: x += 8
            elif x > 8: x -= 8

        return (x, y)
    
    #returns an iterable of all actions which can be taken from this state
    def get_possible_actions(self): #-> [any]
        valid_actions = []
        #TODO: parse grayscale rgb_array into game board
        #TODO: identify all empty spaces next to opponent's pieces
        #TODO: try to place at each space, if reward is 1, add to valid_actions
        #TODO: generate a tuple for each valid move at a position (moves that have reward >= 1), forfeit turn if no possible moves
        return valid_actions

    #returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimizer player
    def get_current_player(self) -> int:
        return self.current_player

    #returns the state which results from taking action
    def take_action(self, action: any) -> 'BaseState':
        #action is a tuple: (player, move1, move2,...,moven)
        new_state = deepcopy(self)
        player = action[0]
        moves = action[1:]

        #execute action: movement to tile, placement of disc, and player swap
        for move in moves: 
            _ = new_state.env.step(move)
        observation, reward, done, trunc, info = new_state.env.step(1)
        new_state.current_player = self.current_player * -1
        new_state.coords = self.update_position(self.coords, moves)
        
        return new_state

    #returns `True` if this state is a terminal state
    def is_terminal(self) -> bool:
        return self.env.done

    #returns the reward for this state; only needed for terminal states
    def get_reward(self) -> float:
        #TODO: implement heuristic
        return self.env.reward