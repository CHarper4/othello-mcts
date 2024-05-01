from mcts.base.base import BaseState
import math

#-------heuristic value functions for component-based policy
def normalize(player_value, opp_value) -> float:
    if player_value + opp_value != 0:
        value = (100*(player_value-opp_value)/(player_value+opp_value)+100)/2
    else:
        value = 0
    return value

def actual_mobility_value(state: BaseState) -> float:
    player_act_mob = len(state.get_possible_actions())
    opp_act_mob = len(state.get_possible_actions(p=state.get_current_player() * -1))
    return normalize(player_act_mob, opp_act_mob)

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
    return normalize(player_pot_mob, opp_pot_mob)

def square_parity_value(state: BaseState) -> float:
    board = state.get_board()
    player = state.get_current_player()
    opp = -player
    player_squares, opp_squares = 0, 0
    for row in board:
        for val in list(row):
            if val == player: player_squares += 1
            elif val == opp: opp_squares += 1
    return normalize(player_squares, opp_squares)

def corner_value(state: BaseState) -> float:
    player_corner_value, opp_corner_value = 0, 0
    player, opp = state.get_current_player(), state.get_current_player()*-1
    board = state.get_board()

    #check for immediate corner captures
    corner_coords = [(0,0), (0,7), (7,0), (0,7)]
    for x, y in corner_coords:
        if board[x][y] == player:
            player_corner_value += 5 #captured corners weighted 5
        elif board[x][y] == opp:
            opp_corner_value += 5

    #check for potential corner moves
    corner_moves = [0, 7, 56, 63]
    player_corner_value += 3*len([a for a in state.get_possible_actions(p=player) if a in corner_moves]) #potential corners weighted 3
    opp_corner_value += 3*len([a for a in state.get_possible_actions(p=opp) if a in corner_moves])
    return normalize(player_corner_value, opp_corner_value)

def stability_value(state: BaseState) -> float:
    #stable: cannot be flipped for the rest of the game
    #semi-stable: could be flipped some time in the future
    #unstable: can be flipped right now
    pass

#-------policies
#evaluates state on linear combination of mobility, stability, coin parity, and corner control
    #TODO: dynamic weighting - infer position of game from state and adjust weights accordingly
def component_policy(state: BaseState):
    #corner 30, mobilities 5, stability 25, square parity 25
    corner_weight, mob_weight, sp_weight = (0.45, 0.1, 0.35)
    while not state.is_terminal():
        #find action that results in position with most available moves
        actions = state.get_possible_actions()
        best_value, best_action = -math.inf, -1
        for action in actions:
            next_state = state.take_action(action)

            #linear combination of heuristics
            state_value = corner_weight*corner_value(next_state) 
            + mob_weight*actual_mobility_value(next_state)
            + mob_weight*potential_mobility_value(next_state)
            + sp_weight*square_parity_value(next_state)

            if state_value > best_value:
                best_value = state_value
                best_action = action
        state = state.take_action(best_action)
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

    # weights2 = [[100, -25, 10, 5, 5, 10, -25, 100],
    #         [-25, -25, 2, 2, 2, 2, -25, -25],
    #         [10, 2, 5, 1, 1, 5, 2, 10],
    #         [5, 2, 1, 2, 2, 1, 2, 5],
    #         [5, 2, 1, 2, 2, 1, 2, 5],
    #         [10, 2, 5, 1, 1, 5, 2, 10],
    #         [-25, -25, 2, 2, 2, 2, -25, -25],
    #         [100, -25, 10, 5, 5, 10, -25, 100]]

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
            state_value = normalize(player_value, opp_value)
            if state_value > best_value:
                best_value = state_value
                best_action = action
        state = state.take_action(best_action)
    return state.get_reward()