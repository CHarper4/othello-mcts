import gymnasium as gym
import matplotlib.pyplot as plt

from env_operations import EnvOps as eo

from othello_state import OthelloState
from mcts.searcher.mcts import MCTS

def main():

    env = gym.make("ALE/Othello-v5", mode=1, render_mode="human", obs_type="grayscale", frameskip=4)
    observation = env.reset()

    terminated=False
    player = 1
    curr_coords = (8,1)
    while not terminated:
        square = input("square: ")
        square = tuple(map(int, square.split(',')))
        print("square: " + str(square))
        moves = eo.get_moves_to_position(curr_coords, square)
        for move in moves:
            eo.nfs_step(env, move)
        observation, reward, terminated, trunc, info = eo.nfs_step(env, 1)
        curr_coords = square
        player *= -1
        print("reward: " + str(reward))


    #trying to run mcts
    # try:
    #     init_state = OthelloState(env, observation)
    #     searcher = MCTS(time_limit=1000)
    #     action = searcher.search(initial_state=init_state)
    #     print(action)
    # except Exception as e:
    #     print(e)

if __name__=="__main__":
    main()


#grayscale values: 0, 212, 104 = black, white, empty

# 0 NOOP
# 1 FIRE
# 2 UP
# 3 RIGHT
# 4 LEFT
# 5 DOWN
# 6 UPRIGHT
# 7 UPLEFT
# 8 DOWNRIGHT
# 9 DOWNLEFT