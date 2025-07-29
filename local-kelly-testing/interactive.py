import kelly
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

k = kelly.KellyAdaptive(20)
k.simulate_days(100)

