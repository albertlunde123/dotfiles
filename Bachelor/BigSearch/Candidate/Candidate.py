import numpy as np

class Candidate:
    '''
    A candidate is a point in the search space.
    coords - A 1d numpy array of coordinates.
    '''
    def __init__(self, coords):
        if type(coords) != np.ndarray:
            raise TypeError('coords must be a numpy array')

        self.coords = coords

    def getCoords(self):
        return self.coords

    def setCoords(self, coords):
        self.coords = coords

    # Returns a 2d numpy array of coordinates.
    def get2dCoords(self):
        coords = self.getCoords()
        coords2d = coords.reshape((coords.shape[0] // 2, 2))
        return coords2d

    # Returns a tuple of 1d numpy arrays of coordinates. Suitable for plotting.
    def getPlotCoords(self):
        coords = self.get2dCoords()
        return coords[:, 0], coords[:, 1]


