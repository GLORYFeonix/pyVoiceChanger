import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication, QLabel, QSlider, QLineEdit

from process import *

process = Process()


class VoiceChanger(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        record = QPushButton("Record")
        record.clicked.connect(process.record_audio)
        time = QLineEdit(self)
        time.setValidator(QIntValidator(1, 3))
        time.textChanged.connect(process.timeChange)
        change = QPushButton("Change")
        change.clicked.connect(process.changeVoice)
        play = QPushButton("Play")
        play.clicked.connect(process.play_audio)
        label_icon = QLabel()
        label_icon.setPixmap(QPixmap("./icon.jpg"))
        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(process.levelChange)
        slider.setMinimum(-2)
        slider.setMaximum(2)
        slider.setSingleStep(1)
        slider.setTickPosition(QSlider.TicksBothSides)
        about = QLabel("by 通信1802 郭泽宇 41802198")
        about.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(label_icon, 0, 0, 4, 4)
        grid.addWidget(record, 4, 0)
        grid.addWidget(time, 4, 1, 1, 1)
        grid.addWidget(change, 4, 2)
        grid.addWidget(play, 4, 3)
        grid.addWidget(slider, 5, 0, 1, 2)
        grid.addWidget(about, 5, 2, 1, 2)

        self.setLayout(grid)

        self.setGeometry(300, 100, 350, 300)
        self.setWindowTitle('Voice Changer')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vc = VoiceChanger()
    sys.exit(app.exec_())
