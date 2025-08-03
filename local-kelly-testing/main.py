import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from kelly import KellyBasic, KellyAdaptive

# ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
def scatter_obswin_avgbank(kellys, outfile):
    xd = []
    yd = []
    for k in kellys:
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
    plt.clf()


# ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
def line_average_days(kellys, days, outfile):
    day_averages = []

    for d in range(days):
        day_sum = 0
        for k in kellys:
            day = k.get_results()['Ending Bank'][d]
            day_sum += day

        day_avg = day_sum / len(kellys)
        day_averages.append(day_avg)

    x = [d for d in range(days)]
    y = day_averages
    plt.plot(x,y)
    plt.xlabel('Day')
    plt.ylabel('Average Day Bankroll')
    plt.savefig(outfile)
    plt.clf()



if __name__ == '__main__':

    print("Kelly Computations")

    parser = ArgumentParser()

    parser.add_argument('-d', '--days', type=int, default=30, help='Number of days to experiment with')
    parser.add_argument('-n', '--monte', type=int, default=1, help='Number of monte carlo runs')
    parser.add_argument('-b', '--bankroll', type=int, default=20, help='Starting bankroll')
    parser.add_argument('-m', '--max_bankroll', type=int, default=2000, help='Maximum bankroll to consider realistic')
    parser.add_argument('-p', '--win_probability', type=float, default=0.7, help='Actual win probability of model')

    args = parser.parse_args()

    # generate a bunch of data
    statics = []
    adaptives = []

    for n in range(args.monte):
        ks = KellyBasic(args.bankroll)
        ks.simulate_days(args.days, args.win_probability)
        statics.append(ks)
        #print(ks.get_results())

        ka = KellyAdaptive(args.bankroll)
        ka.simulate_days(args.days, args.win_probability)
        adaptives.append(ka)
        #print(ka.get_results())

    # scatterplots of win p vs ending bankroll
    scatter_obswin_avgbank(statics, 'out/scatter_obswin_avgbank_statics.png')
    scatter_obswin_avgbank(adaptives, 'out/scatter_obswin_avgbank_adaptives.png')

    # line plots of average bankroll by day
    line_average_days(statics, args.days, 'out/line_avgdays_statics.png')
    line_average_days(adaptives, args.days, 'out/line_avgdays_adaptives.png')


