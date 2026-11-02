from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class NurseryStageInput(BaseModel):
    seed_rate_g_ha: float = Field(125.0, ge=10.0, le=1000.0, description="Seed rate in grams per hectare")
    seedling_count_ha: int = Field(15000, ge=5000, le=35000, description="Number of seedlings raised in nursery")
    nursery_type: str = Field("protray_cocopeat", description="protray_cocopeat or raised_open_bed")
    nursery_electricity_kwh: float = Field(6.5, ge=0.0, le=100.0, description="Electricity for nursery misting/irrigation")
    nursery_to_farm_distance_km: float = Field(12.0, ge=0.0, le=150.0, description="Transit distance from nursery to field")
    seedling_transport_vehicle: str = Field("scv_tata_ace", description="Vehicle used for seedling transit")

class LandPrepStageInput(BaseModel):
    tractor_hp: float = Field(45.0, ge=20.0, le=100.0, description="Tractor rating in horsepower")
    disc_plough_passes: int = Field(1, ge=0, le=5, description="Primary ploughing passes")
    cultivator_passes: int = Field(2, ge=0, le=5, description="Secondary cultivator passes")
    rotavator_passes: int = Field(2, ge=0, le=5, description="Rotavator fine tilth passes")
    ridger_passes: int = Field(1, ge=0, le=3, description="Bed forming / ridge making passes")
    custom_diesel_consumption_l: Optional[float] = Field(None, ge=0.0, le=200.0, description="Override total diesel in liters/ha")

class FertilizerStageInput(BaseModel):
    urea_kg_ha: float = Field(200.0, ge=0.0, le=800.0, description="Urea (46% N) in kg/ha")
    dap_kg_ha: float = Field(150.0, ge=0.0, le=600.0, description="Diammonium Phosphate (18% N, 46% P2O5) in kg/ha")
    mop_kg_ha: float = Field(150.0, ge=0.0, le=500.0, description="Muriate of Potash (60% K2O) in kg/ha")
    ssp_kg_ha: float = Field(0.0, ge=0.0, le=500.0, description="Single Super Phosphate (16% P2O5) in kg/ha")
    complex_19_19_19_kg_ha: float = Field(50.0, ge=0.0, le=500.0, description="Water-soluble 19:19:19 in kg/ha")
    fym_tonnes_ha: float = Field(20.0, ge=0.0, le=50.0, description="Farm Yard Manure in tonnes/ha")
    pesticides_active_ingredient_kg_ha: float = Field(4.5, ge=0.0, le=25.0, description="Active ingredient of plant protection chemicals")
    knapsack_sprayer_petrol_l: float = Field(2.5, ge=0.0, le=30.0, description="Petrol consumed for mechanical sprayers")

class IrrigationStageInput(BaseModel):
    irrigation_system: str = Field("drip_fertigation", description="drip_fertigation or flood_furrow")
    pump_hp: float = Field(7.5, ge=2.0, le=25.0, description="Borewell submersible pump HP")
    energy_source: str = Field("grid_electricity", description="grid_electricity, diesel_generator, or solar_pv")
    borewell_dynamic_head_m: float = Field(140.0, ge=20.0, le=350.0, description="Dynamic groundwater pumping depth in meters")
    total_water_volume_m3_ha: Optional[float] = Field(None, ge=500.0, le=20000.0, description="Total irrigation water applied in m3/ha")
    pumping_hours_override: Optional[float] = Field(None, ge=0.0, le=1000.0, description="Explicit seasonal pumping hours")

class CropMaintenanceInput(BaseModel):
    growth_duration_days: int = Field(125, ge=90, le=160, description="Total days from transplant to final picking")
    staking_method: str = Field("bamboo_twine", description="bamboo_twine, wooden_stakes, or none")
    mulching_type: str = Field("polyethylene_silver_black", description="polyethylene_silver_black, organic_paddy_straw, or none")
    intercultivation_diesel_l: float = Field(12.0, ge=0.0, le=60.0, description="Diesel for mini-tiller weeding")

class HarvestStageInput(BaseModel):
    fresh_yield_kg_ha: float = Field(45000.0, ge=5000.0, le=120000.0, description="Gross harvest yield in kg/ha")
    post_harvest_loss_pct: float = Field(12.0, ge=1.0, le=40.0, description="Estimated post-harvest supply chain loss %")
    packaging_type: str = Field("reusable_hdpe_crate", description="reusable_hdpe_crate or wooden_corrugated")
    use_cold_storage: bool = Field(False, description="Whether refrigerated storage was used")
    cold_storage_days: int = Field(0, ge=0, le=60, description="Days stored in temperature-controlled room")

class TransportStageInput(BaseModel):
    destination_market: str = Field("Antharasanahalli APMC, Tumakuru", description="Target market")
    transport_distance_km: float = Field(28.0, ge=2.0, le=500.0, description="One-way transit distance in km")
    vehicle_type: str = Field("lcv_bolero_dost", description="scv_tata_ace, lcv_bolero_dost, or mcv_eicher_6wheel")
    vehicle_payload_tons: float = Field(1.5, ge=0.5, le=25.0, description="Payload capacity in metric tonnes")

VALID_TUMAKURU_TALUKS = {
    "tumakuru", "tiptur", "kunigal", "gubbi", "koratagere",
    "madhugiri", "pavagada", "sira", "chikkanayakanahalli", "turuvekere"
}

class FarmCycleLcaRequest(BaseModel):
    # Mandatory geographical boundary identifiers (Section 5)
    state_id: str = Field("KA", description="State identifier (Must be KA / Karnataka)")
    district_id: str = Field("TMK", description="District identifier (Must be TMK / Tumakuru)")
    taluk_id: str = Field("tumakuru", description="Taluk ID in Tumakuru district (1 of 10 official taluks)")
    village_id: Optional[str] = Field("Hirehalli", description="Official revenue village name or census code")
    farm_id: Optional[str] = Field("TMK-FARM-001", description="Unique farmer / survey record identifier")
    crop_cycle_id: Optional[str] = Field("CYC-2026-KHA", description="Seasonal crop cycle identifier")
    
    # Crop validation (Section 1 & 4)
    crop_name: str = Field("Tomato", description="Crop must be Tomato (Solanum lycopersicum)")
    farm_name: str = Field("Tumakuru Progressive Tomato Farm", description="Name of farm or survey entry")
    farm_area_ha: float = Field(1.0, ge=0.1, le=100.0, description="Cultivated land area in hectares")
    variety_name: str = Field("Arka Rakshak (ICAR-IIHR)", description="Cultivated tomato variety/hybrid")
    seed_nursery: NurseryStageInput = Field(default_factory=NurseryStageInput)
    land_prep: LandPrepStageInput = Field(default_factory=LandPrepStageInput)
    fertilizer: FertilizerStageInput = Field(default_factory=FertilizerStageInput)
    irrigation: IrrigationStageInput = Field(default_factory=IrrigationStageInput)
    crop_maintenance: CropMaintenanceInput = Field(default_factory=CropMaintenanceInput)
    harvest: HarvestStageInput = Field(default_factory=HarvestStageInput)
    transport: TransportStageInput = Field(default_factory=TransportStageInput)

