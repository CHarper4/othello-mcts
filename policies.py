from mcts.base.base import BaseState
import math
from AlphaOthello.OthelloGame import OthelloGame

#-------heuristic value functions for component-based policy
def normalize(player_value, opp_value, min, max) -> float:
    if player_value + opp_value != 0:
        p_val = (player_value-min)/(max-min)
        o_val = (opp_value-min)/(max-min)
        value = (100*(p_val-o_val)/(p_val+o_val) + 100)/2
    else:
        value = 0
    return value

def actual_mobility_value(state: BaseState) -> float:
    player_act_mob = len(state.get_possible_actions())
    opp_act_mob = len(state.get_possible_actions(-1))#state.get_current_player() *
    return normalize(player_act_mob, opp_act_mob, 0, 32)

def potential_mobility_value(state: BaseState) -> float:
    #potential mobility is the number of empty spaces adjacent to at least 1 opponent space
    def get_pot_mob(board, player):
        b = list(board)
        potential_squares = []
        opp_squares = []

        #find opponent's squares
        for i in range(len(b)):
            row = list(b[i])
            for j, val in enumerate(row):
                if val == -player:
                    opp_squares.append((j, i))
        #check surrounding coords for (unseen) empty squares
        for coord in opp_squares:
            x, y = coord
            xs = [x-1, x, x+1]
            ys = [y-1, y, y+1]
            for x in xs:
                for y in ys:
                    try:
                        if b[y][x] == 0 and (x,y) not in potential_squares:
                            potential_squares.append((x,y))
                    except IndexError:
                        continue
        return len(potential_squares)
    player_pot_mob = get_pot_mob(state.get_board(), state.get_current_player())
    opp_pot_mob = get_pot_mob(state.get_board(), state.get_current_player() * -1)
    return normalize(player_pot_mob, opp_pot_mob, 0, 64)

def mobility_value(state: BaseState) -> float:
    return (actual_mobility_value(state) + potential_mobility_value(state))/2

def square_parity_value(state: BaseState) -> float:
    board = state.get_board()
    player = state.get_current_player()
    opp = -player
    player_squares, opp_squares = 0, 0
    for row in board:
        for val in list(row):
            if val == player: player_squares += 1
            elif val == opp: opp_squares += 1
    return normalize(player_squares, opp_squares, 0, 64)

def corner_value(state: BaseState) -> float:
    player_corner_value, opp_corner_value = 0, 0
    player, opp = state.get_current_player(), state.get_current_player()*-1
    board = state.get_board()

    #check for immediate corner captures
    corner_coords = [(0,0), (0,7), (7,0), (7,7)]
    for x, y in corner_coords:
        if board[x][y] == player:
            player_corner_value += 5 #captured corners weighted 5
        elif board[x][y] == opp:
            opp_corner_value += 5

    #check for potential corner moves
    corner_moves = [0, 7, 56, 63]
    player_corner_value += 3*len([a for a in state.get_possible_actions(p=player) if a in corner_moves]) #potential corners weighted 3
    opp_corner_value += 3*len([a for a in state.get_possible_actions(p=opp) if a in corner_moves])
    return normalize(player_corner_value, opp_corner_value, 0, 20)

def stability_value(state: BaseState) -> float:
    #stable: cannot be flipped for the rest of the game
    #semi-stable: could be flipped some time in the future
    #unstable: can be flipped right now
    #1, 0, -1 for weights
    board = state.get_board()

    def get_stability_value(p):
        game = OthelloGame(8)
        corner_coords = [(0,0), (0,7), (7,0), (7,7)]
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        stability_value = 0

        #check for stable positions
        #stable_positions = []
        for coord in corner_coords:
            x, y = coord
            if board[y][x] == p:
                stability_value += 1
                for dir in directions:
                    x, y = coord
                    x += dir[0]
                    y += dir[1]
                    while y in range(8) and x in range(8) and board[y][x] == p: #traverse axes
                        stability_value += 1
                        x += dir[0]
                        y += dir[1]
        # #check for unstable positions
        # opp_moves = state.get_possible_actions(-p)
        # for y in range(len(board)): 
        #     for x in range(len(board[y])):
        #         if board[y][x] not in stable_positions and board[y][x] == p:
        #             for move in opp_moves:
        #                 next_board = game.getNextState(board, -p, move)[0]
        #                 if next_board[y][x] == -p:  #check if move flipped position
        #                     stability_value -= 1
        #                     break
        return stability_value
    player_value = get_stability_value(state.get_current_player())
    opp_value = get_stability_value(-state.get_current_player())
    return normalize(player_value, opp_value, 0, 28)

#-------policies
#evaluates state on linear combination of mobility, stability, coin parity, and corner control
def component_policy(state: BaseState):
    #weight order: corner, mobility, stability, parity
    early_game = (0.15, 0.5, 0.35, 0)
    mid_game = (0.4, 0.1, 0.4, 0.1)
    late_game = (0, 0, 0, 1)
    board = state.get_board()

    #crude approximation of turn length, could be wrong if a player had to skip a turn because they had no 
    #   moves, but shouldn't make that much of a difference
    turn = -3 #account for starting positions
    for row in board:
        for val in row:
            if val != 0: turn += 1
    if turn <= 10:
        weights = early_game
        depth_limit=20
    elif turn <= 40:
        weights = mid_game
        depth_limit=10
    else:
        depth_limit=20
        weights = late_game
    
    heuristics = [corner_value, mobility_value, stability_value, square_parity_value]
    depth = 0
    while not state.is_terminal() and depth < depth_limit:
        #find action that results in position with most available moves
        actions = state.get_possible_actions()
        best_value, best_action = -math.inf, -1
        for action in actions:
            next_state = state.take_action(action)

            state_value = 0
            #linear combination of heuristics
            for i, heuristic in enumerate(heuristics):
                if weights[i] != 0: #don't calculate heuristic if weight is 0
                    state_value += weights[i]*heuristic(next_state)

            if state_value > best_value:
                best_value = state_value
                best_action = action
        state = state.take_action(best_action)
        depth += 1
    return state.get_reward()

#uses static weight table for state evaluation
def weight_table_policy(state: BaseState) -> float:
    weights = [[4, -3, 2, 2, 2, 2, -3, 4],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [4, -3, 2, 2, 2, 2, -3, 4]]

    def get_state_value(board, player):
        state_value = 0
        b = list(board)
        for i in range(len(b)):
            for j, val in enumerate(list(b[i])):
                if val == player:
                    state_value += weights[i][j]
        return state_value
    
    while not state.is_terminal():
        actions = state.get_possible_actions()
        best_value, best_action = -math.inf, -1
        for action in actions:
            next_state = state.take_action(action)
            player_value = get_state_value(next_state.get_board(), next_state.get_current_player())
            opp_value = get_state_value(next_state.get_board(), next_state.get_current_player()*-1)
            state_value = normalize(player_value, opp_value, -56, 56)
            if state_value > best_value:
                best_value = state_value
                best_action = action
        state = state.take_action(best_action)
    return state.get_reward()