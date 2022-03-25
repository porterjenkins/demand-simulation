import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def plt_cumulative_rewards(eps_rewards, fname='step-plt.png', show=False):

    fig, axs = plt.subplots(
        nrows=len(eps_rewards),
        ncols=1,
        figsize=(12, 8),
        sharex=True,
        sharey=True
    )

    i = 0
    for disp, disp_data in eps_rewards.items():
        for prod, ts in disp_data.items():
            cumsum = np.cumsum(ts)
            x = np.arange(len(cumsum))
            axs[i].plot(x, cumsum, label=prod)
            axs[i].set_title(disp)

        i += 1

    plt.xlabel("Step")
    plt.ylabel("Revenue")
    #axs.set_xlabel("Step")
    #axs.set_ylabel("Revenue")
    plt.legend(loc="best")

    if show:
        plt.show()
    else:
        plt.savefig(fname)


def plot_traffic(ts, traffic, fname="traffic.png", show=False):
    plt.figure(figsize=(12, 8))
    plt.plot(ts, traffic, "--", marker='o', c='red')
    plt.xlabel("Datetime")
    plt.ylabel("Number of Agents")
    plt.xticks(rotation=45)
    if show:
        plt.show()
    else:
        plt.savefig(fname)