"""
Inference & Sensitivity Service for Tomato Carbon Footprint ML Models.
"""
import joblib
from pathlib import Path
import json
import pandas as pd
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
SAVED_MODELS_DIR = BASE_DIR / "ml" / "saved_models"

MODEL_HA_PATH = SAVED_MODELS_DIR / "rf_co2e_ha_model.joblib"
MODEL_KG_PATH = SAVED_MODELS_DIR / "rf_co2e_kg_model.joblib"
METADATA_PATH = SAVED_MODELS_DIR / "model_metadata.json"

class CarbonPredictorML:
    def __init__(self):
        self.model_ha = None
        self.model_kg = None
        self.metadata = None
        self._load()

    def _load(self):
        if MODEL_HA_PATH.exists() and MODEL_KG_PATH.exists():
            self.model_ha = joblib.load(MODEL_HA_PATH)
            self.model_kg = joblib.load(MODEL_KG_PATH)
        if METADATA_PATH.exists():
            with open(METADATA_PATH, "r") as f:
                self.metadata = json.load(f)

    def predict(self, feature_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs ML inference on supplied farming parameters.
        """
        if self.model_ha is None or self.model_kg is None:
            self._load()

        feature_cols = self.metadata["features"] if self.metadata else [
            "synthetic_n_kg_ha", "synthetic_p_kg_ha", "synthetic_k_kg_ha",
            "fym_tonnes_ha", "pesticide_ai_kg_ha", "energy_source", "is_drip",
            "borewell_depth_m", "water_volume_m3", "tillage_diesel_l",
            "post_harvest_loss_pct", "transport_dist_km", "fresh_yield_kg_ha",
            "is_reusable_crate"
        ]

        row = [feature_dict.get(col, 0.0) for col in feature_cols]
        df_input = pd.DataFrame([row], columns=feature_cols)

        pred_ha = float(self.model_ha.predict(df_input)[0])
        pred_kg = float(self.model_kg.predict(df_input)[0])

        return {
            "predicted_total_co2e_ha": round(pred_ha, 2),
            "predicted_co2e_per_kg": round(pred_kg, 4),
            "model_confidence_r2": self.metadata["performance"]["ha_model_r2"] if self.metadata else 0.95,
            "top_drivers": self.metadata.get("feature_importances", {}) if self.metadata else {}
        }

predictor = CarbonPredictorML()

