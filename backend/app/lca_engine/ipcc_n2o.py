"""
IPCC 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories
Volume 4: Agriculture, Forestry and Other Land Use (AFOLU), Chapter 11: N2O Emissions from Managed Soils.
"""
from typing import Dict
from app.core.constants import (
    IPCC_EF1_SYNTHETIC,
    IPCC_EF1_ORGANIC,
    IPCC_FRAC_GASF_SYNTHETIC,
    IPCC_FRAC_GASM_ORGANIC,
    IPCC_EF4_VOLATILIZATION,
    IPCC_FRAC_LEACH,
    IPCC_EF5_LEACHING,
    N2O_TO_N2_MOLECULAR_RATIO,
    GWP_N2O
)

def calculate_soil_n2o_emissions(synthetic_n_kg: float, organic_n_kg: float) -> Dict[str, float]:
    """
    Calculates direct and indirect nitrous oxide (N2O) emissions in kg N2O and kg CO2e.
    
    1. Direct Soil Emissions:
       N2O_direct_N = (N_synthetic * EF1_synth) + (N_organic * EF1_org)
       
    2. Indirect from Atmospheric Deposition (Volatilization):
       N_volatilized = (N_synthetic * Frac_GASF) + (N_organic * Frac_GASM)
       N2O_indirect_volatilization_N = N_volatilized * EF4
       
    3. Indirect from Leaching and Runoff:
       N_leached = (N_synthetic + N_organic) * Frac_LEACH
       N2O_indirect_leaching_N = N_leached * EF5
       
    Total N2O = (N2O_direct_N + N2O_indirect_volatilization_N + N2O_indirect_leaching_N) * (44 / 28)
    Total CO2e = Total N2O * GWP_N2O (273 from IPCC AR6)
    """
    # Direct
    n2o_direct_n = (synthetic_n_kg * IPCC_EF1_SYNTHETIC) + (organic_n_kg * IPCC_EF1_ORGANIC)
    n2o_direct_kg = n2o_direct_n * N2O_TO_N2_MOLECULAR_RATIO
    co2e_direct = n2o_direct_kg * GWP_N2O

    # Indirect: Volatilization
    n_volatilized = (synthetic_n_kg * IPCC_FRAC_GASF_SYNTHETIC) + (organic_n_kg * IPCC_FRAC_GASM_ORGANIC)
    n2o_volatilization_n = n_volatilized * IPCC_EF4_VOLATILIZATION
    n2o_volatilization_kg = n2o_volatilization_n * N2O_TO_N2_MOLECULAR_RATIO
    co2e_volatilization = n2o_volatilization_kg * GWP_N2O

    # Indirect: Leaching
    n_leached = (synthetic_n_kg + organic_n_kg) * IPCC_FRAC_LEACH
    n2o_leaching_n = n_leached * IPCC_EF5_LEACHING
    n2o_leaching_kg = n2o_leaching_n * N2O_TO_N2_MOLECULAR_RATIO
    co2e_leaching = n2o_leaching_kg * GWP_N2O

    total_n2o_kg = n2o_direct_kg + n2o_volatilization_kg + n2o_leaching_kg
    total_co2e = co2e_direct + co2e_volatilization + co2e_leaching

    return {
        "n2o_direct_kg": round(n2o_direct_kg, 4),
        "co2e_direct_kg": round(co2e_direct, 2),
        "n2o_volatilization_kg": round(n2o_volatilization_kg, 4),
        "co2e_volatilization_kg": round(co2e_volatilization, 2),
        "n2o_leaching_kg": round(n2o_leaching_kg, 4),
        "co2e_leaching_kg": round(co2e_leaching, 2),
        "total_n2o_kg": round(total_n2o_kg, 4),
        "total_n2o_co2e_kg": round(total_co2e, 2)
    }

