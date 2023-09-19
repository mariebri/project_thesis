import matplotlib.pyplot as plt

def plotTrajectory(simData):
    #t = range(0, h, N*h)
    plt.plot(simData[0,:], simData[1,:])
    plt.grid()
    plt.show()