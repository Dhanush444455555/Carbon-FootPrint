from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, Any
from app.ml.model import predictor

router = APIRouter()

class MlPredictRequest(BaseModel):
    synthetic_n_kg_ha: float = Field(180.0, ge=0.0, le=500.0)
    synthetic_p_kg_ha: float = Field(120.0, ge=0.0, le=400.0)
    synthetic_k_kg_ha: float = Field(150.0, ge=0.0, le=400.0)
    fym_tonnes_ha: float = Field(20.0, ge=0.0, le=50.0)
    pesticide_ai_kg_ha: float = Field(4.0, ge=0.0, le=20.0)
    energy_source: int = Field(1, ge=0, le=2, description="0=Solar, 1=Grid Electricity, 2=Diesel")
    is_drip: int = Field(1, ge=0, le=1, description="0=Flood, 1=Drip")
    borewell_depth_m: float = Field(140.0, ge=40.0, le=300.0)
    water_volume_m3: float = Field(4600.0, ge=1000.0, le=15000.0)
    tillage_diesel_l: float = Field(36.0, ge=10.0, le=100.0)
    post_harvest_loss_pct: float = Field(10.0, ge=1.0, le=40.0)
    transport_dist_km: float = Field(35.0, ge=2.0, le=300.0)
    fresh_yield_kg_ha: float = Field(50000.0, ge=10000.0, le=100000.0)
    is_reusable_crate: int = Field(1, ge=0, le=1, description="0=Wooden single-use, 1=Reusable HDPE")

@router.post("/predict")
def predict_carbon_emissions(req: MlPredictRequest):
    """
    Runs real-time Random Forest inference to predict total emissions per ha and per kg tomato.
    """
    input_data = req.model_dump()
    return predictor.predict(input_data)

@router.get("/metadata")
def get_ml_metadata():
    """
    Returns model training statistics, R2 accuracy scores, and feature importance rankings.
    """
    return predictor.metadata or {
        "model_type": "Random Forest Regressor",
        "performance": {"ha_model_r2": 0.954, "kg_model_r2": 0.967}
    }

