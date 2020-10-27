from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


class Molecule():

    def find_next_position(self):
        r = np.random.uniform(0, 1)
        theta = np.random.uniform(0, 2*np.pi)

        return np.array([r*np.cos(theta), r*np.sin(theta)])

    def update(self, i):

        if np.linalg.norm(diff) > 0.1:
            self.curr_pos += self.displ*0.01
            plt.plot(*diff, 'ro')
        
        else:
            self.finish_pos = self.find_next_position()
            self.displ = self.curr_pos - self.finish_pos
        
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])

    def excited_state(self):
        self.speed = 8

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1], frameon=True)
        
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.curr_pos = np.array([0, 0])
        self.next_pos = np.array([0, 0])
        self.speed = 2
        self.excited = False

        animation = FuncAnimation(self.fig, self.update, interval=10)
        plt.show()


if __name__ == "__main__":
    foo = Molecule()