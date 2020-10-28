from matplotlib.animation import FuncAnimation
from random_motion import Molecule
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sgeom


class MolecularView():

    def render_molecules(self):

        for i, ax in enumerate(self.axs):
            m = self.ms[i]
            plt.sca(ax)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            plt.axis("off")
            m.temp, = plt.plot(*m.curr_pos, color=m.m_color, marker='o')
        
        ani = FuncAnimation(self.fig, self.update_all_molecules, interval=10)

        plt.show()

    def update_all_molecules(self, i):
        for i, ax in enumerate(self.axs):
            plt.sca(ax)
            m = (self.ms)[i]
            m.update_molecule(i)

    def __init__(self):
        self.fig, self.axs = plt.subplots(nrows=1, ncols=6)
        self.fig.patch.set_visible(False)
        self.ms = [Molecule() for _ in self.axs]

        self.render_molecules()

if __name__ == "__main__":
    mview = MolecularView()