import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from kelly import KellyBasic, KellyAdaptive

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

    ka = KellyAdaptive(args.bankroll)
    ka.simulate_days(args.days)
    adaptives.append(ka)


    #ks.print_results()
    #ka.print_results()

# plot ending bankrolls
bankrolls_s = []
for k in statics:
    if k.get_bankroll() < args.max_bankroll:
        bankrolls_s.append(k.get_bankroll())

np_static = np.array(bankrolls_s)
plt.hist(np_static, bins=300, edgecolor='black')
plt.title(f'Static {len(bankrolls_s)} Eligible Runs')
plt.savefig('out/static_hist.png')
plt.clf()

bankrolls_a = []
for k in adaptives:
    if k.get_bankroll() < args.max_bankroll:
        bankrolls_a.append(k.get_bankroll())

np_static = np.array(bankrolls_a)
plt.hist(np_static, bins=300, edgecolor='black')
plt.title(f'Adaptive {len(bankrolls_a)} Eligible Runs')
plt.savefig('out/adaptive_hist.png')
plt.clf()
