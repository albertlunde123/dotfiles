import numpy as np

from FunctionClass import Function
from OptimizeClass import Optimize
from PlottingClass import Plotting

f = Function()

o = Optimize(f)
o.run(50, "expected_improvement")
p = Plotting(o)
# p.plot_function()
# p.plot_gaussian(alpha=0.1)
# p.plot_expected_improvement()
# for i in o.sample:
#     print(i)
# p.plot_samples()

# o.run(30, "bayesian")
print(f.true_min_location)
print(f.true_min_value)
print(o.guesses_location[-1])
print(o.guesses[-1])
p.plot_guess_progress()
p.show()

o.run(50, "bayesian")

p = Plotting(o)
p.plot_guess_progress()
p.show()

# p = Plotting(o)
# p.plot_function()
# p.plot_samples()
# p.plot_gaussian(alpha=0.1)
# p.plot_expected_improvement()
# p.show()

