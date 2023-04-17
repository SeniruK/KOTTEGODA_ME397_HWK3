# Homework 3 Task 1
# by Seniru Kottegoda

from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory

## constants and assumptions
# capital costs for solar, and energy storage systems
solar_cap_cost 			= 800000000       # $/GW
wind_cap_cost           = 1200000000      # $/GW
ESS_p_cap_cost 			= 200000000       # $/GW
ESS_e_cap_cost 			= 150000000       # $/GWh

# energy storage operational assumptions
ESS_min_level    		= 0.20      # %, minimum level of discharge of the battery
ESS_eta_c           	= 0.95      # ESS charging efficiency, looses 5% when charging
ESS_eta_d        		= 0.9       # ESS discharging efficiency, looses 10% when discharging
ESS_p_var_cost          = 5000     # ESS discharge cost $/GWh

curtailment_cost        = 1000     # curtailment penalty $/GWh

# create the model
model = AbstractModel(name = 'solar-storage model')

# create model sets
model.t                 = Set(initialize = [i for i in range(8760)], ordered=True)    
model.tech              = Set(initialize =['s_cap', 'w_cap', 'ESS_power_cap', 'ESS_energy_cap'], ordered=True)  

# parameters
model.solar             = Param(model.t)
model.wind              = Param(model.t)
model.demand            = Param(model.t)
model.costs             = Param(model.tech, initialize={'s_cap' : solar_cap_cost, 'w_cap' : wind_cap_cost, 'ESS_power_cap' : ESS_p_cap_cost, 'ESS_energy_cap' : ESS_e_cap_cost})

## load data into parameters, solar and wind data are houlry capacity factor data
data = DataPortal()
data.load(filename = 'opt_model_data/2022_ERCOT_data.csv', select = ('t', 'solar', 'wind', 'demand'), param = [model.solar, model.wind, model.demands], index = model.t)
# data.load(filename = 'opt_model_data/2022_ERCOT_data.csv', select = ('t', 'wind'), param = model.wind, index = model.t)
# data.load(filename = 'opt_model_data/2022_ERCOT_data.csv', select = ('t', 'demand'), param = model.demand, index = model.t)

## define variables
model.cap               = Var(model.tech, domain = NonNegativeReals)
model.ESS_SOC           = Var(model.t, domain = NonNegativeReals)
model.ESS_c             = Var(model.t, domain = NonNegativeReals)
model.ESS_d             = Var(model.t, domain = NonNegativeReals)
model.curt              = Var(model.t, domain = NonNegativeReals)

