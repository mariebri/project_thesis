import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class World:
    def __init__(self):
        self.portA = [660, 20]
        self.portB = [620, 280]
        self.portC = [340, 445]
        self.portD = [136, 480]
        self.portE = [470, 578]

    def plotMap(self):
        img = np.asarray(Image.open('../Map/map.png'))
        plt.imshow(img)
        plt.plot(self.portA[0], self.portA[1], marker="o", markersize=5)
        plt.plot(self.portB[0], self.portB[1], marker="o", markersize=5)
        plt.plot(self.portC[0], self.portC[1], marker="o", markersize=5)
        plt.plot(self.portD[0], self.portD[1], marker="o", markersize=5)
        plt.plot(self.portE[0], self.portE[1], marker="o", markersize=5)