
import numpy
import random
from argparse import ArgumentParser

class Result:
  
  def __init__(self, result, f, amount, payout, day, bankroll):
    self.f = f
    self.amount = amount
    self.day = day
    self.result = result
    self.bankroll = bankroll
    self.payout = payout


class KellyBasic:
  
  def __init__(self, bankroll=20):
    self._B = bankroll
    self._results = []
    
  def get_brankroll(self):
    return self._B
  
  def simulate_days(self, days, p=0.7, b=0.7):
    for d in range(days):
    
      # get Kelly factor
      f = p - (1-p)/b
      
      # calculate wager
      wager = f * self._B
      payout = wager * (1 + b)
      
      # place wager
      self._B -= wager
      
      # simulate game
      r = random.random()
      if r <= 1-p:
        r = 0
      else:
        r = 1
      
      # add back winnings  
      self._B += r * payout
      
      # save off result
      result = Result(result=r, f=f, amount=wager, day=len(self._results)+1, bankroll=self._B, payout=payout)
      self._results.append(result)


if __name__ == '__main__':
  print("Kelly Computations")

  parser = ArgumentParser()
  
  parser.add_argument('-d', '--days', type=int, default=30, help='Number of days to experiment with')
  parser.add_argument('-n', '--monte', type=int, default=100, help='Number of monte carlo runs')
  parser.add_argument('-b', '--bankroll', type=int, default=20, help='Starting bankroll')
  
  args = parser.parse_args()

  for n in range(args.monte):
    k = KellyBasic(args.bankroll)
    k.simulate_days(args.days)
    print(k._B)
