from matplotlib.animation import FuncAnimation
from pathlib import Path
from threading import Timer
import matplotlib.pyplot as plt
import numpy as np


GROUND_STATE_MAX_RADIUS = 0.15; EXCITED_STATE_MAX_RADIUS = 0.30
GROUND_SPEED            = 0.10; EXCITED_SPEED            = 0.20
MOLECULE_TYPES_TO_COLORS = {"CO2": "r",
                            "H2O": "cornflowerblue",
                            "CH4": "k",
                            "O3" : "b"}


def state_transition_test():
    m = Molecule()
    t = Timer(5.0, m.change_state)
    t.start()
    m.construct_fig_axes()
    m.animate_molecule()
    t.cancel()


class Molecule():

    def find_next_position(self):
        # Sample random polar coords, so that molecule stays in circular region
        r = np.random.uniform(0, self.rmax)
        theta = np.random.uniform(0, 2*np.pi)

        return np.array([r*np.cos(theta), r*np.sin(theta)])

    def update_molecule(self, i):
        # If not reached yet, move towards next position
        dist = np.linalg.norm(self.curr_pos - self.next_pos)
        if dist > self.m_dist_tolerance:
            self.temp.remove()
            self.curr_pos += self.displ * self.speed
            self.temp, = plt.plot(*self.curr_pos, color=self.m_color, marker='o')

        # If reached next position, set new position and determine displacement
        else:
            self.next_pos = self.find_next_position()
            self.displ = self.next_pos - self.curr_pos

    def change_state(self):
        if self.excited:
            self.excited = False
        else:
            self.excited = True
        self.set_state()
        # Reintialize positions so that molecule doesn't fly off
        # from speed change
        self.curr_pos = np.array([0., 0.])
        self.next_pos = np.array([0., 0.])
        self.displ = self.curr_pos - self.next_pos

    def set_state(self):
        if self.excited:
            self.rmax = EXCITED_STATE_MAX_RADIUS
            self.speed = EXCITED_SPEED
        else:
            self.rmax = GROUND_STATE_MAX_RADIUS
            self.speed = GROUND_SPEED

    def animate_molecule(self):
        # Store the molecule's current position as a temp value for updating
        self.temp, = plt.plot(*self.curr_pos, color=self.m_color, marker='o')
        ani = FuncAnimation(self._fig, self.update_molecule, interval=10)
        plt.show()

    def construct_fig_axes(self):
        self._fig = plt.figure()
        self._ax = self._fig.add_axes([0, 0, 1, 1], frameon=True)

        self._ax.set_xlim(-1, 1)
        self._ax.set_ylim(-1, 1)

    def __init__(self):

        self.m_color = 'g'
        self.m_dist_tolerance = 0.1
        self.excited = False
        self.set_state()

        # Initialize position variables to origin
        self.curr_pos = np.array([0., 0.])
        self.next_pos = np.array([0., 0.])
        self.displ = self.curr_pos - self.next_pos


if __name__ == "__main__":
    state_transition_test()
