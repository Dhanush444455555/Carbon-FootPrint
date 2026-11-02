from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from typing import Dict, Any, List

from app.schemas.farm_input import FarmCycleLcaRequest
from app.schemas.lca_response import FarmCycleLcaResponse
from app.lca_engine.calculator import TomatoLcaCalculator

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent

@router.post("/calculate", response_model=FarmCycleLcaResponse)
def calculate_carbon_footprint(request: FarmCycleLcaRequest):
    """
    Computes complete 8-stage life cycle assessment of tomato cultivation
    specifically calibrated for Tumakuru, Karnataka.
    """
    try:
        return TomatoLcaCalculator.calculate(request)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LCA calculation error: {str(e)}")

@router.get("/scenarios")
def get_predefined_scenarios():
    """
    Returns pre-configured farming archetypes (Conventional, BMP, Solar Regenerative).
    """
    scenarios_path = BASE_DIR / "data" / "baseline_scenarios.json"
    with open(scenarios_path, "r") as f:
        data = json.load(f)
    return data

@router.get("/calculate-scenario/{scenario_id}")
def calculate_predefined_scenario(scenario_id: str):
    """
    Runs full LCA calculation on one of the predefined archetypes.
    """
    scenarios_path = BASE_DIR / "data" / "baseline_scenarios.json"
    with open(scenarios_path, "r") as f:
        data = json.load(f)

    target_scenario = next((s for s in data["scenarios"] if s["id"] == scenario_id), None)
    if not target_scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Map scenario inputs to FarmCycleLcaRequest
    inputs = target_scenario["inputs"]
    req = FarmCycleLcaRequest(
        state_id="KA",
        district_id="Tumakuru",
        crop_name="Tomato",
        farm_name=target_scenario["name"],
        taluk_id=inputs["taluk_id"],
        farm_area_ha=inputs["farm_area_ha"],
        variety_name=target_scenario["name"],
        seed_nursery={
            "seed_rate_g_ha": inputs["seed_rate_g"],
            "seedling_count_ha": inputs["nursery_seedlings_count"],
            "nursery_type": inputs["nursery_type"]
        },
        land_prep={
            "custom_diesel_consumption_l": inputs["total_diesel_tillage_l"]
        },
        fertilizer={
            "urea_kg_ha": inputs["fertilizers"]["urea_kg"],
            "dap_kg_ha": inputs["fertilizers"]["dap_kg"],
            "mop_kg_ha": inputs["fertilizers"]["mop_kg"],
            "ssp_kg_ha": inputs["fertilizers"]["ssp_kg"],
            "complex_19_19_19_kg_ha": inputs["fertilizers"]["complex_19_19_19_kg"],
            "fym_tonnes_ha": inputs["fertilizers"]["fym_tonnes"],
            "pesticides_active_ingredient_kg_ha": inputs["pesticides_active_ingredient_kg"],
            "knapsack_sprayer_petrol_l": inputs["sprayer_petrol_l"]
        },
        irrigation={
            "irrigation_system": inputs["irrigation"]["system_type"],
            "pump_hp": inputs["irrigation"]["pump_hp"],
            "energy_source": inputs["irrigation"]["pump_energy_source"],
            "total_water_volume_m3_ha": inputs["irrigation"]["total_water_volume_m3"],
            "borewell_dynamic_head_m": inputs["irrigation"]["borewell_depth_m"],
            "pumping_hours_override": inputs["irrigation"]["pumping_hours"]
        },
        crop_maintenance={
            "staking_method": inputs["crop_maintenance"]["staking_type"],
            "mulching_type": inputs["crop_maintenance"]["mulching_type"],
            "intercultivation_diesel_l": inputs["crop_maintenance"]["intercultivation_diesel_l"]
        },
        harvest={
            "fresh_yield_kg_ha": inputs["harvest"]["total_harvest_kg"],
            "post_harvest_loss_pct": inputs["harvest"]["post_harvest_loss_pct"],
            "packaging_type": inputs["harvest"]["packaging_type"],
            "use_cold_storage": inputs["harvest"]["cold_storage_used"]
        },
        transport={
            "destination_market": inputs["transport"]["destination_name"],
            "transport_distance_km": inputs["transport"]["distance_km"],
            "vehicle_type": inputs["transport"]["vehicle_type"],
            "vehicle_payload_tons": inputs["transport"]["cargo_payload_tons"]
        }
    )
    return TomatoLcaCalculator.calculate(req)

