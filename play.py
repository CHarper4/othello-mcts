import gymnasium as gym
import matplotlib.pyplot as plt

from env_operations import EnvOps as eo

from othello_state import OthelloState
from mcts.searcher.mcts import MCTS

def main():

    env = gym.make("ALE/Othello-v5", render_mode="rgb_array", obs_type="grayscale")
    env.reset()

    observation, reward, terminated, trunc, info = eo.nfs_step(env, 0)

    #running single game
    # coords = (8,1)
    # player = 1

    # while not terminated:   #take a turn
    #     es = eo.get_empty_squares(observation)
    #     valid_squares = []
    #     for s in es:
    #         if eo.check_square_validity(env, coords, s):
    #             valid_squares.append(s)
        
        
    #     print("valid squares: " + str(valid_squares))
    #     print("moving to " + str(valid_squares[0]))
    #     moves = eo.get_moves_to_position(coords, valid_squares[0])
    #     for move in moves:
    #         eo.nfs_step(env, move)
        
    #     observation, reward, terminated, trunc, info = eo.nfs_step(env, 1)
    #     print("placing at " + str(valid_squares[0]) + " reward: " + str(reward))
    #     coords = valid_squares[0]
    #     player *= -1

    #     rgb = env.render()
    #     plt.imshow(rgb)
    #     plt.show()

    try:
        init_state = OthelloState(env, observation)
        searcher = MCTS(time_limit=1000)
        action = searcher.search(initial_state=init_state)
        print(action)
    except Exception as e:
        print(e)

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