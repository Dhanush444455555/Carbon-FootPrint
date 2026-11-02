from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class StageEmissionBreakdown(BaseModel):
    stage_id: str
    stage_name: str
    emissions_kg_co2e: float
    emissions_kg_co2e_per_ha: float
    percentage_of_total: float
    primary_driver: str
    sub_components: Dict[str, float]
    provenance_reference: str

class HotspotAnalysis(BaseModel):
    top_stage_id: str
    top_stage_name: str
    emissions_kg_co2e: float
    percentage_of_total: float
    primary_cause: str
    mitigation_potential_kg_co2e: float

class DecarbonizationRecommendation(BaseModel):
    category: str
    title: str
    description: str
    potential_reduction_kg_co2e: float
    potential_reduction_percentage: float
    estimated_cost_impact: str
    scientific_basis: str

class BenchmarkComparison(BaseModel):
    benchmark_name: str
    carbon_footprint_kg_co2e_per_kg: float
    total_cycle_emissions_kg_co2e_per_ha: float
    difference_percentage: float

class FarmCycleLcaResponse(BaseModel):
    meta: Dict[str, Any]
    summary: Dict[str, Any]
    stage_breakdown: List[StageEmissionBreakdown]
    hotspot: HotspotAnalysis
    recommendations: List[DecarbonizationRecommendation]
    benchmarks: List[BenchmarkComparison]
    inefficiencies_flagged: List[Dict[str, Any]]

