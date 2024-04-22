from mcts.base.base import BaseState

import random

#default random rollout policy in MCTS library
def random_policy(state: BaseState) -> float:
    while not state.is_terminal():
        try:
            action = random.choice(state.get_possible_actions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(action)
    return state.get_reward()

#maximizes actual mobility and minimizes opponent's
def actual_mobility_policy(state: BaseState) -> float:
    while not state.is_terminal():
        try:
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
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(best_action)
    return state.get_reward()

#maximizes potential mobility and minimizes opponent's
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
        try:
            #find action that results in position with most potential moves
            actions = state.get_possible_actions()
            best_mobility, best_action = -1, -1
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
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(best_action)
    return state.get_reward()

def stability_policy(state: BaseState) -> float:
    pass

def corner_policy(state: BaseState) -> float:
    pass