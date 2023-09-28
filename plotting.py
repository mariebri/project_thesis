import numpy as np
import matplotlib.pyplot as plt

def load_map():
    img = plt.imread('./Map/map2.png')
    extent = [63.42577, 63.44865, 10.359356, 10.435152] # Long, lat
    plt.imshow(img)

def plot(waypoints, trajectory):
    """
    Loads a map, then plots waypoints as blue dots and trajectory as red line

    waypoints   = [[x1, x2, ...], [y1, y2, ...]]
    trajectory  = [[x1, x2, ...], [y1, y2, ...]]
    """
    load_map()
    plt.plot(waypoints[0], waypoints[1],'o')
    plt.plot(trajectory[0], trajectory[1],'r-')
    plt.show()

def test_plot():
    waypoints = np.array([[100,200,300],[200,150,200]])
    xdata = range(100,200)
    ydata = range(150,250)
    trajectory = np.array([xdata, ydata])
    plot(waypoints, trajectory)