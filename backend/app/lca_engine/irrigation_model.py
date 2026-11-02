"""
Irrigation Energy & Emissions Model for Tumakuru District Groundwater Agriculture.
Incorporates Central Ground Water Board (CGWB) dynamic depth, hydraulic lifting physics,
and Central Electricity Authority (CEA) emission factors.
"""
from typing import Dict, Any
from app.core.constants import (
    WATER_DENSITY_KG_M3,
    GRAVITY_ACCELERATION,
    JOULES_PER_KWH,
    COMBINED_PUMPING_EFFICIENCY,
    DELIVERED_GRID_EF_KG_CO2E_KWH,
    DIESEL_WELL_TO_WHEEL_KG_CO2E_L,
    HP_TO_KW
)

SOLAR_PV_LCA_EF_KG_CO2E_KWH = 0.045  # NREL / IEA PVPS Task 12

def calculate_irrigation_emissions(
    irrigation_system: str,
    pump_hp: float,
    energy_source: str,
    borewell_depth_m: float,
    total_water_volume_m3: float = None,
    pumping_hours: float = None
) -> Dict[str, Any]:
    """
    Computes water volume, energy consumption, and carbon emissions for tomato irrigation.
    """
    # 1. Estimate water volume if not explicitly supplied
    if total_water_volume_m3 is None:
        if irrigation_system == "drip_fertigation":
            # UAS Bengaluru & ICAR-IIHR drip requirement for tomato (4,200 - 5,000 m3/ha)
            total_water_volume_m3 = 4600.0
        else:
            # Traditional flood / furrow irrigation (7,500 - 9,500 m3/ha due to percolation/runoff losses)
            total_water_volume_m3 = 8500.0

    # 2. Hydraulic Work Calculation:
    # E_elec_theoretical (kWh) = (Volume_m3 * 1000 kg/m3 * 9.81 m/s2 * Head_m) / (3.6e6 * efficiency)
    hydraulic_energy_kwh = (
        total_water_volume_m3 * WATER_DENSITY_KG_M3 * GRAVITY_ACCELERATION * borewell_depth_m
    ) / (JOULES_PER_KWH * COMBINED_PUMPING_EFFICIENCY)

    # Cross-reference with pump rating and hours
    pump_kw = pump_hp * HP_TO_KW
    if pumping_hours is not None and pumping_hours > 0:
        pump_hour_energy_kwh = pumping_hours * pump_kw * 0.85  # 0.85 load factor
        # Blend theoretical hydraulic requirement with reported pump hours
        actual_energy_kwh = (hydraulic_energy_kwh * 0.4) + (pump_hour_energy_kwh * 0.6)
        effective_pumping_hours = pumping_hours
    else:
        actual_energy_kwh = hydraulic_energy_kwh
        effective_pumping_hours = actual_energy_kwh / (pump_kw * 0.85)

    # 3. Compute Emissions by Energy Source
    diesel_liters_used = 0.0
    if energy_source == "grid_electricity":
        emissions_kg_co2e = actual_energy_kwh * DELIVERED_GRID_EF_KG_CO2E_KWH
    elif energy_source == "diesel_generator":
        # Specific fuel consumption for diesel generator: ~0.30 liters / kWh
        diesel_liters_used = actual_energy_kwh * 0.30
        emissions_kg_co2e = diesel_liters_used * DIESEL_WELL_TO_WHEEL_KG_CO2E_L
    elif energy_source == "solar_pv":
        emissions_kg_co2e = actual_energy_kwh * SOLAR_PV_LCA_EF_KG_CO2E_KWH
    else:
        # Default to grid
        emissions_kg_co2e = actual_energy_kwh * DELIVERED_GRID_EF_KG_CO2E_KWH

    return {
        "water_volume_m3": round(total_water_volume_m3, 1),
        "energy_consumption_kwh": round(actual_energy_kwh, 2),
        "pumping_hours": round(effective_pumping_hours, 1),
        "diesel_liters": round(diesel_liters_used, 1),
        "borewell_head_m": borewell_depth_m,
        "energy_source": energy_source,
        "emissions_kg_co2e": round(emissions_kg_co2e, 2),
        "grid_ef_used": DELIVERED_GRID_EF_KG_CO2E_KWH if energy_source == "grid_electricity" else None
    }

