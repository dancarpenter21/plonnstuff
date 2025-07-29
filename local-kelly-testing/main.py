import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from kelly import KellyBasic, KellyAdaptive

def scatter(statics, outfile):
    xd = []
    yd = []
    for k in statics:
        # ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
        res_frame = k.get_results()
        observed_win_prob = res_frame['Result'].sum() / len(res_frame)
        xd.append(observed_win_prob)
        average_bankroll = res_frame['Ending Bank'].mean()
        yd.append(average_bankroll)

    x = np.array(xd)
    y = np.array(yd)

    plt.scatter(x,y)
    plt.xlabel('Observed Win Probability')
    plt.ylabel('Average Bankroll')
    plt.savefig(outfile)




if __name__ == '__main__':

    print("Kelly Computations")

    parser = ArgumentParser()

    parser.add_argument('-d', '--days', type=int, default=30, help='Number of days to experiment with')
    parser.add_argument('-n', '--monte', type=int, default=1, help='Number of monte carlo runs')
    parser.add_argument('-b', '--bankroll', type=int, default=20, help='Starting bankroll')
    parser.add_argument('-m', '--max_bankroll', type=int, default=2000, help='Maximum bankroll to consider realistic')

    args = parser.parse_args()

    # generate a bunch of data
    statics = []
    adaptives = []

    for n in range(args.monte):
        ks = KellyBasic(args.bankroll)
        ks.simulate_days(args.days)
        statics.append(ks)
        #print(ks.get_results())

        ka = KellyAdaptive(args.bankroll)
        ka.simulate_days(args.days)
        adaptives.append(ka)
        #print(ka.get_results())

    # scatterplots of win p vs ending bankroll
    scatter(statics, 'out/statics.png')
    scatter(adaptives, 'out/adaptives.png')



