import numpy as np

class CandidateManipulation:
    """
    This class is used to manipulate the candidate
    """
    def __init__(self, cand):
        # cand: (n, 2), takes a candidate
        self.cand = cand
        self.bounds = cand.get_bounds()

    def center_candidate(self):

        x_min, x_max = self.bounds[0], self.bounds[1]
        y_min, y_max = self.bounds[0], self.bounds[1]
        cand_x_min, cand_x_max = np.min(self.cand[:, 0]), np.max(self.cand[:, 0])
        cand_y_min, cand_y_max = np.min(self.cand[:, 1]), np.max(self.cand[:, 1])

        x_shift = (x_min + x_max) / 2 - (cand_x_min + cand_x_max) / 2
        y_shift = (y_min + y_max) / 2 - (cand_y_min + cand_y_max) / 2

        self.cand[:, 0] += x_shift
        self.cand[:, 1] += y_shift

        return cand
