from mcts.searcher.mcts import MCTS
from othello_state import OthelloState

from AlphaOthello.OthelloGame import OthelloGame
from AlphaOthello.OthelloPlayers import GreedyOthelloPlayer

from tqdm import tqdm
import ast

#tests return list of (score, turns) 100 for games

def policy_v_policy_test(search_time, policy1=None, policy2=None):
    game = OthelloGame(8)
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
    pol1 = 1 #1/O, -1/X, tracks who policy1 is playing as

    #testing loop, 100 iterations
    for i in tqdm(range(100)):
        board = game.getInitBoard()
        turns = 0
        #first turn alternation
        if pol1 == 1:
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
        scores.append((game.getScore(board, pol1), turns))
        pol1 *= -1
    return scores

#policy vs greedy player
def policy_test(search_time, policy=None):
    game = OthelloGame(8)

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
    game = OthelloGame(8)
    def greedy_move(board, player):
        greedy_player = GreedyOthelloPlayer(game, player)
        action = greedy_player.play(board)
        return action
    def mcts_move(board, player):
        searcher = MCTS(time_limit=1000, rollout_policy=policy)
        state = OthelloState(board, player)
        action = searcher.search(initial_state=state)
        return action
    curr_player, turn = 1, 1
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
        turn += 1
    print("score: %i" % game.getScore(board, 1))  
    print("turns: %i" % turn)

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