import revolt
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    h       = 0.1
    x       = np.zeros((6,1))

    vessel  = revolt.ReVolt(x=x)

    for i in range(1000):
        vessel.step(h)
        vessel.plot()
    plt.show()
