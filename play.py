import gymnasium as gym
import matplotlib.pyplot as plt
from othello_state import OthelloState

from env_operations import EnvOps as eo

def main():

    env = gym.make("ALE/Othello-v5", render_mode="rgb_array", obs_type="grayscale", frameskip=4)
    env.reset()

    observation, reward, terminated, trunc, info = eo.nfs_step(env, 0)
    game_state = OthelloState(env, observation, (1,1))
    actions = game_state.get_possible_actions()
    print(actions)

    # env.close()

    # rgb = env.render()

    # plt.imshow(rgb)
    # plt.show()
    # input()

    # init_state = OthelloState(env)
    # searcher = MCTS(time_limit=1000)
    # action = searcher.search(initial_state=init_state)
    # print(action)

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