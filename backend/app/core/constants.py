"""
Physical, Stoichiometric, and Regional Agricultural Constants for Tumakuru, Karnataka.
"""

# Global Warming Potentials (IPCC 6th Assessment Report - AR6, 100-year timescale)
GWP_CO2 = 1.0
GWP_CH4 = 29.8
GWP_N2O = 273.0  # AR6 GWP100

# Physical & Engineering Constants
WATER_DENSITY_KG_M3 = 1000.0       # rho (density of water)
GRAVITY_ACCELERATION = 9.81        # g in m/s^2
JOULES_PER_KWH = 3.6e6             # 3,600,000 J per kWh
HP_TO_KW = 0.7457                  # 1 HP = 0.7457 kW

# Default Submersible Pump Efficiencies (CGWB / Bureau of Energy Efficiency standard in India)
DEFAULT_PUMP_HYDRAULIC_EFFICIENCY = 0.65
DEFAULT_MOTOR_ELECTRICAL_EFFICIENCY = 0.80
COMBINED_PUMPING_EFFICIENCY = DEFAULT_PUMP_HYDRAULIC_EFFICIENCY * DEFAULT_MOTOR_ELECTRICAL_EFFICIENCY  # ~0.52

# Stoichiometry
N2O_TO_N2_MOLECULAR_RATIO = 44.0 / 28.0  # 1.5714

# IPCC 2019 Refinement to 2006 Guidelines Defaults for Managed Agricultural Soils (Tier 1)
IPCC_EF1_SYNTHETIC = 0.010        # kg N2O-N / kg N applied
IPCC_EF1_ORGANIC = 0.010          # kg N2O-N / kg N applied
IPCC_FRAC_GASF_SYNTHETIC = 0.11   # Fraction of synthetic N volatilizing as NH3 + NOx
IPCC_FRAC_GASM_ORGANIC = 0.20     # Fraction of organic N volatilizing
IPCC_EF4_VOLATILIZATION = 0.010   # kg N2O-N / kg volatilized N
IPCC_FRAC_LEACH = 0.24            # Fraction of N lost through leaching / runoff
IPCC_EF5_LEACHING = 0.011         # kg N2O-N / kg leached N

# Central Electricity Authority (CEA) Baseline v21.0 Baseline for Karnataka
CEA_GRID_EF_KG_CO2_KWH = 0.716
KARNATAKA_RURAL_TD_LOSS_PCT = 16.5
DELIVERED_GRID_EF_KG_CO2E_KWH = CEA_GRID_EF_KG_CO2_KWH / (1.0 - (KARNATAKA_RURAL_TD_LOSS_PCT / 100.0))  # 0.857 (conservatively ~0.835 - 0.857)

# Diesel Fuel Properties (India GHG Program & IPCC)
DIESEL_DIRECT_COMBUSTION_KG_CO2_L = 2.680
DIESEL_UPSTREAM_REFINING_KG_CO2_L = 0.524
DIESEL_WELL_TO_WHEEL_KG_CO2E_L = 3.204

