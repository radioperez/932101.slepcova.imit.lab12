import sys
import random
import numpy as np
from numpy.random import default_rng
import scipy.stats
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QSpinBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)
from PyQt6.QtGui import QFont
import pyqtgraph as QtGraph
from enum import Enum

class Weather(Enum):
    SUNNY = 0
    CLOUDY = 1
    OVERCAST = 2

class Graph(QtGraph.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground("w")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Симулятор погоды')

        panel = QHBoxLayout()
        # start button
        start_button = QPushButton("СТАРТ")
        start_button.clicked.connect(self.start)

        self.timer = QTimer()
        stop_button = QPushButton("СТОП")
        stop_button.clicked.connect(self.stats)
        panel.addWidget(start_button)
        panel.addWidget(stop_button)

        # graph
        self.graph = Graph()
        font = QFont("Arial", 24)
        sunny = QtGraph.TextItem("☀️", anchor=(1,1))
        sunny.setPos(-0.5, 0)
        sunny.setFont(font)
        cloudy = QtGraph.TextItem("⛅", anchor=(1,1))
        cloudy.setPos(-0.5, 1)
        cloudy.setFont(font)
        overcast = QtGraph.TextItem("☁️", anchor=(1,0))
        overcast.setPos(-0.5, 2)
        overcast.setFont(font)
        self.graph.addItem(sunny)
        self.graph.addItem(cloudy)
        self.graph.addItem(overcast)

        self.statistics = QLabel("")

        layout = QVBoxLayout()
        layout.addLayout(panel)
        layout.addWidget(self.graph)
        layout.addWidget(self.statistics)
        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)

    def start(self):
        self.graph.clear()
        font = QFont("Arial", 24)
        
        sunny = QtGraph.TextItem("☀️", anchor=(1,1))
        sunny.setPos(-0.5, 0)
        sunny.setFont(font)
        cloudy = QtGraph.TextItem("⛅", anchor=(1,1))
        cloudy.setPos(-0.5, 1)
        cloudy.setFont(font)
        overcast = QtGraph.TextItem("☁️", anchor=(1,0))
        overcast.setPos(-0.5, 2)
        overcast.setFont(font)
        self.graph.addItem(sunny)
        self.graph.addItem(cloudy)
        self.graph.addItem(overcast)

        Q = [[-0.4, 0.3, 0.1],
             [0.4, -0.8, 0.4],
             [0.1, 0.4, -0.5]]

        self.delta = 1/8 # Every 3 hours
        self.P = np.empty((3,3))
        for i in range(3):
            for j in range(3):
                self.P[i][j] = 1 + Q[i][j]*self.delta if i==j else Q[i][j]*self.delta

        self.times = []
        self.weathers = []
        t = 0
        self.times.append(t)
        cur_weather = default_rng().choice(list(Weather))
        self.weathers.append(cur_weather.value)

        pen = QtGraph.mkPen(color=(0, 0, 255), width=5)
        self.line = self.graph.plot(self.times, self.weathers, pen=pen)

        self.timer.setInterval(120)
        self.timer.timeout.connect(self.run)
        self.timer.start()

    def run(self):
        t = self.times[-1] + self.delta
        self.times.append(t)
        cur_weather = default_rng().choice(list(Weather), p=self.P[self.weathers[-1]])
        self.weathers.append(cur_weather.value)
        self.line.setData(self.times, self.weathers)
    def stats(self):
        self.timer.stop()
        # TODO статическая обработка полученных данных !
        STATS, _ = np.histogram(self.weathers, bins=3)
        FREQUENCY = STATS/sum(STATS)
        text = f'''Статистика: СОЛНЕЧНО = {STATS[0]} | ОБЛАЧНО = {STATS[1]} | ПАСМУРНО = {STATS[2]}\nВероятности: СОЛНЕЧНО = {FREQUENCY[0]:.4f} | ОБЛАЧНО = {FREQUENCY[1]:.4f} | ПАСМУРНО = {FREQUENCY[2]:.4f}'''
        self.statistics.setText(text)
        print(FREQUENCY)


random.seed()
app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
