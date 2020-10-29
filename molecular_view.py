from matplotlib.animation import FuncAnimation
from random_motion import Molecule
from threading import Timer
import matplotlib.pyplot as plt
import numpy as np


class Photon(Molecule):

    def create_figure_axes(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

    def determine_transmission_reflection(self):
        self.reflect_off = bool(np.random.randint(2)) #flip a coin

    # Override inherited method from Molecule class
    def find_next_position(self):
        return self.next_pos

    def update_photon(self, i):
        self.update_molecule(i)
        if self.curr_pos[1] >= 0.49 and self.curr_pos[1] <= 0.51:
            self.reached_middle = True
            self.determine_transmission_reflection()
        if self.curr_pos[1] >= 0.99:
            self.reached_end = True
            self.temp.remove()

    def animate_just_photon(self):
        self.create_figure_axes()
        self.temp, = plt.plot(*self.curr_pos, color=self.m_color, marker='o')
        ani = FuncAnimation(self.fig, self.update_photon, interval=10)
        plt.show()

    def __init__(self):
        Molecule.__init__(self)

        # Determine start and end points for photon's trajectory
        self.curr_pos   = np.array([np.random.uniform(0.1, 0.9), 0.0])
        self.next_pos   = np.array([np.random.uniform(0.1, 0.9), 1.0])
        self.displ      = self.next_pos - self.curr_pos

        self.reached_end = False
        self.reached_middle = False
        self.reflect_off = False
        self.speed = 0.01
        self.m_dist_tolerance = 0.01
        self.m_color = "y"


class MolecularView():

    def render_molecules(self):
        # Prepare all molecules' axes
        for i, ax in enumerate(self.axs):
            m = self.ms[i]
            plt.sca(ax)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            plt.axis("off")
            m.temp, = plt.plot(*m.curr_pos, color=m.m_color, marker='o')
        # Prepare the photon's axes
        plt.sca(self.photon_axes)
        for p in self.photons:
            p.temp, = plt.plot(*p.curr_pos, color=p.m_color, marker='o')

        ani = FuncAnimation(self.fig, self.update_all_molecules, interval=5)
        plt.show()

    # Updates the positions of all molecules in grid
    def update_all_molecules(self, i):
        # Update the grid molecule positions
        for i, ax in enumerate(self.axs):
            plt.sca(ax)
            m = (self.ms)[i]
            m.update_molecule(i)
        # Update photon's position and don't retain if reached end
        plt.sca(self.photon_axes)
        retained_photons = []
        for p in self.photons:
            p.update_photon(i)
            if p.reached_middle:
                pass
            if not p.reached_end:
                retained_photons += [p]
        self.photons = retained_photons

    def generate_photon(self):
        self.photons += [Photon()]

        self.time_before_next_photon = np.random.poisson(1) + 1 # average of one sec between photons

        return

    def __init__(self, num_molecules):
        self.fig, self.axs = plt.subplots(nrows=1, ncols=num_molecules)
        self.fig.patch.set_visible(False)
        self.ms = [Molecule() for _ in self.axs]

        self.photon_axes = self.fig.add_subplot(111)
        self.photon_axes.set_xlim(0, 1)
        self.photon_axes.set_ylim(0, 1)
        plt.axis("off")

        self.photons = []
        self.generate_photon()

        self.render_molecules()

if __name__ == "__main__":
    mview = MolecularView(num_molecules=10)
    #p = Photon().animate_just_photon()
