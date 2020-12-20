# Generates histogram for given data
import argparse
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import math

def generatePlots(nodes_processed, x_label, y_label, title, file_name):
    n_bins = 10
    # Creating histogram
    fig, axs = plt.subplots(1, 1,
                            figsize=(10, 7),
                            tight_layout=True)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        axs.spines[s].set_visible(False)

    # Remove x, y ticks
    axs.xaxis.set_ticks_position('none')
    axs.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    axs.xaxis.set_tick_params(pad=5)
    axs.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    axs.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.6)

    # Creating histogram
    N, bins, patches = axs.hist(nodes_processed, bins=n_bins)

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # Adding extra features

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Show plot
    plt.savefig(file_name)

