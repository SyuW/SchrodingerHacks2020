import basic_greenhouse_model
from random_motion import Molecule

from matplotlib.animation import FuncAnimation
from threading import Timer
import matplotlib.pyplot as plt
import numpy as np


EXCITATION_TIME_BEFORE_EMIT = 5

class Photon(Molecule):
    # self figure creation method
    def create_figure_axes(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

    def determine_absorption(self):
        # Probability of absorption dependent on emissivity of atmosphere
        self.got_absorbed = bool(np.random.binomial(n=1, p=basic_greenhouse_model.emv))

    # Override inherited method from Molecule class
    def find_next_position(self):
        return self.next_pos

    def update_photon(self, i):
        self.update_molecule(i)

    def animate_just_photon(self):
        self.create_figure_axes()
        self.temp, = plt.plot(*self.curr_pos, color=self.m_color, marker='o')
        ani = FuncAnimation(self.fig, self.update_photon, interval=10)
        plt.show()

    def __init__(self, set_pos=None):
        Molecule.__init__(self)

        self.reemited = False

        if set_pos == None:
            # Determine start and end points for photon's trajectory
            self.curr_pos   = np.array([np.random.uniform(0.1, 0.9), 0.0])
            self.next_pos   = np.array([np.random.uniform(0.1, 0.9), 1.0])
        else:
            self.curr_pos = np.array(set_pos)
            self.next_pos = np.array([np.random.uniform(0.1, 0.9), 0.0])
            self.reemited = True

        self.displ = self.next_pos - self.curr_pos

        self.reached_end = False
        self.reached_middle = False
        self.got_absorbed = False
        self.speed = 0.01
        self.m_dist_tolerance = 0.01
        self.m_color = "y"


class MolecularView():

    # Call if photon gets absorbed
    def check_region(self, photon):
        for i, bound in enumerate(self.molecule_region_bounds):
            if photon.curr_pos[0] > bound:
                continue
            else:
                return i-1

    def render_molecules(self):
        # Prepare all molecules' axes
        for i, ax in enumerate(self.axs):
            m = self.ms[i]
            plt.sca(ax)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            plt.axis("off")
            m.temp, = plt.plot(*m.curr_pos, color=m.m_color, marker='o')

        ani = FuncAnimation(self.fig, self.update_all_molecules, interval=5)
        plt.show()
        # if the plot window is closed, cancel timer
        self.photon_gen_t.cancel()

    def produce_excitation(self, molecule, region_num):
        molecule.change_state()
        r_photon = Photon(set_pos=[self.interval_length*(region_num+1)-0.05, 0.5])
        plt.sca(self.photon_axes)
        r_photon.temp, = plt.plot(*r_photon.curr_pos, color=r_photon.m_color, marker='o')
        self.photons += [r_photon]

    # Updates the positions of all molecules in grid
    def update_all_molecules(self, frame):
        # Update the grid molecule positions
        for i, ax in enumerate(self.axs):
            is_excited = self.excitations[i]
            plt.sca(ax)
            # update state/position of grid molecule
            m = (self.ms)[i]
            if m.excited != is_excited:
                self.produce_excitation(m, region_num=i)
            m.update_molecule(frame)
        # Update photon's position and don't retain if reached end
        # Alter excitation states for molecules if interaction
        plt.sca(self.photon_axes)
        retained_photons = []
        for p in self.photons:
            p.update_photon(frame)
            # incoming reflected photon
            if p.curr_pos[1] <= 0.01 and p.reemited:
                p.temp.remove()
            # molecule grid interaction
            elif p.curr_pos[1] >= 0.49 and p.curr_pos[1] <= 0.5:
                p.determine_absorption()
                # absorbed
                if p.got_absorbed:
                    region_hit = self.check_region(p)
                    # if molecule is already excited, just transmit
                    if not self.excitations[region_hit]:
                        p.temp.remove()
                        self.excitations[region_hit] = True
                    else:
                        retained_photons += [p]
                # transmitted
                else:
                    retained_photons += [p]
            # photon reached end
            elif p.curr_pos[1] >= 0.99:
                p.temp.remove()
            else:
                retained_photons += [p]
        self.photons = retained_photons

    def generate_photon(self):
        p = Photon()
        p.temp, = plt.plot(*p.curr_pos, color=p.m_color, marker='o')
        self.photons += [p]
        # Poisson generation, avoid 0 values with offset of 1
        # and set next photon generation event
        self.time_before_next_photon = np.random.poisson(1) + 1
        self.photon_gen_t = Timer(self.time_before_next_photon, self.generate_photon)
        self.photon_gen_t.start()

    def __init__(self, num_molecules):
        self.fig, self.axs = plt.subplots(nrows=1, ncols=num_molecules)
        self.fig.patch.set_visible(False)
        self.ms = [Molecule() for _ in self.axs]

        self.interval_length = 1.0 / num_molecules
        self.excitations = [False for m in self.ms]
        self.molecule_region_bounds = [i*self.interval_length
                                       for i in range(len(self.ms))]

        # Photon stuff
        self.photon_axes = self.fig.add_subplot(111)
        self.photon_axes.set_xlim(0, 1)
        self.photon_axes.set_ylim(0, 1)
        plt.axis("off")
        self.photons = []
        self.generate_photon()

        # Start main event loop
        self.render_molecules()

if __name__ == "__main__":
    mview = MolecularView(num_molecules=10)
    # = Photon(set_pos=[0.4, 0.5]).animate_just_photon()
