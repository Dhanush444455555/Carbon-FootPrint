from fastapi import APIRouter
from fastapi.responses import JSONResponse, PlainTextResponse
from app.schemas.farm_input import FarmCycleLcaRequest
from app.lca_engine.calculator import TomatoLcaCalculator
import io
import csv

router = APIRouter()

@router.post("/export-csv")
def export_lca_csv(request: FarmCycleLcaRequest):
    """
    Exports a structured CSV summary of the Life Cycle Carbon Assessment for the farm.
    """
    response = TomatoLcaCalculator.calculate(request)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["PROJECT", "Tomato CarbonTrace - AI-Based Carbon Footprint Tracking"])
    writer.writerow(["LOCATION", "Tumakuru District, Karnataka, India"])
    writer.writerow(["FARM NAME", request.farm_name])
    writer.writerow(["CULTIVATED AREA (HA)", request.farm_area_ha])
    writer.writerow([])
    writer.writerow(["METRIC", "VALUE", "UNIT"])
    writer.writerow(["Total Lifecycle Emissions", response.summary["total_cycle_emissions_kg_co2e"], "kg CO2e"])
    writer.writerow(["Emissions per Hectare", response.summary["emissions_kg_co2e_per_ha"], "kg CO2e / ha"])
    writer.writerow(["Carbon Footprint per kg Marketable Tomato", response.summary["footprint_kg_co2e_per_kg_marketable"], "kg CO2e / kg"])
    writer.writerow(["Total Harvest Yield", response.summary["gross_harvest_yield_kg"], "kg"])
    writer.writerow(["Marketable Yield", response.summary["marketable_yield_kg"], "kg"])
    writer.writerow(["Post-Harvest Loss", response.summary["post_harvest_loss_pct"], "%"])
    writer.writerow([])
    writer.writerow(["STAGE ID", "STAGE NAME", "EMISSIONS (KG CO2E)", "EMISSIONS PER HA", "SHARE (%)", "PRIMARY DRIVER"])
    for s in response.stage_breakdown:
        writer.writerow([s.stage_id, s.stage_name, s.emissions_kg_co2e, s.emissions_kg_co2e_per_ha, s.percentage_of_total, s.primary_driver])
    
    writer.writerow([])
    writer.writerow(["RECOMMENDED DECARBONIZATION INTERVENTIONS"])
    writer.writerow(["CATEGORY", "TITLE", "POTENTIAL REDUCTION (KG CO2E)", "PERCENT REDUCTION", "SCIENTIFIC BASIS"])
    for r in response.recommendations:
        writer.writerow([r.category, r.title, r.potential_reduction_kg_co2e, f"{r.potential_reduction_percentage}%", r.scientific_basis])
        
    return PlainTextResponse(output.getvalue(), media_type="text/csv")

