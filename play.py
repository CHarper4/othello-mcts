import gymnasium
import matplotlib.pyplot as plt
from othello_state import OthelloState

def main():
    env = gymnasium.make("ALE/Othello-v5", render_mode="rgb_array", obs_type="grayscale")

    _ = env.reset()

    observation, reward, done, trunc, info = env.step(2)

    rgb = env.render()
    plt.imshow(rgb)
    plt.show()

    # observation[210][160]
    # 212 is white, 104 is empty, 0 is black

    # action = (1, 2, 2, 2, 2, 4, 4)
    # moves = action[1:]

    # init_state = OthelloState(env)
    # searcher = MCTS(time_limit=1000)
    # action = searcher.search(initial_state=init_state)
    # print(action)

if __name__=="__main__":
    main()