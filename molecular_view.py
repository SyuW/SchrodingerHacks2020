from matplotlib.animation import FuncAnimation
from random_motion import Molecule
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sgeom


def render_molecules():
    fig, axs = plt.subplots(nrows=2, ncols=3)
    fig.patch.set_visible(False)
    for ax in fig.axes: 
        ax.axis('on')
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
        mol = Molecule(excited=False, _fig=fig, _ax=ax)

    plt.show()


if __name__ == "__main__":
    render_molecules()