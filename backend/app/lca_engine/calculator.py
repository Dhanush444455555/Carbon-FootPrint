"""
Master Life Cycle Assessment (LCA) Calculator for Open-Field Tomato Cultivation
in Tumakuru District, Karnataka, India.
Compliant with ISO 14040/14044 principles and IPCC 2019 Refinement methodology.
"""
from typing import Dict, Any, List
import json
from pathlib import Path

from app.schemas.farm_input import FarmCycleLcaRequest
from app.schemas.lca_response import (
    FarmCycleLcaResponse,
    StageEmissionBreakdown,
    HotspotAnalysis,
    DecarbonizationRecommendation,
    BenchmarkComparison
)
from app.core.constants import (
    DIESEL_WELL_TO_WHEEL_KG_CO2E_L,
    DELIVERED_GRID_EF_KG_CO2E_KWH
)
from app.lca_engine.ipcc_n2o import calculate_soil_n2o_emissions
from app.lca_engine.irrigation_model import calculate_irrigation_emissions
from app.lca_engine.transport_model import calculate_transport_emissions
from app.lca_engine.diagnostics import analyze_inefficiencies, generate_recommendations

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / "data" / "emission_factors.json", "r") as f:
    EMISSION_FACTORS = json.load(f)["emission_factors"]

with open(BASE_DIR / "data" / "taluks_tumakuru.json", "r") as f:
    TALUKS_DATA = {t["id"]: t for t in json.load(f)["taluks"]}

