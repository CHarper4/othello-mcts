import matplotlib.pyplot as plt
import numpy as np

def main():
    labels = ['Random', 'Weight Table', 'Component']
    index = np.arange(len(labels))
    w = 0.35

    wins_at_1sec = [54, 73, 42]
    wins_at_5sec = [72, 81, 94]

    plt.bar(index-w/2, wins_at_1sec, w, label='1s', color='gray', align='center')
    plt.bar(index+w/2, wins_at_5sec, w, label='5s', color='black', align='center')
    
    plt.ylim(0, 100)
    plt.xlabel('Policies')
    plt.ylabel('Win Rate')
    plt.title('Policy Win Rates Against Greedy Player')
    plt.xticks(index, labels)
    plt.legend()

    #plt.show()

    plt.savefig('output/policies_v_greedy.png')


if __name__ == '__main__':
    main()