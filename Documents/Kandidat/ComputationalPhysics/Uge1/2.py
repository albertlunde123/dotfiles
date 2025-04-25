import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants and initial conditions

x_init = 0
x_final = 30
x_range = [x_init, x_final]
x_eval = np.linspace(x_init, x_final, 100)

y_init = [22.5]
g = 9.8

# A basic linear ramp function

def y_ramp(x):
    return y_init[0] - y_init[0] * x / 30

def dydx_ramp():
    return -y_init[0] / 30

def dxdt(x, t):
    return np.sqrt(2*g) * np.sqrt(y_init[0] - y_ramp(x)) * 1 / np.sqrt(1 + dydx_ramp()**2)

# An event function to stop the integration when the ball reaches the end of the ramp

f = lambda x, t: x - x_final
f.terminal = True

my_sol = solve_ivp(dxdt, x_range, y_init, t_eval=x_eval, events=[f])

ts = my_sol.t
ys = my_sol.y[0]
t_event = my_sol.t_events[0]

print(f'The ball reaches the end of the ramp at t = {t_event}')



    


