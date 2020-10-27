from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


class Molecule():

    def find_next_position(self):
        r = np.random.uniform(0, 1)
        theta = np.random.uniform(0, 2*np.pi)

        return np.array([r*np.cos(theta), r*np.sin(theta)])

    def update(self, i):
        dist = np.linalg.norm(self.curr_pos - self.next_pos)

        if dist > 0.1:
            self.temp.remove()
            self.fig.canvas.draw_idle()
            self.curr_pos += self.displ*0.05
            self.temp, = plt.plot(*self.curr_pos, 'ro') 
        
        else:
            self.next_pos = self.find_next_position()
            self.displ = self.next_pos - self.curr_pos

    def excited_state(self):
        self.speed = 8

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1], frameon=True)
        
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)

        self.curr_pos = np.array([0., 0.])
        self.next_pos = np.array([0., 0.])
        self.displ = self.curr_pos - self.next_pos

        self.speed = 2
        self.excited = False

        self.temp, = plt.plot(*self.curr_pos, 'ro') 
        animation = FuncAnimation(self.fig, self.update, interval=1)
        plt.show()


if __name__ == "__main__":
    foo = Molecule()