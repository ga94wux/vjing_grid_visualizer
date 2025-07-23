from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject

class Param(QObject):
    updated = pyqtSignal(float, float, float, float, float, float, float, bool)

class ControlWindow(QtWidgets.QWidget):
    def __init__(self, param):
        super().__init__()
        self.param = param
        self.init_ui()

    def init_ui(self):
        self.slider_amp = self.create_slider(30, 0, 100)
        self.slider_freq = self.create_slider(10, 0, 100)
        self.slider_speed = self.create_slider(20, 0, 100)
        self.slider_rot = self.create_slider(20, 0, 100)
        self.slider_zoom = self.create_slider(50, 15, 100)
        self.slider_color = self.create_slider(130, 0, 360)
        self.slider_sens = self.create_slider(100, 1, 300)
        self.checkbox_auto = QtWidgets.QCheckBox("Automatik")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Amplitude"))
        layout.addWidget(self.slider_amp)
        layout.addWidget(QtWidgets.QLabel("Frequency"))
        layout.addWidget(self.slider_freq)
        layout.addWidget(QtWidgets.QLabel("Wave Speed"))
        layout.addWidget(self.slider_speed)
        layout.addWidget(QtWidgets.QLabel("Rotation Speed"))
        layout.addWidget(self.slider_rot)
        layout.addWidget(QtWidgets.QLabel("Zoom"))
        layout.addWidget(self.slider_zoom)
        layout.addWidget(QtWidgets.QLabel("Color (Hue)"))
        layout.addWidget(self.slider_color)
        layout.addWidget(QtWidgets.QLabel("Sensitivity"))
        layout.addWidget(self.slider_sens)
        layout.addWidget(self.checkbox_auto)

        self.setLayout(layout)
        self.setWindowTitle("Control Panel")
        self.show()

        self.slider_changed()

        for s in [self.slider_amp, self.slider_freq, self.slider_speed,
                  self.slider_rot, self.slider_zoom, self.slider_color,
                  self.slider_sens, self.checkbox_auto]:
            s.valueChanged.connect(self.slider_changed) if isinstance(s, QtWidgets.QSlider) else s.stateChanged.connect(self.slider_changed)

    def create_slider(self, default=50, min_val=0, max_val=100):
        slider = QtWidgets.QSlider()
        slider.setOrientation(1)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        return slider

    def slider_changed(self):
        amp = self.slider_amp.value() / 10.0
        freq = self.slider_freq.value() / 10.0
        speed = self.slider_speed.value() / 10.0
        rot = self.slider_rot.value()
        zoom = self.slider_zoom.value()
        color = self.slider_color.value()
        sens = self.slider_sens.value()
        auto = self.checkbox_auto.isChecked()
        self.param.updated.emit(amp, freq, speed, rot, zoom, color, sens, auto)

def run_gui(param):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ControlWindow(param)
    sys.exit(app.exec_())
