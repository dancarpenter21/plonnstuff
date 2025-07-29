import sys
import random

class Result:

    def __init__(self, initial_b, final_b, result, f, p, b, wager, payout, day):
        '''
        Should make this a pandas dataframe for real data analysis
        '''
        self.initial_b = initial_b
        self.final_b = final_b
        self.result = result
        self.f = f
        self.p = p
        self.b = b
        self.wager = wager
        self.day = day
        self.payout = payout

    def __str__(self):
        return f'Result[Day: {self.day} Bank: {self.initial_b:.2f}->{self.final_b:.2f}   f: {self.f:.2f}={self.p:.2f}-(1-{self.p:.2f})/{self.b:.2f}   {self.result=} {self.wager=:.2f} {self.payout=:.2f}]'


class KellyBasic:

    def __init__(self, bankroll=20):
        self._bankroll = bankroll
        self._results = []

    def print_results(self, start=0, end=sys.maxsize):
        if end > len(self._results):
            end = len(self._results)

        for i in range(start, end):
            print(self._results[i])

    def get_results(self):
        return self._results

    def get_bankroll(self):
        return self._bankroll

    def get_bankline(self):
        bankline = []
        for r in self._results:
            bankline.append(r.final_b)

        return bankline

    def simulate_days(self, days, p_expected=0.7, b_mean=0.7):
        for d in range(days):

            initial_b = self._bankroll

            # get new b
            b = self._update_b(b_mean)
            p = self._update_p(p_expected)

            # get Kelly factor
            f = self._get_kelly(p, b)

            # calculate wager
            wager, payout = self._calculate_wager(f, b)

            # place wager
            self._place_wager(wager)

            # simulate game
            r = self._simulate_game(p_expected)

            # add back winnings
            self._bankroll += r * payout

            # save off result
            result = Result(result=r, f=f, p=p, b=b, wager=wager, day=len(self._results)+1, initial_b=initial_b, final_b=self._bankroll, payout=payout)
            self._results.append(result)

    def _update_b(self, b):
        spread = random.random() * 0.2 - 0.1
        return b + spread

    def _update_p(self, p):
        return p

    def _get_kelly(self, p, b):
        return p - (1-p)/b

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


