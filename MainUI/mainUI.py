"""
This is the main IU file for Team 17B's Schrodinger's Hack Project 2020.

Author: Kondapuram Aditya Seshadri, Saral Shah
Date: October 29, 2020
"""

import sys
sys.path.append("..")
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import basic_greenhouse_model


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
        self.setCentralWidget(QWidget())

        self.EarthViewSetup()
        self.sliderSetup()
        self.setupFluxLines()

        self.resize(self.width, self.height)

    # This updates the UI elements to scale wtih the window size
    # Pass box visualization through here later - Sam
    def updateUI(self):
        sunWidthScale = 0.4
        sunHeightScale = 0.35
        self.width, self.height = self.getScreenSize()
        self.sunWidth = sunWidthScale * min(self.width, self.height)
        self.sunHeight = sunHeightScale * min(self.width, self.height)

        self.EarthLabel.setGeometry(QRect(0, 0, self.width, self.height))
        self.SunLabel.setGeometry(QRect(-self.sunWidth / 2, -self.sunHeight / 2 , self.sunWidth, self.sunHeight))

        self.updateSlider()

    # returns the length and width of the current window size
    def getScreenSize(self):
        return self.centralWidget().frameSize().width(), self.centralWidget().frameSize().height()

    def EarthViewSetup(self):
        self.EarthLabel = QLabel(self)
        self.EarthLabel.setPixmap(QPixmap("EarthDrawn-1.png"))
        self.EarthLabel.setScaledContents(True)

        self.SunLabel = QLabel(self)
        self.SunLabel.setPixmap(QPixmap("SunDrawn.png"))
        self.SunLabel.setScaledContents(True)

    def sliderSetup(self):
        # These are values required by the wavelength slider
        min_wavelength = 1
        max_wavelength = 100
        wavelength_step = 10
        start_wavelength = 0

        # These are the values required by the albedo and emissivity sliders
        albedo_step = 0.05
        self.albedo_scale = 100
        start_albedo = 0

        emissivity_step = 0.05
        self.emissivity_scale = 100
        start_emissivity = 0

        # general constants used by all sliders
        slider_width = 200
        slider_height = 20

        # buffer space around sliders
        x_buffer = 10
        y_buffer = 0

        # these are the positions such that all the sliders are in the top right corner
        # of the application window (including buffer space)
        x_slider = self.width - slider_width - (x_buffer / 2)
        y_slider = slider_height + (y_buffer / 2)

        # the width and heights of the text boxes and their positions
        # including the buffer space for the sliders
        text_width = 150
        text_height = slider_height
        x_text = x_slider - (x_buffer / 2) - text_width
        y_text = y_slider

        # sets up all the sliders in the scene
        self.wavelengthSlider = QSlider(self)
        self.wavelengthSlider.setGeometry(QRect(x_slider, y_slider,
                                                slider_width, slider_height))
        self.wavelengthSlider.setMinimum(min_wavelength)
        self.wavelengthSlider.setMaximum(max_wavelength)
        self.wavelengthSlider.setSingleStep(wavelength_step)
        self.wavelengthSlider.setOrientation(Qt.Horizontal)
        self.wavelengthSlider.setSliderPosition(start_wavelength)

        self.albedoSlider = QSlider(self)
        self.albedoSlider.setGeometry(QRect(x_slider, y_slider + slider_height,
                                            slider_width, slider_height))
        self.albedoSlider.setMinimum(0)
        self.albedoSlider.setMaximum(100)
        self.albedoSlider.setSingleStep(albedo_step * self.albedo_scale)
        self.albedoSlider.setOrientation(Qt.Horizontal)
        self.albedoSlider.setSliderPosition(start_albedo)


        self.emissivitySlider = QSlider(self)
        self.emissivitySlider.setGeometry(QRect(x_slider, y_slider + 2 * slider_height,
                                            slider_width, slider_height))
        self.emissivitySlider.setMinimum(0)
        self.emissivitySlider.setMaximum(100)
        self.emissivitySlider.setSingleStep(emissivity_step * self.emissivity_scale)
        self.emissivitySlider.setOrientation(Qt.Horizontal)
        self.emissivitySlider.setSliderPosition(start_albedo)


        # sets up all text for the slider in the scene
        self.wavelengthLabel = QLabel(self)
        self.wavelengthLabel.setGeometry(QRect(x_text, y_text, text_width, text_height))

        self.albedoLabel = QLabel(self)
        self.albedoLabel.setGeometry(QRect(x_text, y_text + slider_height,
                                           text_width, text_height))

        self.emissivityLabel = QLabel(self)
        self.emissivityLabel.setGeometry(QRect(x_text, y_text + (2 * slider_height),
                                           text_width, text_height))


    def updateSlider(self):
        # updates the values of the sliders as stored in memory
        self.wavelengthValue = self.wavelengthSlider.value()
        self.albedoValue = self.albedoSlider.value()
        self.emissivityValue = self.emissivitySlider.value()

        # general constants used by all sliders
        slider_width = 200
        slider_height = 20

        # buffer space around sliders
        x_buffer = 10
        y_buffer = 0

        # these are the positions such that all the sliders are in the top right corner
        # of the application window (including buffer space)
        x_slider = self.width - slider_width - (x_buffer / 2)
        y_slider = slider_height + (y_buffer / 2)

        # the width and heights of the text boxes and their positions
        # including the buffer space for the sliders
        text_width = 150
        text_height = slider_height
        x_text = x_slider - (x_buffer / 2) - text_width
        y_text = y_slider

        # updates text associated to all the sliders
        # wavelength units changed to micrometers -Sam
        self.wavelengthLabel.setText("Wavelength: %d \u03BCm" % self.wavelengthValue)
        self.albedoLabel.setText("Albedo: %g" % (self.albedoValue / self.albedo_scale))
        self.emissivityLabel.setText("Emissivity: %g" % (self.emissivityValue / self.albedo_scale))

        # moves the labels and sliders to match the screen dimensions
        self.wavelengthSlider.move(x_slider, y_slider)
        self.wavelengthLabel.move(x_text, y_text)
        self.albedoSlider.move(x_slider, y_slider + slider_height)
        self.albedoLabel.move(x_text, y_text + slider_height)
        self.emissivitySlider.move(x_slider, y_slider + (2 * slider_height))
        self.emissivityLabel.move(x_text, y_text + (2 * slider_height))

    def setupFluxLines(self):
        # Moved sunWidths and scales to this function because they were called
        # before being defined -Sam
        sunWidthScale = 0.4
        sunHeightScale = 0.35
        self.sunWidth = sunWidthScale * min(self.width, self.height)
        self.sunHeight = sunHeightScale * min(self.width, self.height)

        lineup = QPixmap("LineUp.png")
        linedown = QPixmap("LineDown.png")

        self.incidentSunFlux = QLabel(self)
        self.incidentSunFlux.setPixmap(linedown)
        self.incidentSunFlux.setGeometry(self.sunWidth / 2, self.sunHeight / 2, 200, 200)

        """
        self.reflectedSunFlux = QLabel(self)
        self.reflectedSunFlux.setPixmap(lineup)
        self.transmittedSunFlux = QLabel(self)
        self.transmittedSunFlux.setPixmap(linedown)
        self.surfaceEmittedFlux = QLabel(self)
        self.surfaceEmittedFlux.setPixmap(lineup)
        self.transmittedSurfaceFlux = QLabel(self)
        self.transmittedSurfaceFlux.setPixmap(lineup)
        self.reflectedSurfaceFlux = QLabel(self)
        self.reflectedSurfaceFlux.setPixmap(linedown)
        """

    def updateFluxLines(self):
        opacity_effect = QGraphicsOpacityEffect()

        opacity_effect.setOpacity(1)

def reqWidthHeight(x_i, y_i, x_f, y_f):
    return (x_f - x_i), (y_f - y_i)

# main() runs at program initialization, sets up the application window objects handle
# executes them
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

# initializes the main() function at program initialization
if __name__ == '__main__':
    main()
