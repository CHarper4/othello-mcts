import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanOthelloPlayer():
    def __init__(self, game, display_moves=False):
        self.game = game
        self.display_moves = display_moves

    def play(self, board):
        valid = self.game.getValidMoves(board, -1)
        if self.display_moves:
            print("Available actions: ", end='')
            for i in range(len(valid)):
                if valid[i]:
                    print("[" + str(int(i/self.game.n)) + " " + str(int(i%self.game.n)), end="] ")
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 2:
                try:
                    x,y = [int(i) for i in input_a]
                    if ((0 <= x) and (x < self.game.n) and (0 <= y) and (y < self.game.n)) or \
                            ((x == self.game.n) and (y == 0)):
                        a = self.game.n * x + y if x != -1 else self.game.n ** 2
                        if valid[a]:
                            break
                except ValueError:
                    'Invalid integer'
            print('Invalid move')
        return a


class GreedyOthelloPlayer():
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def play(self, board):
        valids = self.game.getValidMoves(board, self.player)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, self.player, a)
            score = self.game.getScore(nextBoard, self.player)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
