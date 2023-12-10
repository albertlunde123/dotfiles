import numpy as np

def calc_bounds(n_atoms):
    upper = 1/np.sqrt(2) * (2*(n_atoms - 1) + 2*np.sqrt(2))*1.36 - 2*1.36
    return upper / 2

class ConfigurationSpace:

    def __init__(self, n_dim, bounds = None, epsilon = 2.72):
        self.dimensions = n_dim
        if bounds is None:
            bounds = (0, self.calc_bounds(n_dim // 2))
        self.bounds = bounds
        self.epsilon = epsilon

    def calc_bounds(self, n_atoms):
        upper = 1/np.sqrt(2) * (2*(n_atoms - 1) + 2*np.sqrt(2))*1.36 - 2*1.36
        return upper / 1.5

    def check_within_bounds(self, point):
        lower, upper = self.bounds
        return np.all(point >= lower) and np.all(point <= upper)
    
    def check_non_overlapping(self, point):
        num_atoms = self.dimensions // 2
        atoms = point.reshape(num_atoms, 2)

        for i in range(num_atoms):
            for j in range(i + 1, num_atoms):
                if np.linalg.norm(atoms[i] - atoms[j]) < self.epsilon:
                    return False
        return True

    def sample_near_point(self, original, delta=0.1):
        sampled_points = []

        for i in range(self.dimensions):
            new_point = original.copy()
            new_point[i] += delta
            if self.check_within_bounds(new_point) and self.check_non_overlapping(new_point):
                sampled_points.append(new_point)

        for i in range(self.dimensions):
            new_point = original.copy()
            new_point[i] -= delta
            if self.check_within_bounds(new_point) and self.check_non_overlapping(new_point):
                sampled_points.append(new_point)
        
        if len(sampled_points) == 0:
            return None

        return np.array(sampled_points)
    
    def rattle(self, point, delta=0.1):

        new_point = True
        while not self.check_within_bounds(new_point) or not self.check_non_overlapping(new_point):
            new_point = point.copy()
            for i in range(self.dimensions):
                new_point[i] += np.random.uniform(-delta, delta)

        return new_point
