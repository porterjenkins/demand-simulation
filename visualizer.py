import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def plt_cumulative_rewards(eps_rewards, fname='step-plt.png', show=False):

    for k, v in eps_rewards.items():
        cumsum = np.cumsum(v)
        x = np.arange(len(cumsum))
        plt.plot(x, cumsum, label=k)
        plt.xlabel("Step")
        plt.ylabel("Revenue")
        plt.legend(loc="best")

    if show:
        plt.show()
    else:
        plt.savefig(fname)
