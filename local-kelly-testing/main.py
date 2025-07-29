import numpy

from argparse import ArgumentParser
from kelly import KellyBasic, KellyAdaptive

print("Kelly Computations")

parser = ArgumentParser()

parser.add_argument('-d', '--days', type=int, default=50, help='Number of days to experiment with')
parser.add_argument('-n', '--monte', type=int, default=1000, help='Number of monte carlo runs')
parser.add_argument('-b', '--bankroll', type=int, default=20, help='Starting bankroll')

args = parser.parse_args()

results = numpy.ndarray((args.monte, 2))
for n in range(args.monte):
    #k = KellyBasic(args.bankroll)
    ka = KellyAdaptive(args.bankroll)
    #k.simulate_days(args.days)
    ka.simulate_days(args.days)

    ka.print_results()


#print(results.mean(0))
#print(results.std(0))
