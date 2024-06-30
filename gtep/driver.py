from gtep.gtep_model import ExpansionPlanningModel
from gtep.gtep_data import ExpansionPlanningData
from gtep.gtep_solution import ExpansionPlanningSolution
from pyomo.core import TransformationFactory
from pyomo.contrib.appsi.solvers.highs import Highs
from pyomo.contrib.appsi.solvers.gurobi import Gurobi


data_path = "./gtep/data/5bus"
data_object = ExpansionPlanningData()
data_object.load_prescient(data_path)
mod_object = ExpansionPlanningModel(
    stages=2,
    data=data_object.md,
    num_reps=2,
    len_reps=1,
    num_commit=24,
    num_dispatch=12,
)
mod_object.create_model()
TransformationFactory("gdp.bound_pretransformation").apply_to(mod_object.model)
TransformationFactory("gdp.bigm").apply_to(mod_object.model)
# opt = SolverFactory("gurobi")
# opt = Gurobi()
opt = Highs()
# mod_object.results = opt.solve(mod_object.model, tee=True)
mod_object.results = opt.solve(mod_object.model)


save_numerical_results = False
if save_numerical_results:

    sol_object = ExpansionPlanningSolution()

    sol_object.load_from_model(mod_object)
    sol_object.dump_json()
load_numerical_results = False
if load_numerical_results:
    # sol_object.read_json("./gtep_solution.json")
    sol_object.read_json("./bigger_longer_wigglier_gtep_solution.json")
plot_results = False
if plot_results:
    sol_object.plot_levels(save_dir="./plots/")

pass