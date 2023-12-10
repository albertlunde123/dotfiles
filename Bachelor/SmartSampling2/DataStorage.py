import csv
import os.path
import numpy as np

class DataStorage:
    def __init__(self, filename, optimizer):
        self.filename = filename
        self.optimizer = optimizer
        
        if not os.path.isfile(self.filename):
            with open(self.filename, 'a', newline = '') as csvfile:
                fieldnames = ['method', 'distance', 'iterations']
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        self.distance = self.get_distance()

    def get_distance(self):
        distance = []
        gy = self.optimizer.guesses
        gx = self.optimizer.guesses_location
        x = [self.optimizer.function_obj.true_min_location for _ in range(len(gx))]
        y = [self.optimizer.function_obj.true_min_value for _ in range(len(gy))]
        for i in range(len(gx)):
            distance.append(np.linalg.norm(np.array([gx[i], gy[i]]) - np.array([x[i], y[i]])))
        return distance

        
    def write(self):
        with open(self.filename, 'a', newline = '') as csvfile:
            fieldnames = ['distance', 'iterations']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writerow({'distance': self.distance,
                             'iterations': len(self.distance)})
