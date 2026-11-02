"""
AI Agronomic Diagnostics & Decarbonization Recommendation Engine
Tailored to Tumakuru's Agro-Climatic Zone 4 and UAS Bengaluru PoP Benchmarks.
"""
from typing import List, Dict, Any

def analyze_inefficiencies(farm_input, stage_emissions: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Identifies resource waste and high-carbon agricultural practices.
    """
    flags = []
    
    # 1. Fertilizer Inefficiency Check
    fert = farm_input.fertilizer
    synthetic_n = (fert.urea_kg_ha * 0.46) + (fert.dap_kg_ha * 0.18) + (fert.complex_19_19_19_kg_ha * 0.19)
    if synthetic_n > 210.0:
        excess_n = synthetic_n - 180.0
        flags.append({
            "stage": "fertilizer",
            "severity": "HIGH",
            "title": "Excessive Synthetic Nitrogen Application",
            "detail": f"Farm applies {round(synthetic_n, 1)} kg N/ha. UAS Bengaluru Package of Practices recommends 180 kg N/ha for drip or 200 kg N/ha for open-field.",
            "excess_quantity": round(excess_n, 1),
            "unit": "kg N/ha",
            "carbon_penalty_kg_co2e": round(excess_n * (2.62 / 0.46 + 0.010 * 1.5714 * 273), 1)
        })

    # 2. Irrigation Inefficiency Check
    irr = farm_input.irrigation
    if irr.irrigation_system == "flood_furrow":
        flags.append({
            "stage": "irrigation",
            "severity": "CRITICAL",
            "title": "Inefficient Flood/Furrow Irrigation in Groundwater-Stressed Zone",
            "detail": "Tumakuru is categorized as Over-Exploited by CGWB. Flood irrigation wastes ~45% of pumped groundwater and drives thermal grid emissions.",
            "carbon_penalty_kg_co2e": round(stage_emissions.get("irrigation", 0) * 0.48, 1)
        })
    elif irr.energy_source == "grid_electricity":
        flags.append({
            "stage": "irrigation",
            "severity": "MEDIUM",
            "title": "Heavy Reliance on Carbon-Intensive Grid Electricity",
            "detail": "Electricity from BESCOM grid has a delivered carbon factor of 0.835 kg CO2e/kWh due to thermal coal dominance and 16.5% rural T&D loss.",
            "carbon_penalty_kg_co2e": round(stage_emissions.get("irrigation", 0) * 0.90, 1)
        })

    # 3. Tillage Operations Check
    land = farm_input.land_prep
    total_passes = land.disc_plough_passes + land.cultivator_passes + land.rotavator_passes + land.ridger_passes
    if total_passes > 5:
        flags.append({
            "stage": "land_prep",
            "severity": "MEDIUM",
            "title": "Excessive Tractor Tillage Operations",
            "detail": f"Recorded {total_passes} tractor passes. Intensive tillage oxidizes soil organic carbon and burns unnecessary diesel in Alfisols.",
            "carbon_penalty_kg_co2e": round((total_passes - 4) * 8.0 * 3.204, 1)
        })

    # 4. Packaging & Post-Harvest Losses
    harvest = farm_input.harvest
    if harvest.packaging_type == "wooden_corrugated":
        flags.append({
            "stage": "harvest",
            "severity": "MEDIUM",
            "title": "Single-Use Packaging Crates",
            "detail": "Single-use wooden boxes result in higher cradle-to-grave emissions and higher transit damage than reusable sanitized HDPE crates.",
            "carbon_penalty_kg_co2e": round(farm_input.farm_area_ha * harvest.fresh_yield_kg_ha * (0.024 - 0.0028), 1)
        })

    if harvest.post_harvest_loss_pct > 14.0:
        flags.append({
            "stage": "harvest",
            "severity": "HIGH",
            "title": "Elevated Post-Harvest Supply Chain Losses",
            "detail": f"Post-harvest loss is {harvest.post_harvest_loss_pct}%, leading to wasted embedded upstream emissions in tomatoes that never reach consumers.",
            "carbon_penalty_kg_co2e": round(stage_emissions.get("total", 0) * (harvest.post_harvest_loss_pct / 100.0), 1)
        })

    return flags

def generate_recommendations(farm_input, stage_emissions: Dict[str, float], total_co2e: float) -> List[Dict[str, Any]]:
    """
    Synthesizes actionable, science-backed decarbonization pathways with estimated ROI and emission cuts.
    """
    recommendations = []
    
    # 1. Drip Fertigation Conversion
    if farm_input.irrigation.irrigation_system == "flood_furrow":
        irr_cut = stage_emissions.get("irrigation", 0) * 0.48
        fert_cut = stage_emissions.get("fertilizer", 0) * 0.22
        total_saving = irr_cut + fert_cut
        recommendations.append({
            "category": "Irrigation & Fertigation",
            "title": "Transition to Precision In-Line Drip Fertigation",
            "description": "Convert from furrow flooding to drip irrigation with Venturi fertigation. Conserves 45% irrigation water, increases fertilizer uptake efficiency by 30%, and improves tomato fruit yield by 20-35%.",
            "potential_reduction_kg_co2e": round(total_saving, 1),
            "potential_reduction_percentage": round((total_saving / total_co2e) * 100, 1) if total_co2e > 0 else 0,
            "estimated_cost_impact": "High initial capital (partially offset by 75-90% PMKSY subsidy for Karnataka farmers); saves ₹12,000/ha annually in fertilizer and pumping costs.",
            "scientific_basis": "UAS Bengaluru Precision Farming Development Centre (PFDC) Tomato Drip Protocol"
        })

    # 2. Solar PV Pumping
    if farm_input.irrigation.energy_source != "solar_pv":
        solar_saving = stage_emissions.get("irrigation", 0) * 0.94
        recommendations.append({
            "category": "Clean Energy",
            "title": "Solarize Borewell Pump via PM-KUSUM Scheme",
            "description": "Install a 5 HP or 7.5 HP standalone solar PV submersible pumpset. Replaces fossil-heavy coal grid electricity (0.835 kg CO2e/kWh) with low-carbon solar power (0.045 kg CO2e/kWh).",
            "potential_reduction_kg_co2e": round(solar_saving, 1),
            "potential_reduction_percentage": round((solar_saving / total_co2e) * 100, 1) if total_co2e > 0 else 0,
            "estimated_cost_impact": "60% capital subsidy from Central & Karnataka State Govt; eliminates erratic grid power outages and night irrigation hazards.",
            "scientific_basis": "Ministry of New and Renewable Energy (MNRE) PM-KUSUM Guidelines & Central Electricity Authority"
        })

    # 3. Integrated Nutrient Management & Bio-fertilizers
    fert_n = (farm_input.fertilizer.urea_kg_ha * 0.46) + (farm_input.fertilizer.dap_kg_ha * 0.18)
    if fert_n > 140:
        inm_saving = stage_emissions.get("fertilizer", 0) * 0.28
        recommendations.append({
            "category": "Nutrient Management",
            "title": "Integrated Nutrient Management (INM) & Bio-Fertilizer Substitution",
            "description": "Replace 25% of synthetic urea with seed/seedling root inoculation of Azotobacter and Phosphate Solubilizing Bacteria (PSB) combined with enriched vermicompost and neem-coated urea.",
            "potential_reduction_kg_co2e": round(inm_saving, 1),
            "potential_reduction_percentage": round((inm_saving / total_co2e) * 100, 1) if total_co2e > 0 else 0,
            "estimated_cost_impact": "Net savings of ₹3,500/ha in chemical fertilizer purchase while rebuilding soil organic carbon in Tumakuru Alfisols.",
            "scientific_basis": "ICAR-IIHR Hessaraghatta Bio-fertilizer Technology & IPCC 2019 N2O mitigation research"
        })

    # 4. Packaging & Cold Chain
    if farm_input.harvest.packaging_type != "reusable_hdpe_crate" or farm_input.harvest.post_harvest_loss_pct > 10:
        packaging_saving = 180.0
        recommendations.append({
            "category": "Post-Harvest & Packaging",
            "title": "Standardized Reusable HDPE Crates & On-Farm Pre-Cooling",
            "description": "Switch from single-use crates to reusable vented plastic crates and field shade pre-cooling. Reduces physical fruit bruising, bacterial soft rot, and trims post-harvest losses from 16% to under 8%.",
            "potential_reduction_kg_co2e": round(packaging_saving, 1),
            "potential_reduction_percentage": round((packaging_saving / total_co2e) * 100, 1) if total_co2e > 0 else 0,
            "estimated_cost_impact": "Crate purchase cost amortized over 3-4 years; provides 8-12% higher market realization at Antharasanahalli / Bangalore APMC.",
            "scientific_basis": "CIPHET & National Horticulture Board Post-Harvest Protocols"
        })

    # 5. Route & Fleet Optimization
    if farm_input.transport.vehicle_type == "scv_tata_ace" and farm_input.harvest.fresh_yield_kg_ha > 30000:
        trans_saving = stage_emissions.get("transport", 0) * 0.35
        recommendations.append({
            "category": "Logistics & Distribution",
            "title": "Aggregated Farmer Producer Organisation (FPO) Medium-Truck Logistics",
            "description": "Consolidate harvest loads through local Tumakuru FPOs using 5-tonne medium commercial vehicles instead of 10+ individual small vehicle trips.",
            "potential_reduction_kg_co2e": round(trans_saving, 1),
            "potential_reduction_percentage": round((trans_saving / total_co2e) * 100, 1) if total_co2e > 0 else 0,
            "estimated_cost_impact": "Reduces freight logistics cost from ₹2.20/kg to ₹1.10/kg tomato delivered to Bengaluru/Tumakuru.",
            "scientific_basis": "India GHG Program Freight Logistics Benchmarks"
        })

    return recommendations

