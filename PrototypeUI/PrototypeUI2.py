"""
This is a prototype UI file for our Schrodinger's Hack project 2020.

It is a simple file to test out the resizing capabilities of the images.

Author: Kondapuram Aditya Seshadri
Date: October 28, 2020
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# This is the class which inherits from the application window object
# and modifies it so that
class MainWindow(QMainWindow):
    # __init__() runs when a new instance of MainWindow is initialized
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # sets the window size to its maximum size
        self.width = QApplication.desktop().screenGeometry().width()
        self.height = QApplication.desktop().screenGeometry().height()

        # setups up all UI elements
        self.setupUI()
        self.show()

        # This timer runs updateUI() every 10 milliseconds
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()

    # setupUI() initializes all the required UI elemets and sets their geometry accordingly
    def setupUI(self):
        self.EarthLabel = QLabel(self)
        self.EarthLabel.setPixmap(QPixmap("EarthDrawn-1.png"))
        self.EarthLabel.setScaledContents(True)

        self.SunLabel = QLabel(self)
        self.SunLabel.setPixmap(QPixmap("SunDrawn.png"))
        self.SunLabel.setScaledContents(True)

        self.setCentralWidget(QWidget())
        self.resize(self.width, self.height)

    # This updates the UI elements to scale wtih the window size
    def updateUI(self):
        sunWidthScale = 0.15
        sunHeightScale = 0.1
        self.width, self.height = self.getScreenSize()
        sunWidth = 0.15 * min(self.width, self.height)
        sunHeight = 0.1 * min(self.width, self.height)

        self.EarthLabel.setGeometry(QRect(0, 0, self.width, self.height))
        self.SunLabel.setGeometry(QRect(0, 0, sunWidth, sunHeight))

    # returns the length and width of the current window size
    def getScreenSize(self):
        return self.centralWidget().frameSize().width(), self.centralWidget().frameSize().height()

# main() runs at program initialization, sets up the application window objects handle
# executes them
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

# initializes the main() function at program initialization
if __name__ == '__main__':
    main()
