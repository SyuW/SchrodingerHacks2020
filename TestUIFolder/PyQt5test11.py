"""
This is a simple test file for working out how to use PyQt5 for our Schrodinger's Hack project.

This test file uses multithreading to handle timers.

Author: Kondapuram Aditya Seshadri
Date: October 28, 2020
"""

# importing all necessary dependencies
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time

# the application window object
class MainWindow(QMainWindow):
    # initializes all required elements in the application window
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # QThreadPool() is used to create new threads inside of a PyQt5 application
        self.threadpool = QThreadPool()
        self.counter = 0
        self.UISetup()

        # sets up a QTimer, which functions as a timer
        self.timer = QTimer()
        # the timer resets and begins again every 1000ms (1 sec)
        self.timer.setInterval(1000)
        # when the timer runs out, recurring_timer() is called
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    # sets up all UI elements in the scene including the layout
    def UISetup(self):
        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("Press Me!")
        b.pressed.connect(self.bpush)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

    # If the button is pushed, then the program cretes a Worker() thread and sleeps for 5 seconds
    def bpush(self):
        # a new instance of the Worker() class is created
        worker = Worker()
        # a new thread is started using the worker object for event handling
        self.threadpool.start(worker)

    # At the end of every timer cycle, we display how many times the button has been pressed
    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)


# This is an object which will be instantiated when the button is pressed and will
# show the current progress on how much time has passed
class Worker(QRunnable):
    """
    This is the worker thread
    """

    @pyqtSlot()
    # this is called when a thread is started using a Worker() isntnace
    def run(self):
        # over 5 seconds
        for i in range(5):
            # prints the progress to the command window
            print("%d%% Done!" % (((i + 1) / 5) * 100))
            #sleeps for 1 second
            time.sleep(1)

# main() sets up the application window and executes the code for the GUI
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

# runs the main() function at initialization
if __name__ == '__main__':
    main()
