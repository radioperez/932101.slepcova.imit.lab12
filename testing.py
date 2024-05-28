# Тестирование алгоритма без гуи

from enum import Enum
import sys
import numpy as np
from numpy.random import default_rng

class Weather(Enum):
    SUNNY = 0
    CLOUDY = 1
    OVERCAST = 2

delta = 1 # Hours

Q = [[-0.4, 0.3, 0.1],
     [0.4, -0.8, 0.4],
     [0.1, 0.4, -0.5]]

P = np.empty((3,3))
for i in range(3):
    for j in range(3):
        P[i][j] = 1 + Q[i][j]*delta if i==j else Q[i][j]*delta

t = 0
cur_weather = Weather.CLOUDY
states = []

while (t < 24):
    t += delta
    cur_weather = default_rng().choice(list(Weather), p=P[cur_weather.value])
    states.append((t, cur_weather))

x, y = zip(*states)
y = [y_.value for y_ in y]
print(y)