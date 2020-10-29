"""
This is a simple test file for working out how to use PyQt5 for our Schrodinger's Hack project.

This file simply creates a window application with some imported images.

Author: Kondapuram Aditya Seshadri
Date: October 24, 2020
"""

# importing the required dependencies
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
# importing the module containing the scnene information
from TestUI import Ui_MainWindow

# this class creates a new window
class MainWindow(QMainWindow, Ui_MainWindow):
    # run at the initialization of a anew instance of this class
    def __init__(self):
        # runs the __init__() for each of the superclasses
        super().__init__()

        # runs the method responsible for creating and populating the scene/application window
        self.setupUi(self)

        # displays the application window
        self.show()

# main() is run at initialization and sets up the required objects to create the application
# and its window
def main():
    # creates an instance of the application
    app = QApplication(sys.argv)

    # creates and isntance of the application window and displays it
    win = MainWindow()

    # shuts down the program safely when the user exits the application
    sys.exit(app.exec_())

# runs the program at initialization of this file
if __name__ == '__main__':
    main()
