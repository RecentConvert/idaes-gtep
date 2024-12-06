# %% [markdown]
# # IDAES-GTEP Tutorial Notebook
# ### Presented & last updated 9/19/24

# %% [markdown]
# This notebook is intended as an introductory tutorial to using the IDAES-GTEP tool.  It walks through loading a small test case (PJM 5-bus) and solves expansion planning models with a few different assumptions on the network.  It demonstrates some basic result visualizations on the investment options and grid operations.

# %%
from gtep.gtep_model import ExpansionPlanningModel
from gtep.gtep_data import ExpansionPlanningData
from gtep.gtep_solution import ExpansionPlanningSolution
from pyomo.core import TransformationFactory
from pyomo.contrib.appsi.solvers.highs import Highs
import pdb

# %% [markdown]
# Loads default set of representative days -- #TODO allow non defaults by Tuesday

# %%
data_path = "./gtep/data/5bus"
data_object = ExpansionPlanningData()
data_object.load_prescient(data_path)

# %% [markdown]
# Builds expansion planning object but not specific model yet -- #TODO note issues that can occur with num_reps too large.  Also, make config overwrite these periods for the distinct times.

# %%
mod_object = ExpansionPlanningModel(
    stages=1,
    data=data_object.md,
    num_reps=1,
    len_reps=1,
    num_commit=2,
    num_dispatch=2,
)

# %%
mod_object.create_model()

# %%
TransformationFactory("gdp.bound_pretransformation").apply_to(mod_object.model)
TransformationFactory("gdp.bigm").apply_to(mod_object.model)

# %%
# opt = Highs()
# mod_object.results = opt.solve(mod_object.model)

# %% [markdown]
# #TODO -- demonstrate capabilities to save & load solution info

# %%
sol_object = ExpansionPlanningSolution()
# sol_object.load_from_model(mod_object)
# sol_object.dump_json("./gtep/gtep_solution.json")


# %%
sol_object.import_data_object(data_object)
sol_object.read_json("./gtep/gtep_solution.json")

# %%
'''
plot_selection: if key = True that object will be plotted

plots from toplevel keys:
'branchChanged':        if branch was disabled, extended, installed, operational, or retired
'genChanged':           if gen was disabled, extended, installed, operational, or retired
'renewableGeneration':  if renewable was extended, installed, or operational

plots from midlevel keys:
'genPowered':           if gen was off, on, shutdown, or startup

plots from bottomlevel keys:
'powerFlow_graph':      networkx plot of power flow: branchInUse, branchNotInUse
'powerFlow':            line plot of power flow: branchInUse, branchNotInUse
'loadShed':             line plot of loadShed
'thermalGeneration':    line plot of quickstartReserve, spinningReserve, thermalGeneration
'renewableGeneration':  line plot of renewableCurtailment, renewableGeneration
'''
plot_selection = {
    'toplevel':     False,
    'midlevel':     False,
    'bottomlevel':  True,    
}

sol_object.plot_levels(save_dir="./gtep/plots/",
                       plot_selection=plot_selection)


