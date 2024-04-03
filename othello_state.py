from mcts.base.base import BaseState
from env_operations import EnvOps as eo

class OthelloState(BaseState):

    def __init__(self, env, board=None, reward=0, coords=(8,1)):
        self.env = env
        self.board = board   #grayscale array representation of the board
        self.current_player = 1  #player is white and starts
        self.coords = coords
        self.terminated = False
        self.reward = reward
    
    #returns an iterable of coordinates for all valid disc placements
    def get_possible_actions(self):
        valid_actions = []  #list of tuples containing full actions to place discs at valid squares
        empty_squares = eo.get_empty_squares(self.board)

        for square_coord in empty_squares:
            if eo.check_square_validity(square_coord, self.board):
                valid_actions.append(square_coord)
        if not valid_actions:
            return [(-1, -1)]
        return valid_actions

    #returns 1 if it is the maximizer player's turn to choose an action, or -1 for the minimizer player
    def get_current_player(self) -> int:
        return self.current_player

    #returns the state which results from taking action
    def take_action(self, coord: any) -> 'BaseState':
        if coord == (-1, -1):
            print("No available actions, forfeiting turn")
            new_state = OthelloState(self.env, self.board, self.reward, self.coords)
            new_state.current_player *= -1
            return new_state
        
        new_state = OthelloState(self.env)
        moves = eo.get_moves_to_position(self.coords, coord)

        for move in moves:
            eo.nfs_step(new_state.env, move)
        observation, reward, terminated, trunc, info = eo.nfs_step(new_state.env, 1)
        new_state.current_player *= -1
        new_state.board = observation
        new_state.coords = coord
        new_state.terminated = terminated
        new_state.reward = reward

        return new_state

    #returns `True` if this state is a terminal state
    def is_terminal(self) -> bool:
        return self.terminated

    #returns the reward for this state; only needed for terminal states
    def get_reward(self) -> float:
        #TODO: implement heuristic
        return self.reward
