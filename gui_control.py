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
        layout = QtWidgets.QVBoxLayout()

        self.slider_amp, self.label_amp = self.create_slider("Amplitude", 30, 0, 100, 10.0)
        layout.addWidget(self.label_amp)
        layout.addWidget(self.slider_amp)

        self.slider_freq, self.label_freq = self.create_slider("Frequency", 10, 0, 100, 10.0)
        layout.addWidget(self.label_freq)
        layout.addWidget(self.slider_freq)

        self.slider_speed, self.label_speed = self.create_slider("Wave Speed", 20, 0, 100, 10.0)
        layout.addWidget(self.label_speed)
        layout.addWidget(self.slider_speed)

        self.slider_rot, self.label_rot = self.create_slider("Rotation Speed", 20, 0, 100)
        layout.addWidget(self.label_rot)
        layout.addWidget(self.slider_rot)

        self.slider_zoom, self.label_zoom = self.create_slider("Zoom", 50, 15, 100)
        layout.addWidget(self.label_zoom)
        layout.addWidget(self.slider_zoom)

        self.slider_color, self.label_color = self.create_slider("Color (Hue)", 130, 0, 360)
        layout.addWidget(self.label_color)
        layout.addWidget(self.slider_color)

        self.slider_sens, self.label_sens = self.create_slider("Sensitivity", 100, 1, 300)
        layout.addWidget(self.label_sens)
        layout.addWidget(self.slider_sens)

        self.checkbox_auto = QtWidgets.QCheckBox("Automatik")
        layout.addWidget(self.checkbox_auto)

        self.setLayout(layout)
        self.setWindowTitle("Control Panel")
        self.show()

        self.slider_changed()

        for s in [self.slider_amp, self.slider_freq, self.slider_speed,
                  self.slider_rot, self.slider_zoom, self.slider_color,
                  self.slider_sens]:
            s.valueChanged.connect(self.slider_changed)
        self.checkbox_auto.stateChanged.connect(self.slider_changed)

    def create_slider(self, label, default=50, min_val=0, max_val=100, scale=1.0):
        slider = QtWidgets.QSlider()
        slider.setOrientation(1)
        slider.setRange(min_val, max_val)
        slider.setValue(default)

        label_widget = QtWidgets.QLabel(f"{label}: {default / scale:.2f}" if scale != 1.0 else f"{label}: {default}")
        slider.valueChanged.connect(lambda val: label_widget.setText(
            f"{label}: {val / scale:.2f}" if scale != 1.0 else f"{label}: {val}"))

        return slider, label_widget

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
