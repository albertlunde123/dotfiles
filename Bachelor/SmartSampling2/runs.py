from DataStorage import DataStorage
from OptimizeClass import Optimize
from FunctionClass import Function

f = Function()

optimize = Optimize(f)
optimize.run(10, "expected_improvement")

data = DataStorage("Data/EI_runs.csv", optimize)
data.write()