class TomatoLcaCalculator:
    """
    Evaluates cradle-to-market greenhouse gas emissions across all 8 stages.
    """

    @staticmethod
    def calculate(request: FarmCycleLcaRequest) -> FarmCycleLcaResponse:
        # ----------------------------------------------------
        # STRICT GEOGRAPHICAL & CROP BOUNDARY VALIDATION
        # Section 1 & Section 4 Compliance
        # ----------------------------------------------------
        state_str = str(request.state_id or "").strip().lower()
        if state_str not in {"ka", "karnataka"}:
            raise ValueError(f"Geographic rejection: State must be 'Karnataka' (got '{request.state_id}'). Only Karnataka is supported.")

        dist_str = str(request.district_id or "").strip().lower()
        if dist_str not in {"tmk", "tumakuru", "tumkur"}:
            raise ValueError(
                f"Geographic rejection: District must be 'Tumakuru' (got '{request.district_id}'). "
                f"Records from Bengaluru, Chitradurga, Hassan, Mysuru or other districts are strictly non-negotiable and rejected."
            )

        valid_taluk_keys = {
            "tumakuru", "tiptur", "kunigal", "gubbi", "koratagere",
            "madhugiri", "pavagada", "sira", "chikkanayakanahalli", "chiknayakanhalli", "turuvekere"
        }
        taluk_key = str(request.taluk_id or "").strip().lower()
        if taluk_key not in valid_taluk_keys:
            raise ValueError(
                f"Geographic rejection: Taluk '{request.taluk_id}' is not one of the 10 official Tumakuru taluks. "
                f"Must be one of: Tumakuru, Tiptur, Kunigal, Gubbi, Koratagere, Madhugiri, Pavagada, Sira, Chikkanayakanahalli, Turuvekere."
            )

        crop_str = str(request.crop_name or "").strip().lower()
        if "tomato" not in crop_str and "lycopersicum" not in crop_str:
            raise ValueError(f"Crop rejection: Crop must be 'Tomato (Solanum lycopersicum)', got '{request.crop_name}'.")

        area_ha = request.farm_area_ha
        taluk_info = TALUKS_DATA.get(request.taluk_id, TALUKS_DATA.get(taluk_key, TALUKS_DATA["tumakuru"]))

        # ==========================================
        # STAGE 1: SEED AND NURSERY
        # ==========================================
        nursery_in = request.seed_nursery
        seed_kg_total = (nursery_in.seed_rate_g_ha / 1000.0) * area_ha
        seed_upstream_ef = EMISSION_FACTORS["hybrid_seed_production"]["value"]  # 145 kg CO2e/kg seed
        seed_prod_co2e = seed_kg_total * seed_upstream_ef

        seedling_raising_ef = EMISSION_FACTORS["seedling_protray_raising"]["value"]  # 0.0055 kg CO2e/seedling
        seedling_raising_co2e = nursery_in.seedling_count_ha * area_ha * seedling_raising_ef

        nursery_elec_co2e = nursery_in.nursery_electricity_kwh * area_ha * DELIVERED_GRID_EF_KG_CO2E_KWH
        # Seedling transit to farm: small payload ~0.15 tons per ha equivalent
        nursery_transit_tkm = (0.15 * area_ha) * nursery_in.nursery_to_farm_distance_km
        nursery_transit_co2e = nursery_transit_tkm * EMISSION_FACTORS["transport_scv_tata_ace"]["value"]

        stage1_total = seed_prod_co2e + seedling_raising_co2e + nursery_elec_co2e + nursery_transit_co2e

        # ==========================================
        # STAGE 2: LAND PREPARATION
        # ==========================================
        land_in = request.land_prep
        if land_in.custom_diesel_consumption_l is not None and land_in.custom_diesel_consumption_l > 0:
            total_diesel_tillage_l = land_in.custom_diesel_consumption_l * area_ha
        else:
            # Operation fuel coefficients (L/ha) for 45-50 HP tractor in Karnataka Alfisols
            fuel_disc_plough = land_in.disc_plough_passes * 14.0
            fuel_cultivator = land_in.cultivator_passes * 5.8
            fuel_rotavator = land_in.rotavator_passes * 8.2
            fuel_ridger = land_in.ridger_passes * 6.0
            total_diesel_tillage_l = (fuel_disc_plough + fuel_cultivator + fuel_rotavator + fuel_ridger) * area_ha

        stage2_total = total_diesel_tillage_l * DIESEL_WELL_TO_WHEEL_KG_CO2E_L

        # ==========================================
        # STAGE 3: CULTIVATION AND FERTILIZER APPLICATION
        # ==========================================
        fert_in = request.fertilizer
        # Upstream Manufacturing
        urea_total_kg = fert_in.urea_kg_ha * area_ha
        dap_total_kg = fert_in.dap_kg_ha * area_ha
        mop_total_kg = fert_in.mop_kg_ha * area_ha
        ssp_total_kg = fert_in.ssp_kg_ha * area_ha
        complex_total_kg = fert_in.complex_19_19_19_kg_ha * area_ha
        fym_total_kg = fert_in.fym_tonnes_ha * 1000.0 * area_ha

        co2e_urea_mfg = urea_total_kg * EMISSION_FACTORS["fertilizer_urea_upstream"]["value"]
        co2e_dap_mfg = dap_total_kg * EMISSION_FACTORS["fertilizer_dap_upstream"]["value"]
        co2e_mop_mfg = mop_total_kg * EMISSION_FACTORS["fertilizer_mop_upstream"]["value"]
        co2e_ssp_mfg = ssp_total_kg * EMISSION_FACTORS["fertilizer_ssp_upstream"]["value"]
        co2e_complex_mfg = complex_total_kg * EMISSION_FACTORS["fertilizer_complex_19_19_19"]["value"]
        co2e_fym_storage = fym_total_kg * EMISSION_FACTORS["organic_manure_fym"]["value"]

        total_upstream_fert = (
            co2e_urea_mfg + co2e_dap_mfg + co2e_mop_mfg + co2e_ssp_mfg + co2e_complex_mfg + co2e_fym_storage
        )

        # Nitrogen mass calculation for IPCC N2O
        synthetic_n_kg = (
            (urea_total_kg * 0.46) +
            (dap_total_kg * 0.18) +
            (complex_total_kg * 0.19)
        )
        # FYM contains ~0.50% total N on wet basis
        organic_n_kg = fym_total_kg * 0.0050

        # IPCC 2019 Refinement N2O calculation
        n2o_results = calculate_soil_n2o_emissions(synthetic_n_kg, organic_n_kg)
        soil_n2o_co2e = n2o_results["total_n2o_co2e_kg"]

        # Agrochemicals (Pesticides & Spraying)
        pesticide_ai_kg = fert_in.pesticides_active_ingredient_kg_ha * area_ha
        pesticide_mfg_co2e = pesticide_ai_kg * EMISSION_FACTORS["pesticide_active_ingredient"]["value"]
        # Petrol combustion in 2-stroke sprayer (approx 2.31 kg CO2/L direct + upstream = 2.85 kg CO2e/L)
        sprayer_petrol_co2e = fert_in.knapsack_sprayer_petrol_l * area_ha * 2.85

        stage3_total = total_upstream_fert + soil_n2o_co2e + pesticide_mfg_co2e + sprayer_petrol_co2e

        # ==========================================
        # STAGE 4: IRRIGATION AND WATER MANAGEMENT
        # ==========================================
        irr_in = request.irrigation
        # Use taluk's actual CGWB groundwater dynamic head if not specified differently
        effective_depth_m = irr_in.borewell_dynamic_head_m if irr_in.borewell_dynamic_head_m > 0 else taluk_info["groundwater_depth_m_bgl"]
        irrigation_results = calculate_irrigation_emissions(
            irrigation_system=irr_in.irrigation_system,
            pump_hp=irr_in.pump_hp,
            energy_source=irr_in.energy_source,
            borewell_depth_m=effective_depth_m,
            total_water_volume_m3=irr_in.total_water_volume_m3_ha * area_ha if irr_in.total_water_volume_m3_ha else None,
            pumping_hours=irr_in.pumping_hours_override * area_ha if irr_in.pumping_hours_override else None
        )
        stage4_total = irrigation_results["emissions_kg_co2e"]

        # ==========================================
        # STAGE 5: CROP GROWTH AND MAINTENANCE
        # ==========================================
        maint_in = request.crop_maintenance
        staking_co2e = 0.0
        if maint_in.staking_method == "bamboo_twine":
            staking_co2e = 28.5 * area_ha
        elif maint_in.staking_method == "wooden_stakes":
            staking_co2e = 38.0 * area_ha

        mulch_co2e = 0.0
        if maint_in.mulching_type == "polyethylene_silver_black":
            # 80 kg mulch film / ha @ 2.4 kg CO2e / kg amortized over 2 seasons
            mulch_co2e = 96.0 * area_ha
        elif maint_in.mulching_type == "organic_paddy_straw":
            mulch_co2e = 15.0 * area_ha

        intercult_fuel_co2e = maint_in.intercultivation_diesel_l * area_ha * DIESEL_WELL_TO_WHEEL_KG_CO2E_L
        stage5_total = staking_co2e + mulch_co2e + intercult_fuel_co2e

        # ==========================================
        # STAGE 6: HARVESTING AND POST-HARVEST
        # ==========================================
        harv_in = request.harvest
        gross_yield_kg = harv_in.fresh_yield_kg_ha * area_ha
        post_harvest_loss_fraction = harv_in.post_harvest_loss_pct / 100.0
        marketable_yield_kg = gross_yield_kg * (1.0 - post_harvest_loss_fraction)

        # Packaging emissions
        if harv_in.packaging_type == "reusable_hdpe_crate":
            crate_ef = EMISSION_FACTORS["packaging_reusable_hdpe_crate"]["value"]  # 0.0028 kg CO2e/kg
        else:
            crate_ef = EMISSION_FACTORS["packaging_wooden_corrugated"]["value"]    # 0.024 kg CO2e/kg
        packaging_co2e = marketable_yield_kg * crate_ef

        # Cold storage emissions (if active)
        cold_storage_co2e = 0.0
        if harv_in.use_cold_storage and harv_in.cold_storage_days > 0:
            # 0.0035 kWh per kg tomato per storage day
            cold_storage_kwh = marketable_yield_kg * 0.0035 * harv_in.cold_storage_days
            cold_storage_co2e = cold_storage_kwh * DELIVERED_GRID_EF_KG_CO2E_KWH

        # Manual picking and sorting: ~0.0008 kg CO2e / kg
        harvest_labor_machinery_co2e = gross_yield_kg * 0.0008
        stage6_total = packaging_co2e + cold_storage_co2e + harvest_labor_machinery_co2e

        # ==========================================
        # STAGE 7: TRANSPORTATION AND DISTRIBUTION
        # ==========================================
        trans_in = request.transport
        effective_dist_km = trans_in.transport_distance_km if trans_in.transport_distance_km > 0 else taluk_info["distance_to_apmc_tumakuru_km"]
        transport_results = calculate_transport_emissions(
            marketable_cargo_kg=marketable_yield_kg,
            one_way_distance_km=effective_dist_km,
            vehicle_type=trans_in.vehicle_type,
            custom_payload_tons=trans_in.vehicle_payload_tons
        )
        stage7_total = transport_results["emissions_kg_co2e"]

        # ==========================================
        # STAGE 8: FINAL TOTAL LIFECYCLE AGGREGATION
        # ==========================================
        total_cycle_emissions = (
            stage1_total +
            stage2_total +
            stage3_total +
            stage4_total +
            stage5_total +
            stage6_total +
            stage7_total
        )

        emissions_per_ha = total_cycle_emissions / area_ha
        footprint_per_kg_marketable = total_cycle_emissions / marketable_yield_kg if marketable_yield_kg > 0 else 0.0
        footprint_per_kg_gross_farmgate = total_cycle_emissions / gross_yield_kg if gross_yield_kg > 0 else 0.0

        # Stage breakdown items
        stage_items = [
            StageEmissionBreakdown(
                stage_id="stage_1_seed_nursery",
                stage_name="Stage 1: Seed and Nursery",
                emissions_kg_co2e=round(stage1_total, 2),
                emissions_kg_co2e_per_ha=round(stage1_total / area_ha, 2),
                percentage_of_total=round((stage1_total / total_cycle_emissions) * 100, 2),
                primary_driver="Hybrid seed breeding upstream & nursery shade net pro-tray preparation",
                sub_components={
                    "seed_production": round(seed_prod_co2e, 2),
                    "seedling_protray_raising": round(seedling_raising_co2e, 2),
                    "nursery_electricity": round(nursery_elec_co2e, 2),
                    "seedling_farm_transit": round(nursery_transit_co2e, 2)
                },
                provenance_reference="ICAR-IIHR Hessaraghatta & UAS Bengaluru PoP (Hybrid Seed Rate: 125-150 g/ha)"
            ),
            StageEmissionBreakdown(
                stage_id="stage_2_land_prep",
                stage_name="Stage 2: Land Preparation",
                emissions_kg_co2e=round(stage2_total, 2),
                emissions_kg_co2e_per_ha=round(stage2_total / area_ha, 2),
                percentage_of_total=round((stage2_total / total_cycle_emissions) * 100, 2),
                primary_driver="Tractor diesel fuel combustion during primary ploughing & rotavator tilth",
                sub_components={
                    "total_diesel_liters": round(total_diesel_tillage_l, 1),
                    "well_to_wheel_co2e": round(stage2_total, 2)
                },
                provenance_reference="AICRP on Farm Implements, UAS Bengaluru (45-50 HP Tractor Operations in Alfisols)"
            ),
            StageEmissionBreakdown(
                stage_id="stage_3_fertilizer",
                stage_name="Stage 3: Cultivation & Fertilizers",
                emissions_kg_co2e=round(stage3_total, 2),
                emissions_kg_co2e_per_ha=round(stage3_total / area_ha, 2),
                percentage_of_total=round((stage3_total / total_cycle_emissions) * 100, 2),
                primary_driver="Direct & indirect N2O soil fluxes and upstream chemical manufacturing (Urea/DAP)",
                sub_components={
                    "fertilizer_manufacturing_upstream": round(total_upstream_fert, 2),
                    "ipcc_soil_direct_n2o": round(n2o_results["co2e_direct_kg"], 2),
                    "ipcc_soil_indirect_n2o_volatilization": round(n2o_results["co2e_volatilization_kg"], 2),
                    "ipcc_soil_indirect_n2o_leaching": round(n2o_results["co2e_leaching_kg"], 2),
                    "pesticides_manufacturing": round(pesticide_mfg_co2e, 2),
                    "sprayer_petrol": round(sprayer_petrol_co2e, 2)
                },
                provenance_reference="IPCC 2019 Refinement to 2006 Guidelines (Tier 1 N2O) & Fertilizers Europe LCA"
            ),
            StageEmissionBreakdown(
                stage_id="stage_4_irrigation",
                stage_name="Stage 4: Irrigation & Pumping",
                emissions_kg_co2e=round(stage4_total, 2),
                emissions_kg_co2e_per_ha=round(stage4_total / area_ha, 2),
                percentage_of_total=round((stage4_total / total_cycle_emissions) * 100, 2),
                primary_driver=f"Groundwater lifting from {round(effective_depth_m)} m depth powered by {irr_in.energy_source.replace('_', ' ')}",
                sub_components={
                    "water_pumped_m3": round(irrigation_results["water_volume_m3"], 1),
                    "pumping_energy_kwh": round(irrigation_results["energy_consumption_kwh"], 1),
                    "pumping_hours": round(irrigation_results["pumping_hours"], 1),
                    "irrigation_emissions": round(stage4_total, 2)
                },
                provenance_reference="Central Ground Water Board (CGWB) Tumkur Hydrogeology & CEA CO2 Baseline v21.0"
            ),
            StageEmissionBreakdown(
                stage_id="stage_5_crop_maintenance",
                stage_name="Stage 5: Crop Maintenance",
                emissions_kg_co2e=round(stage5_total, 2),
                emissions_kg_co2e_per_ha=round(stage5_total / area_ha, 2),
                percentage_of_total=round((stage5_total / total_cycle_emissions) * 100, 2),
                primary_driver="Staking materials (bamboo & polypropylene twine) and inter-row weeding fuel",
                sub_components={
                    "staking_emissions": round(staking_co2e, 2),
                    "mulch_film_emissions": round(mulch_co2e, 2),
                    "intercultivation_diesel": round(intercult_fuel_co2e, 2)
                },
                provenance_reference="Karnataka Horticultural Crop Calendar & UAS Bengaluru Vegetable Agronomy"
            ),
            StageEmissionBreakdown(
                stage_id="stage_6_harvest_postharvest",
                stage_name="Stage 6: Harvest & Post-Harvest",
                emissions_kg_co2e=round(stage6_total, 2),
                emissions_kg_co2e_per_ha=round(stage6_total / area_ha, 2),
                percentage_of_total=round((stage6_total / total_cycle_emissions) * 100, 2),
                primary_driver="Packaging crate life cycle footprint and cold storage conditioning",
                sub_components={
                    "packaging_crates": round(packaging_co2e, 2),
                    "cold_storage_energy": round(cold_storage_co2e, 2),
                    "field_sorting_and_picking": round(harvest_labor_machinery_co2e, 2),
                    "post_harvest_loss_allocated_kg": round(gross_yield_kg * post_harvest_loss_fraction, 1)
                },
                provenance_reference="CIPHET / ICAR Post-Harvest Loss Assessment & Reusable Crate LCA"
            ),
            StageEmissionBreakdown(
                stage_id="stage_7_transport",
                stage_name="Stage 7: Transport & Logistics",
                emissions_kg_co2e=round(stage7_total, 2),
                emissions_kg_co2e_per_ha=round(stage7_total / area_ha, 2),
                percentage_of_total=round((stage7_total / total_cycle_emissions) * 100, 2),
                primary_driver=f"Road freight to {trans_in.destination_market} ({round(effective_dist_km, 1)} km) via {trans_in.vehicle_type.replace('_', ' ')}",
                sub_components={
                    "freight_tonne_km": round(transport_results["total_freight_tkm"], 1),
                    "trips_count": transport_results["trips_required"],
                    "vehicle_payload_tons": transport_results["payload_tons"],
                    "transport_emissions": round(stage7_total, 2)
                },
                provenance_reference="India GHG Program Freight Logistics Protocol & ARAI BS-VI Fuel Baselines"
            )
        ]

        # Identify Hotspot
        sorted_stages = sorted(stage_items, key=lambda s: s.emissions_kg_co2e, reverse=True)
        top_stage = sorted_stages[0]
        hotspot = HotspotAnalysis(
            top_stage_id=top_stage.stage_id,
            top_stage_name=top_stage.stage_name,
            emissions_kg_co2e=top_stage.emissions_kg_co2e,
            percentage_of_total=top_stage.percentage_of_total,
            primary_cause=top_stage.primary_driver,
            mitigation_potential_kg_co2e=round(top_stage.emissions_kg_co2e * 0.40, 2)
        )

        # Inefficiencies and Recommendations
        raw_emissions_dict = {
            "seed": stage1_total,
            "land_prep": stage2_total,
            "fertilizer": stage3_total,
            "irrigation": stage4_total,
            "crop_maintenance": stage5_total,
            "harvest": stage6_total,
            "transport": stage7_total,
            "total": total_cycle_emissions
        }
        inefficiencies = analyze_inefficiencies(request, raw_emissions_dict)
        recs_data = generate_recommendations(request, raw_emissions_dict, total_cycle_emissions)
        recommendations = [DecarbonizationRecommendation(**r) for r in recs_data]

        # Regional Benchmark Comparisons
        # Conventional Tumakuru Benchmark: ~0.172 kg CO2e/kg (5,337 kg CO2e/ha @ 31,000 kg yield)
        # Recommended BMP Benchmark: ~0.073 kg CO2e/kg (3,557 kg CO2e/ha @ 54,000 kg yield)
        # Solar Regenerative Benchmark: ~0.030 kg CO2e/kg (1,273 kg CO2e/ha @ 46,000 kg yield)
        benchmarks = [
            BenchmarkComparison(
                benchmark_name="Tumakuru Conventional Flood Baseline",
                carbon_footprint_kg_co2e_per_kg=0.205,
                total_cycle_emissions_kg_co2e_per_ha=5337.0,
                difference_percentage=round(((footprint_per_kg_marketable - 0.205) / 0.205) * 100, 1)
            ),
            BenchmarkComparison(
                benchmark_name="UAS Bengaluru Recommended Drip Fertigation BMP",
                carbon_footprint_kg_co2e_per_kg=0.073,
                total_cycle_emissions_kg_co2e_per_ha=3557.0,
                difference_percentage=round(((footprint_per_kg_marketable - 0.073) / 0.073) * 100, 1)
            ),
            BenchmarkComparison(
                benchmark_name="Solar PV Regenerative & Bio-Integrated Archetype",
                carbon_footprint_kg_co2e_per_kg=0.030,
                total_cycle_emissions_kg_co2e_per_ha=1273.0,
                difference_percentage=round(((footprint_per_kg_marketable - 0.030) / 0.030) * 100, 1)
            )
        ]

        # Potential reduction: If all recommended pathways implemented
        total_mitigation = sum([r.potential_reduction_kg_co2e for r in recommendations])
        mitigation_pct = round(min(88.0, (total_mitigation / total_cycle_emissions) * 100), 1) if total_cycle_emissions > 0 else 0.0

        # Persist assessment record into local SQLite database
        try:
            from app.db.database import get_connection
            import uuid, datetime
            conn = get_connection()
            cursor = conn.cursor()
            ass_id = f"LCA-TMK-{uuid.uuid4().hex[:6].upper()}"
            cursor.execute("""
            INSERT INTO lca_assessments 
            (assessment_id, state_id, state, district_id, district, taluk_id, taluk, village_id, village, farm_id, farm_name, crop_cycle_id, crop_name, variety_name, cultivated_area_ha, gross_yield_kg, marketable_yield_kg, total_cycle_emissions_kg_co2e, emissions_per_ha_kg_co2e, footprint_per_kg_marketable, top_hotspot_stage, top_hotspot_pct, potential_reduction_pct, stage_breakdown_json, recommendations_json, created_at)
            VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, ?, ?, ?, ?, ?, 'Tomato (Solanum lycopersicum)', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                ass_id, request.taluk_id, taluk_info["name"], request.village_id or "VIL-001",
                request.village_id or "Tumakuru Village", request.farm_id or "TMK-FARM",
                request.farm_name, request.crop_cycle_id or "CYC-2026", request.variety_name,
                area_ha, gross_yield_kg, marketable_yield_kg, round(total_cycle_emissions, 2),
                round(emissions_per_ha, 2), round(footprint_per_kg_marketable, 4),
                top_stage.stage_name, top_stage.percentage_of_total, mitigation_pct,
                json.dumps([s.model_dump() for s in stage_items]),
                json.dumps([r.model_dump() for r in recommendations]),
                datetime.datetime.utcnow().isoformat()
            ))
            conn.commit()
            conn.close()
        except Exception as db_err:
            print("Warning: could not persist LCA to local SQLite:", db_err)

        return FarmCycleLcaResponse(
            meta={
                "project_title": "Tomato CarbonTrace",
                "location": {
                    "country": "India",
                    "state": "Karnataka",
                    "district": "Tumakuru",
                    "taluk": taluk_info["name"],
                    "apmc_hub": "Antharasanahalli APMC Market Yard, Tumakuru",
                    "agro_climatic_zone": taluk_info["soil_type"]
                },
                "crop": {
                    "botanical_name": "Solanum lycopersicum",
                    "common_name": "Tomato",
                    "variety_name": request.variety_name,
                    "cultivated_area_ha": area_ha
                },
                "standards_used": [
                    "ISO 14040:2006 / ISO 14044:2006 (LCA Principles & Framework)",
                    "IPCC 2019 Refinement to 2006 Guidelines for National GHG Inventories (Vol 4 AFOLU)",
                    "Central Electricity Authority (CEA) CO2 Baseline Database v21.0 (Ministry of Power)"
                ]
            },
            summary={
                "total_cycle_emissions_kg_co2e": round(total_cycle_emissions, 2),
                "emissions_kg_co2e_per_ha": round(emissions_per_ha, 2),
                "footprint_kg_co2e_per_kg_marketable": round(footprint_per_kg_marketable, 4),
                "footprint_kg_co2e_per_kg_farmgate": round(footprint_per_kg_gross_farmgate, 4),
                "gross_harvest_yield_kg": round(gross_yield_kg, 1),
                "marketable_yield_kg": round(marketable_yield_kg, 1),
                "post_harvest_loss_pct": harv_in.post_harvest_loss_pct,
                "potential_carbon_reduction_pct": mitigation_pct,
                "potential_emission_savings_kg_co2e": round(total_mitigation, 2)
            },
            stage_breakdown=stage_items,
            hotspot=hotspot,
            recommendations=recommendations,
            benchmarks=benchmarks,
            inefficiencies_flagged=inefficiencies
        )

