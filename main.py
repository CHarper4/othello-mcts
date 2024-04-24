# MCTS from https://github.com/kstruempf/MCTS/tree/main
# Othello environment and greedy player from https://github.com/suragnair/alpha-zero-general
#
# @misc{thakoor2016learning,
#   title={Learning to play othello without human knowledge},
#   author={Thakoor, Shantanu and Nair, Surag and Jhunjhunwala, Megha},
#   year={2016},
#   publisher={Stanford University, Final Project Report}
# }

from mcts.searcher.mcts import MCTS
from othello_state import OthelloState

from AlphaOthello.OthelloGame import OthelloGame
from AlphaOthello.OthelloPlayers import HumanOthelloPlayer, GreedyOthelloPlayer

from policies import weight_table_policy, component_policy

from tqdm import tqdm
import ast

#returns list of game stats, each containing the score from policy1's perspective and the number of turns
def policy_v_policy_test(search_time, policy1=None, policy2=None):
    game = OthelloGame(6)
    def mcts1_move(board, player):
        searcher = MCTS(time_limit=search_time, rollout_policy=policy1)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action
    def mcts2_move(board, player):
        searcher = MCTS(time_limit=search_time, rollout_policy=policy2)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action
    scores = []
    mcts_player = 1 #1/O, -1/X, tracks who mcts is playing as

    #testing loop, 100 iterations
    for i in tqdm(range(100)):
        board = game.getInitBoard()
        turns = 0
        #first turn alternation
        if mcts_player == 1:
            p1, p2 = mcts1_move, mcts2_move
        else:
            p1, p2 = mcts2_move, mcts1_move
        #game loop
        curr_player = 1
        while game.getGameEnded(board, 1) == 0:
            if curr_player == 1:
                action = p1(board, curr_player)
                board, curr_player = game.getNextState(board, curr_player, action)
            else:
                action = p2(board, curr_player)
                board, curr_player = game.getNextState(board, curr_player, action)
            turns += 1
        scores.append((game.getScore(board, mcts_player), turns))
        mcts_player *= -1
    return scores

def policy_test(search_time, policy=None):
    game = OthelloGame(6)

    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action

    def mcts_move(board, player):
        searcher = MCTS(time_limit=search_time, rollout_policy=policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action
    
    scores = []
    mcts_player = 1 #1/O, -1/X, tracks who mcts is playing as

    #testing loop, 100 iterations
    for i in tqdm(range(100)):
        board = game.getInitBoard()
        turns = 0

        #first turn alternation
        if mcts_player == 1:
            p1, p2 = mcts_move, greedy_move
        else:
            p1, p2 = greedy_move, mcts_move

        #game loop
        curr_player = 1
        while game.getGameEnded(board, 1) == 0:
            if curr_player == 1:
                action = p1(board, curr_player)
                board, curr_player = game.getNextState(board, curr_player, action)
            else:
                action = p2(board, curr_player)
                board, curr_player = game.getNextState(board, curr_player, action)
            turns += 1
        scores.append((game.getScore(board, mcts_player), turns))
        mcts_player *= -1
    
    return scores

def policy_debug(policy=None):
    game = OthelloGame(6)

    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action

    def mcts_move(board, player):
        searcher = MCTS(time_limit=1000, rollout_policy=policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action

    curr_player = 1
    board = game.getInitBoard()
    game.display(board)
    while game.getGameEnded(board, 1) == 0:
        if curr_player == 1:
            print("MCTS")
            action = mcts_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        else:
            print("greedy")
            action = greedy_move(board, curr_player)
            board, curr_player = game.getNextState(board, curr_player, action)
        game.display(board)
    print("score: %i " % game.getScore(board, 1))  

def get_stats(path):
    #get number of wins and average score from file record
    with open(path, 'r') as f:
        games = ast.literal_eval(f.readline())
        total = 0
        wins = [w[0] for w in games if w[0] > 0]
        num_wins = len(wins)
        for game in games:
            total += game[0]
        avg_score = total/100
    return num_wins, avg_score

def main():
    # policy_debug(policy=component_policy)

    # #policy v policy
    # try:
    #     print("weight table policy vs component policy at 5 sec")
    #     games = policy_v_policy_test(5000, policy1=component_policy, policy2=weight_table_policy)
    #     mcts_wins = [s for s in games if s[0] > 0]
    #     print("%i mcts wins" % len(mcts_wins))
    #     with open('output/comp_v_table_5.txt', 'w') as f:
    #         f.write(str(games))
    # except Exception as e:
    #     print("comp v weight table failed: " + str(e))

    # #policy v greedy
    # try:
    #     print("6x6 weight table policy at 1 sec")
    #     games = policy_test(1000, policy=weight_table_policy)
    #     mcts_wins = [s for s in games if s[0] > 0]
    #     print("%i mcts wins" % len(mcts_wins))
    #     with open('output/table_.txt', 'w') as f:
    #         f.write(str(games))
    # except Exception as e:
    #     print("component failed: " + str(e))

    wins, avg_score = get_stats('output/table_1.txt')
    print(wins)
    print(avg_score)

    

if __name__ == "__main__":
    main()
