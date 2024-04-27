# MCTS from https://github.com/kstruempf/MCTS/tree/main
# Othello environment and greedy player from https://github.com/suragnair/alpha-zero-general
#
# @misc{thakoor2016learning,
#   title={Learning to play othello without human knowledge},
#   author={Thakoor, Shantanu and Nair, Surag and Jhunjhunwala, Megha},
#   year={2016},
#   publisher={Stanford University, Final Project Report}
# }

from policies import weight_table_policy, component_policy
from tests import policy_v_policy_test, policy_debug, policy_test, get_stats


def main():
    policy_debug(policy=weight_table_policy)

    # #policy v policy
    # try:
    #     print("weight table policy vs component policy at 1 sec")
    #     games = policy_v_policy_test(1000, policy1=component_policy, policy2=weight_table_policy)
    #     mcts_wins = [s for s in games if s[0] > 0]
    #     print("%i mcts wins" % len(mcts_wins))
    #     with open('output/8x8/comp_v_table_1.txt', 'w') as f:
    #         f.write(str(games))
    # except Exception as e:
    #     print("comp v weight table failed: " + str(e))

    #policy v greedy
    # try:
    #     print("weight table policy at 1 sec")
    #     games = policy_test(1000, policy=weight_table_policy)
    #     mcts_wins = [s for s in games if s[0] > 0]
    #     print("%i mcts wins" % len(mcts_wins))
    #     with open('output/8x8/table_1.txt', 'w') as f:
    #         f.write(str(games))
    # except Exception as e:
    #     print("failed: " + str(e))

    # wins, avg_score = get_stats('output/table_.txt')
    # print(wins)
    # print(avg_score)

    
if __name__ == "__main__":
    main()
