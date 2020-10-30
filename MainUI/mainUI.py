"""
This is the main IU file for Team 17B's Schrodinger's Hack Project 2020.

Author: Kondapuram Aditya Seshadri, Saral Shah
Date: October 29, 2020
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import basic_greenhouse_model as gmodel
from molecular_view import MolecularView

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
        self.setupFluxLines()
        self.sliderSetup()

        self.EarthTempLabel = QLabel(self)
        self.AtmosTempLabel = QLabel(self)

        self.setWindowTitle("Interactive Climate Model")
        self.resize(self.width, self.height)

    # This updates the UI elements to scale wtih the window size
    def updateUI(self):
        self.width, self.height = self.getScreenSize()
        self.albedoValue = self.albedoSlider.value()
        self.emissivityValue = self.emissivitySlider.value()
        self.T_s, self.T_a, self.green_perc, self.planet_perc, self.surface_perc = gmodel.run((self.albedoValue / self.albedo_scale),
                                                                                   (self.emissivityValue / self.emissivity_scale))

        #print(f"Atmosphere Temp: {self.T_a - 273.15}")
        #print(f"Surface Temp: {self.T_s - 273.15}")

        self.updateSlider()
        self.updateEarthView()
        self.updateFluxLines()

    def updateEarthView(self):
        sunWidthScale = 0.4
        sunHeightScale = 0.35
        self.sunWidth = sunWidthScale * min(self.width, self.height)
        self.sunHeight = sunHeightScale * min(self.width, self.height)

        self.EarthLabel.setGeometry(QRect(0, 0, self.width, self.height))
        self.SunLabel.setGeometry(QRect(-self.sunWidth / 2, -self.sunHeight / 2,
                                        self.sunWidth, self.sunHeight))

        self.EarthTempLabel.setGeometry(self.width / 2 - 145, 0.9 * self.height, 200, 45)
        self.AtmosTempLabel.setGeometry(self.width / 2 - 135, 0.45 * self.height, 200, 45)

        self.EarthTempLabel.setText("Surface Temp: %g\u2103" % round(self.T_s - 273.15, 1))
        self.AtmosTempLabel.setText(f"Air Temp: %g\u2103" % round(self.T_a - 273.15, 1))

    # returns the length and width of the current window size
    def getScreenSize(self):
        return self.centralWidget().frameSize().width(), self.centralWidget().frameSize().height()

    def EarthViewSetup(self):
        sunWidthScale = 0.4
        sunHeightScale = 0.35
        self.sunWidth = sunWidthScale * min(self.width, self.height)
        self.sunHeight = sunHeightScale * min(self.width, self.height)

        self.EarthLabel = QLabel(self)
        self.EarthLabel.setPixmap(QPixmap("EarthDrawn.png"))
        self.EarthLabel.setScaledContents(True)

        self.SunLabel = QLabel(self)
        self.SunLabel.setPixmap(QPixmap("SunDrawn.png"))
        self.SunLabel.setScaledContents(True)

    def sliderSetup(self):
        # These are the values required by the albedo and emissivity sliders
        albedo_step = 0.05
        self.albedo_scale = 100
        start_albedo = 0.3 * self.albedo_scale

        emissivity_step = 0.05
        self.emissivity_scale = 100
        start_emissivity = 0.75 * self.emissivity_scale

        # sets up all the sliders in the scene
        self.albedoSlider = QSlider(self)
        self.albedoSlider.setMinimum(0)
        self.albedoSlider.setMaximum(100)
        self.albedoSlider.setSingleStep(albedo_step * self.albedo_scale)
        self.albedoSlider.setOrientation(Qt.Horizontal)
        self.albedoSlider.setSliderPosition(start_albedo)


        self.emissivitySlider = QSlider(self)
        self.emissivitySlider.setMinimum(10)
        self.emissivitySlider.setMaximum(100)
        self.emissivitySlider.setSingleStep(emissivity_step * self.emissivity_scale)
        self.emissivitySlider.setOrientation(Qt.Horizontal)
        self.emissivitySlider.setSliderPosition(start_emissivity)


        # sets up all text for the slider in the scene
        self.albedoLabel = QLabel(self)
        self.emissivityLabel = QLabel(self)


    def updateSlider(self):
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
        self.albedoLabel.setText("Albedo: %g" % (self.albedoValue / self.albedo_scale))
        self.emissivityLabel.setText("Emissivity: %g" % (self.emissivityValue / self.albedo_scale))

        # moves the labels and sliders to match the screen dimensions
        self.albedoSlider.setGeometry(QRect(x_slider, y_slider,
                                            slider_width, slider_height))
        self.emissivitySlider.setGeometry(QRect(x_slider, y_slider + slider_height,
                                            slider_width, slider_height))
        self.albedoLabel.setGeometry(QRect(x_text, y_text,
                                           text_width, text_height))
        self.emissivityLabel.setGeometry(QRect(x_text, y_text + slider_height,
                                           text_width, text_height))

    def setupFluxLines(self):
        lineup = QPixmap("LineUp.png")
        linedown = QPixmap("LineDown.png")

        self.incidentSunFlux = QLabel(self)
        self.incidentSunFlux.setPixmap(linedown)
        self.incidentSunFlux.setScaledContents(True)

        self.reflectedSunFlux = QLabel(self)
        self.reflectedSunFlux.setPixmap(lineup)
        self.reflectedSunFlux.setScaledContents(True)

        self.transmittedSunFlux = QLabel(self)
        self.transmittedSunFlux.setPixmap(linedown)
        self.transmittedSunFlux.setScaledContents(True)

        self.surfaceEmittedFlux = QLabel(self)
        self.surfaceEmittedFlux.setPixmap(lineup)
        self.surfaceEmittedFlux.setScaledContents(True)

        self.transmittedSurfaceFlux = QLabel(self)
        self.transmittedSurfaceFlux.setPixmap(lineup)
        self.transmittedSurfaceFlux.setScaledContents(True)

        self.reflectedSurfaceFlux = QLabel(self)
        self.reflectedSurfaceFlux.setPixmap(linedown)
        self.reflectedSurfaceFlux.setScaledContents(True)

    def updateFluxLines(self):
        opacity_full = QGraphicsOpacityEffect()
        opacity_albedo = QGraphicsOpacityEffect()
        opacity_albedo_left = QGraphicsOpacityEffect()
        opacity_emissivity = QGraphicsOpacityEffect()
        opacity_emissivity_trans = QGraphicsOpacityEffect()
        opacity_emissivity_refl = QGraphicsOpacityEffect()

        opacity_full.setOpacity(1)
        opacity_albedo.setOpacity(self.albedoValue / self.albedo_scale)
        opacity_albedo_left.setOpacity((1 - (self.albedoValue / self.albedo_scale)))
        opacity_emissivity.setOpacity(self.surface_perc)
        opacity_emissivity_refl.setOpacity(self.green_perc)
        opacity_emissivity_trans.setOpacity(self.planet_perc)

        self.incidentSunFlux.setGraphicsEffect(opacity_full)
        self.incidentSunFlux.setGeometry((self.sunWidth / 4), (self.sunHeight / 4),
                                         self.width * 0.14, self.height * 0.25)

        self.reflectedSunFlux.setGraphicsEffect(opacity_albedo)
        self.reflectedSunFlux.setGeometry((self.sunWidth / 4) + (self.width * 0.14),
                                          (self.sunHeight / 4), self.width * 0.14, self.height * 0.25)

        self.transmittedSunFlux.setGraphicsEffect(opacity_albedo_left)
        self.transmittedSunFlux.setGeometry((self.sunWidth / 4) + (self.width * 0.14),
                                            (self.sunHeight / 4) + (self.height * 0.25),
                                            self.width * 0.18, self.height * 0.3)

        self.surfaceEmittedFlux.setGraphicsEffect(opacity_emissivity)
        self.surfaceEmittedFlux.setGeometry((self.sunWidth / 4) + (self.width * 0.5),
                                            (self.sunHeight / 4) + (self.height * 0.25),
                                            self.width * 0.18, self.height * 0.3)

        self.transmittedSurfaceFlux.setGraphicsEffect(opacity_emissivity_trans)
        self.transmittedSurfaceFlux.setGeometry((self.sunWidth / 4) + (self.width * 0.68),
                                                (self.sunHeight / 4) - (self.height * 0.05),
                                                self.width * 0.18, self.height * 0.3)

        self.reflectedSurfaceFlux.setGraphicsEffect(opacity_emissivity_refl)
        self.reflectedSurfaceFlux.setGeometry((self.sunWidth / 4) + (self.width * 0.68),
                                                (self.sunHeight / 4) + (self.height * 0.25),
                                                self.width * 0.18, self.height * 0.3)

    # Method for running molecular visualization; spawn another thread
    def create_molecular_view(self):
        mview = MolecularView()
        mview.start_animation_loop()

# main() runs at program initialization, sets up the application window objects handle
# executes them
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

# initializes the main() function at program initialization
if __name__ == '__main__':
    main()
