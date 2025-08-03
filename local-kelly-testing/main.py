import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
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
    plt.title(f'Average Bankroll Per Observed Win Probability')
    plt.xlabel('Observed Win Probability')
    plt.ylabel('Average Bankroll')
    plt.savefig(outfile)
    plt.clf()


# ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
def line_average_days(kellys, days, outfile):
    days = range(days)
    day_avgs = []
    day_std = []
    for d in days:
        dayline = []
        for k in kellys:
            rs = k.get_results()['Ending Bank'][d]
            dayline.append(rs)

        dayline_np = np.array(dayline)
        day_avgs.append(dayline_np.mean())
        day_std.append(dayline_np.std())

    x = np.array(days)
    y = np.array(day_avgs)
    ys = np.array(day_std)
    plt.plot(x,y)
    #plt.fill_between(x, y-ys, y+ys, color='lightblue', alpha=0.4)
    plt.xlabel('Day')
    plt.ylabel('Average Day Bankroll')
    plt.savefig(outfile)
    plt.clf()

# ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
def print_average_kellys(kellys):
    with open('out/results.txt', 'w') as file:
        for k in kellys:
            fs = k.get_results()['f']
            mean = np.array(fs).mean()
            print(mean)
            file.write(mean)

def get_timestamp():
    return datetime.now().isoformat()


if __name__ == '__main__':

    print("Kelly Betting Strategies")

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
    scatter_obswin_avgbank(statics, f'out/{get_timestamp()}_scatter_obswin_avgbank_staticP_p={args.win_probability}_N={args.monte}_B={args.bankroll}_Days={args.days}.png')
    scatter_obswin_avgbank(adaptives, f'out/{get_timestamp()}_scatter_obswin_avgbank_adaptiveP_p={args.win_probability}_N={args.monte}_B={args.bankroll}_Days={args.days}.png')

    # line plots of average bankroll by day
    line_average_days(statics, args.days, f'out/{get_timestamp()}_line_avgdays_staticP_p={args.win_probability}_N={args.monte}_B={args.bankroll}_Days={args.days}.png.png')
    line_average_days(adaptives, args.days, f'out/{get_timestamp()}_line_avgdays_adaptiveP_p={args.win_probability}_N={args.monte}_B={args.bankroll}_Days={args.days}.png.png')

    print_average_kellys(statics)
    print_average_kellys(adaptives)
