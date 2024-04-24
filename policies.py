from mcts.base.base import BaseState
import math

#-------single-heuristic policies
def actual_mobility_policy(state: BaseState) -> float:
    while not state.is_terminal():
        #find action that results in position with most available moves
        actions = state.get_possible_actions()
        best_mobility, best_action = -1, -1
        for action in actions:
            next_state = state.take_action(action)
            opp = state.get_current_player() * -1
            mcts_act_mob = len(next_state.get_possible_actions())
            opponent_act_mob = len(next_state.get_possible_actions(p=opp))
            if mcts_act_mob + opponent_act_mob != 0:
                mobility_value = 100*(mcts_act_mob-opponent_act_mob)/(mcts_act_mob+opponent_act_mob)
            else:
                mobility_value = 0
            if mobility_value > best_mobility:
                best_mobility = mobility_value
                best_action = action
        state = state.take_action(best_action)
    return state.get_reward()

def potential_mobility_policy(state: BaseState) -> float:
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
    
    while not state.is_terminal():
        #find action that results in position with most potential moves
        actions = state.get_possible_actions()
        best_mobility, best_action = -math.inf, -1
        for action in actions:
            next_state = state.take_action(action)
            mcts_pot_mob = get_pot_mob(next_state.get_board(), state.get_current_player())
            opponent_pot_mob = get_pot_mob(next_state.get_board(), state.get_current_player() * -1)
            if mcts_pot_mob + opponent_pot_mob != 0:
                mobility_value = 100*(mcts_pot_mob-opponent_pot_mob)/(mcts_pot_mob+opponent_pot_mob)
            else:
                mobility_value = 0
            if mobility_value > best_mobility:
                best_mobility = mobility_value
                best_action = action
        state = state.take_action(best_action)
    return state.get_reward()

def corner_policy(state: BaseState) -> float:
    #captured corners weighted 5
    #potential corners weighted 3
    corner_moves = [0, 5, 30, 35]
    corner_coords = [(0,0), (0,5), (5,0), (5,5)]
    while not state.is_terminal():
        actions = state.get_possible_actions()
        best_corner_value, best_action = -1, -1
        for action in actions:
            corner_value = 0
            next_state = state.take_action(action)
            for coord in corner_coords: #check each corner for player piece
                if coord == next_state.get_current_player():
                    corner_value += 5
            potential_corners = [a for a in next_state.get_possible_actions() if a in corner_moves]
            corner_value += 3*len(potential_corners)
            if corner_value > best_corner_value:
                best_corner_value = corner_value
                best_action = action
        state.take_action(best_action)
    return state.get_reward()

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

def stability_value(state: BaseState) -> float:
    #stable: cannot be flipped for the rest of the game
    #semi-stable: could be flipped some time in the future
    #unstable: can be flipped right now
    pass

def corner_value(state: BaseState) -> float:
    corner_moves = [0, 5, 30, 35]
    corner_coords = [(0,0), (0,5), (5,0), (5,5)]
    player_corner_value, opp_corner_value = 0, 0
    player, opp = state.get_current_player(), state.get_current_player()*-1
    for coord in corner_coords: #check each corner for player piece
        if coord == player:
            player_corner_value += 5 #captured corners weighted 5
        elif coord == opp:
            opp_corner_value += 5
    player_corner_value += 3*len([a for a in state.get_possible_actions(p=player) if a in corner_moves])
    opp_corner_value += 3*len([a for a in state.get_possible_actions(p=opp) if a in corner_moves])
    return normalize(player_corner_value, opp_corner_value)

#-------final policies
#evaluates state on linear combination of mobility, stability, coin parity, and corner control
    #takes weights as argument, otherwise uses default weights
def component_policy(state: BaseState, **kwargs):
    #linear combination of heuristic values using passed weights or
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

#prioritizes moves based on static weight table
def weight_table_policy(state: BaseState) -> float:
    # weights = [[4, -3, 2, 2, 2, 2, -3, 4],
    #         [-3, -4, -1, -1, -1, -1, -4, -3],
    #         [2, -1, 1, 0, 0, 1, -1, 2],
    #         [2, -1, 0, 1, 1, 0, -1, 2],
    #         [2, -1, 0, 1, 1, 0, -1, 2],
    #         [2, -1, 1, 0, 0, 1, -1, 2],
    #         [-3, -4, -1, -1, -1, -1, -4, -3],
    #         [4, -3, 2, 2, 2, 2, -3, 4]]

    #weights scaled down to 6x6
    reduced_weights = [[100, -25, 10, 10, -25, 100],
            [-25, -25, 2, 2, -25, -25],
            [7, 1, 5, 5, 1, 7],
            [7, 1, 5, 5, 1, 7],
            [-25, -25, 2, 2, -25, -25],
            [100, -25, 10, 10, -25, 100]]
    
    def get_state_value(board, player):
        state_value = 0
        b = list(board)
        for i in range(len(b)):
            for j, val in enumerate(list(b[i])):
                if val == player:
                    state_value += val*reduced_weights[i][j]
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