from copy import deepcopy

from mcts.base.base import BaseState #, BaseAction
from mcts.searcher.mcts import MCTS

from env_operations import EnvOps as eo

class OthelloState(BaseState):

    #pixel mapping for squares by x and y coords
    pixels = {
        'x': [20, 37, 54, 70, 85, 100, 117, 133],
        'y': [180, 160, 140, 120, 95, 70, 50, 30]
    }

    def __init__(self, env, game_state, coords):
        self.env = env
        self.board = game_state   #grayscale array representation of the board
        self.current_player = 1  #player is white, opponent is black
        self.coords = coords  #player starts bottom left
    
    #returns an iterable of action tuples for all valid disc placements
    def get_possible_actions(self):
        valid_actions = []  #list of tuples containing full actions to place dics at valid squares

        #identify all spaces where placing a disc would give reward >= 1
        for x in range(1,9):
            for y in range(1,9):
                x_px, y_py = self.pixels['x'][x-1], self.pixels['y'][y-1]
                if self.board[y_py][x_px] == 104:   #square is empty

                    #move env to empty square
                    moves = eo.get_moves_to_position(self.coords, (x,y))
                    for move in moves:
                        eo.nfs_step(self.env, move)
                    self.coords = (x, y)
                    
                    print("placing disc at %d, %d" % (x, y))

                    #try to place a disc, if reward >= 1 the square is a valid place to put a disc
                    #FIXME: copied environment only ever returns reward=0 - write a workaround?: check if adjacent square is black and if it's capped by a white disc 
                    temp_env = deepcopy(self.env)
                    observation, reward, terminated, truncated, info = eo.nfs_step(temp_env, 1)
                    print("env reward: " + str(reward))
                    if reward >= 1:
                        valid_actions.append(moves)

        return valid_actions

    #returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimizer player
    def get_current_player(self) -> int:
        return self.current_player

    #returns the state which results from taking action
    def take_action(self, action: any) -> 'BaseState':
        
        if not action:
            print("No available actions, forfeiting turn")
            #TODO: forfeit turn
        
        #action is a tuple: (player, move1, move2,...,moven)
        new_state = deepcopy(self)
        player = action[0]
        moves = action[1:]

        #execute action: movement to tile, placement of disc, player swap
        for move in moves: 
            _ = new_state.env.step(move)
        observation, reward, done, trunc, info = new_state.env.step(1)
        new_state.current_player = self.current_player * -1
        new_state.coords = self.update_position(self.coords, moves)
        new_state.board = observation
        
        return new_state

    #returns `True` if this state is a terminal state
    def is_terminal(self) -> bool:
        return self.env.done

    #returns the reward for this state; only needed for terminal states
    def get_reward(self) -> float:
        #TODO: implement heuristic
        return self.env.reward
