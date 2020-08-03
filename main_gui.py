import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import os
import utils
import json
import datetime
import calibration

Ui_MainWindow, QMainWindow = loadUiType("main_gui.ui")


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

        # monitor related stuff
        self.screen_distance.setText("57")
        self.screen_size.setText("22")
        self.screen_height.setText("1050")
        self.screen_width.setText("1680")

        # calibration stuff
        self.calibration_reward_duration.setText("0.5")
        self.calibration_target_size.setText("1.0")
        self.calibration_type.addItem("3 points")
        self.calibration_type.addItem("5 points")
        self.calibration_type.addItem("9 points")
        self.calibration_type.addItem("13 points")
        self.calibration_target_color.addItem("white")
        self.calibration_target_color.addItem("yellow")
        self.calibration_target_color.addItem("blue")
        self.calibration_stimulus.addItem("Image...")
        self.calibration_stimulus.addItem("Gabor patch")
        self.calibration_stimulus.addItem("Circle")
        self.calibration_stimulus.setCurrentIndex(2)
        self.calibration_stimulus.activated.connect(self.set_calibration_image)
        self.manual_calibration.setChecked(False)
        self.calibration_start.clicked.connect(self.start_calibration)

        # results
        self.results = {}
        self.combos = []

    def set_calibration_image(self):
        if self.calibration_stimulus.currentText() == "Image...":
            filters = "Image and movie files (*.jpg *.tiff *.png *.mp4)"
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Set calibration image", os.getcwd(),
                                                             filters)
            if filename:
                idx = self.calibration_stimulus.findText(filename, QtCore.Qt.MatchFixedString)
                if idx < 0:  # not found, so add it
                    self.calibration_stimulus.addItem(filename)
                    idx = self.calibration_stimulus.findText(filename, QtCore.Qt.MatchFixedString)
                self.calibration_stimulus.setCurrentIndex(idx)

    def load(self):
        filters = "Settings files (*_settings.txt)"
        # TODO: Why is this not resolving symoblic links?
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load settings",
                                                            os.path.join(os.getcwd(),self.data_dir), filters)
        if filename:
            exp_info = json.load(open(str(filename), "r"))
            self.screen_width.setText(str(exp_info.get("screen_width", 1680)))
            self.screen_height.setText(str(exp_info.get("screen_height", 1080)))
            self.screen_size.setText(str(exp_info.get("screen_size", 25)))
            self.screen_distance.setText(str(exp_info.get("screen_distance", 57)))

            self.serial_path.setText(str(exp_info.get("serial_port", "")))

            #  calibration
            self.calibration_reward_duration.setText(str(exp_info.get("calibration_reward_duration", 0.5)))
            self.calibration_target_size.setText(str(exp_info.get("calibration_target_size", 1.0)))
            calib_type = exp_info.get("calibration_type", "9 points")
            idx = self.calibration_type.findText(calib_type, QtCore.Qt.MatchFixedString)
            if idx >= 0:
                self.calibration_type.setCurrentIndex(idx)
            calib_color = exp_info.get("calibration_target_color", "white")
            idx = self.calibration_target_color.findText(calib_color, QtCore.Qt.MatchFixedString)
            if idx >= 0:
                self.calibration_target_color.setCurrentIndex(idx)

            calibration_stim = exp_info.get("calibration_stimulus", "Circle")
            idx = self.calibration_stimulus.findText(calibration_stim)
            if idx >= 0:
                self.calibration_stimulus.setCurrentIndex(idx)
            else:
                self.calibration_stimulus.addItem(calibration_stim)
            self.manual_calibration.setChecked(exp_info.get("manual_calibration", False))

    def saveas(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save settings",
                                                     os.path.join(os.getcwd(),self.data_dir))
        if filename:
            exp_info = self.get_settings()
            json.dump(exp_info, open(filename, "w"))


    def get_settings(self):
        screen_width = float(self.screen_width.text())
        screen_height = float(self.screen_height.text())
        screen_distance = float(self.screen_distance.text())
        screen_size = float(self.screen_size.text())
        serialpath = str(self.serial_path.text())

        # calibration stuff
        calibration_reward_duration = float(self.calibration_reward_duration.text())
        calibration_target_size = float(self.calibration_target_size.text())
        calibration_target_color = str(self.calibration_target_color.currentText())
        calibration_type = str(self.calibration_type.currentText())
        calibration_stimulus = str(self.calibration_stimulus.currentText())
        manual_calibration = self.manual_calibration.isChecked()

        exp_info = {"screen_width": screen_width,
                    "screen_height": screen_height,
                    "screen_size": screen_size,
                    "screen_distance": screen_distance,
                    "serial_port": serialpath,
                    "calibration_reward_duration": calibration_reward_duration,
                    "calibration_target_size": calibration_target_size,
                    "calibration_type": calibration_type,
                    "calibration_target_color": calibration_target_color,
                    "calibration_stimulus": calibration_stimulus,
                    "manual_calibration": manual_calibration}
        return exp_info

    def start_calibration(self):
        exp_info = self.get_settings()
        calibration.start_calibration(exp_info)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())
