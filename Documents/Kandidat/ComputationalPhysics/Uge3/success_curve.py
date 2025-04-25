import numpy as np
import matplotlib.pyplot as plt

data = np.array([1, 2, 2, 2, 5, 6, 8, 8, 8])
data = np.sort(data)
index = np.unique(data, return_index=True)[1][1:]

def succes_curve(data):
    data = np.sort(data)
    index = np.unique(data, return_index=True)[1]

    x_data = data[index]
    index = np.append(index[1:], len(data))
    print(index)
    y_data = [i/len(data) for i in index]
    plt.plot(x_data, y_data, marker='o')
    plt.title('Success Curve')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Success Rate')
    plt.set_xlim([0, 10])
    plt.set_ylim([0, 1])
    plt.show()

succes_curve(data)
