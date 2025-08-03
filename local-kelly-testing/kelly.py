import random
import pandas as pd

from argparse import ArgumentParser

def get_kelly(p, b):
    return p - (1-p)/b

class KellyBasic:

    def __init__(self, bankroll=20):
        self._bankroll = bankroll
        self._columns = ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
        self._results = pd.DataFrame(columns=self._columns)

    def get_results(self):
        return self._results

    def get_bankroll(self):
        return self._bankroll

    def simulate_days(self, days, p_expected=0.7, b_mean=0.7):
        for d in range(days):

            initial_b = self._bankroll

            # get new b
            b = self._update_b(b_mean)
            p = self._update_p(p_expected)

            # get Kelly factor
            f = get_kelly(p, b)

            # calculate wager
            wager, payout = self._calculate_wager(f, b)

            # place wager
            self._place_wager(wager)

            # simulate game
            r = self._simulate_game(p_expected)

            # add back winnings
            self._bankroll += r * payout

            # save off result
            #columns = ['Day', 'Starting Bank', 'Ending Bank', 'Result', 'Wager', 'Payout', 'f', 'b', 'p']
            self._results.loc[len(self._results)] = [d+1, initial_b, self._bankroll, r, wager, payout, f, b, p]

    def _update_b(self, b):
        spread = random.random() * 0.2 - 0.1
        return b + spread

    def _update_p(self, p):
        return p

    def _calculate_wager(self, f, b):
        wager = f * self._bankroll
        payout = wager * (1 + b)

        if wager < 0:
            wager = 0
        if payout < 0:
            payout = 0

        return wager, payout

    def _place_wager(self, wager):
        if wager < 0:
            return

        self._bankroll -= wager
        if (self._bankroll < 0):
            raise ValueError(f'Went bust')

    def _simulate_game(self, p):
        r = random.random()
        if r <= 1-p:
            r = 0
        else:
            r = 1

        return r


class KellyAdaptive(KellyBasic):

    def __init__(self, bankroll=20):
        super().__init__(bankroll)
        self._wins = 7
        self._games = 10

    def _simulate_game(self, p):
        r = super()._simulate_game(p)

        if r == 1:
            self._wins += 1
        self._games += 1

        return r

    def _update_p(self, p):
        if self._games == 0:
            return p
        else:
            return self._wins / self._games

if __name__ == '__main__':

    parser = ArgumentParser()

    parser.add_argument('-b', '--odds', type=float, default=.7, help='Payout (e.g. If a bet gives 2 to 1 odds b=2.0. If a bet gives 1.78 to one b=0.78. If a bet gives -111 b=100/111=0.9009.')
    parser.add_argument('-p', '--win_probability', type=float, default=0.7, help='Probability of winning a particular bet.')

    args = parser.parse_args()

    print(f'f=${get_kelly(p, b)}')
