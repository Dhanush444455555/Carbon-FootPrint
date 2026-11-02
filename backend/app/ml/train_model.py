"""
Random Forest ML Model Training Script
Tomato Carbon Footprint Prediction – Tumakuru District, Karnataka.

Trains two models:
  1. rf_co2e_ha_model: Predicts total kg CO2e per hectare
  2. rf_co2e_kg_model: Predicts kg CO2e per kg marketable tomato

Uses synthetic training data calibrated to Tumakuru farming conditions.
Real training data should be substituted when primary survey data is collected.
"""
import numpy as np
import json
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error

SAVED_MODELS_DIR = Path(__file__).resolve().parent / "saved_models"
SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

# -------------------------------------------------------
# Synthetic Training Data Generator (Tumakuru-calibrated)
# -------------------------------------------------------
N = 3000  # Training samples

def generate_tumakuru_dataset(n: int) -> np.ndarray:
    """
    Generates synthetic farming records representative of the
    range of practices observed in Tumakuru district.
    """
    # Feature distributions based on field advisory literature (KVK Tumakuru, UAS Dharwad)
    synthetic_n_kg_ha = np.random.uniform(80, 350, n)     # N applied: 80-350 kg/ha
    synthetic_p_kg_ha = np.random.uniform(40, 200, n)     # P2O5: 40-200 kg/ha
    synthetic_k_kg_ha = np.random.uniform(50, 200, n)     # K2O: 50-200 kg/ha
    fym_tonnes_ha     = np.random.uniform(0, 40, n)       # FYM: 0-40 t/ha
    pesticide_ai_kg_ha = np.random.uniform(1, 15, n)      # Pesticide AI: 1-15 kg/ha
    energy_source     = np.random.randint(0, 3, n)        # 0=solar,1=grid,2=diesel
    is_drip           = np.random.randint(0, 2, n)        # 0=flood,1=drip
    borewell_depth_m  = np.random.uniform(80, 280, n)     # 80–280 m depth
    water_volume_m3   = np.random.uniform(1500, 12000, n) # Water applied
    tillage_diesel_l  = np.random.uniform(20, 90, n)      # Diesel for tillage
    post_harvest_loss = np.random.uniform(5, 35, n)       # PHL %
    transport_dist_km = np.random.uniform(5, 150, n)      # Farm-to-market km
    fresh_yield_kg_ha = np.random.uniform(15000, 100000, n)
    is_reusable_crate = np.random.randint(0, 2, n)        # 0=wood,1=HDPE

    X = np.column_stack([
        synthetic_n_kg_ha, synthetic_p_kg_ha, synthetic_k_kg_ha,
        fym_tonnes_ha, pesticide_ai_kg_ha, energy_source, is_drip,
        borewell_depth_m, water_volume_m3, tillage_diesel_l,
        post_harvest_loss, transport_dist_km, fresh_yield_kg_ha,
        is_reusable_crate
    ])
    return X, fresh_yield_kg_ha, post_harvest_loss


def compute_labels(X: np.ndarray, fresh_yield, phl_pct) -> tuple:
    """
    Generate emission labels using the analytical LCA model
    (same emission factors as TomatoLcaCalculator).
    """
    n = X.shape[0]
    # Unpack features
    synth_n = X[:, 0]; synth_p = X[:, 1]; synth_k = X[:, 2]
    fym_t   = X[:, 3]; pest_ai = X[:, 4]
    e_src   = X[:, 5]; is_drip = X[:, 6]
    bw_dep  = X[:, 7]; water   = X[:, 8]
    tractor = X[:, 9]; phl     = X[:, 10]
    dist    = X[:, 11]; yield_  = X[:, 12]
    crate   = X[:, 13]

    # Stage 1: Seed & Nursery (~16 kg CO2e/ha typical)
    s1 = np.full(n, 18.125)

    # Stage 2: Land Prep (diesel * 3.204)
    s2 = tractor * 3.204

    # Stage 3: Fertilizers (upstream manufacturing + IPCC N2O)
    urea_N  = synth_n * 0.46 * 2.62
    dap_N   = synth_p * 0.18 * 2.42
    mop_K   = synth_k * 0.6  * 0.46
    fym_co2 = fym_t * 1000   * 0.0044
    pest_co2 = pest_ai * 18.0

    # IPCC 2019 N2O (direct + indirect)
    organic_n = fym_t * 1000 * 0.0051
    n2o_direct = ((synth_n * 0.010) + (organic_n * 0.010)) * (44/28) * 273
    n2o_indir  = (synth_n * 0.10 * 0.01 + (synth_n + organic_n) * 0.24 * 0.0075) * (44/28) * 273
    s3 = urea_N + dap_N + mop_K + fym_co2 + pest_co2 + n2o_direct + n2o_indir

    # Stage 4: Irrigation
    pump_kw = 5.6  # typical 7.5HP pump = 5.59kW
    head_factor = bw_dep / 140.0
    water_raised_m3 = water
    energy_kwh = (pump_kw * water_raised_m3 * head_factor) / 36.0
    # Energy source factor
    ef_energy = np.where(e_src == 0, 0.0, np.where(e_src == 1, 0.835, 3.204 * 0.3))
    # Drip reduces water need
    water_factor = np.where(is_drip == 1, 0.62, 1.0)
    s4 = energy_kwh * ef_energy * water_factor + np.random.normal(0, 20, n).clip(0)

    # Stage 5: Crop Maintenance
    s5 = np.full(n, 74.5) + np.where(crate == 1, -3.2, 8.4)

    # Stage 6: Harvest & Packaging
    marketable = yield_ * (1 - phl / 100)
    packaging_ef = np.where(crate == 1, 0.0005, 0.0024)
    s6 = marketable * packaging_ef + np.where(phl > 20, phl * 2.1, 0)

    # Stage 7: Transport
    cargo_tons = marketable / 1000
    tkm = cargo_tons * dist
    transport_ef = 0.225  # LCV average
    s7 = tkm * transport_ef * 1.30

    total_co2e_ha = s1 + s2 + s3 + s4 + s5 + s6 + s7
    # Add realistic noise
    total_co2e_ha += np.random.normal(0, total_co2e_ha * 0.04)
    total_co2e_ha = total_co2e_ha.clip(200, 25000)

    co2e_per_kg = (total_co2e_ha / marketable).clip(0.01, 2.0)

    return total_co2e_ha, co2e_per_kg


print("Generating Tumakuru-calibrated synthetic training data...")
X, fresh_yield, phl_pct = generate_tumakuru_dataset(N)
y_ha, y_kg = compute_labels(X, fresh_yield, phl_pct)

print(f"  Samples: {N}")
print(f"  CO2e/ha range: {y_ha.min():.1f} – {y_ha.max():.1f}")
print(f"  CO2e/kg range: {y_kg.min():.4f} – {y_kg.max():.4f}")

# Train/test split
X_train, X_test, yha_train, yha_test, ykg_train, ykg_test = train_test_split(
    X, y_ha, y_kg, test_size=0.15, random_state=42
)

FEATURES = [
    "synthetic_n_kg_ha", "synthetic_p_kg_ha", "synthetic_k_kg_ha",
    "fym_tonnes_ha", "pesticide_ai_kg_ha", "energy_source", "is_drip",
    "borewell_depth_m", "water_volume_m3", "tillage_diesel_l",
    "post_harvest_loss_pct", "transport_dist_km", "fresh_yield_kg_ha",
    "is_reusable_crate"
]

print("\nTraining Random Forest – CO2e per hectare model...")
rf_ha = RandomForestRegressor(n_estimators=300, max_depth=18, min_samples_leaf=3, random_state=42, n_jobs=-1)
rf_ha.fit(X_train, yha_train)
r2_ha = r2_score(yha_test, rf_ha.predict(X_test))
mae_ha = mean_absolute_error(yha_test, rf_ha.predict(X_test))
print(f"  R² = {r2_ha:.4f}, MAE = {mae_ha:.1f} kg CO2e/ha")

print("Training Random Forest – CO2e per kg tomato model...")
rf_kg = RandomForestRegressor(n_estimators=300, max_depth=18, min_samples_leaf=3, random_state=42, n_jobs=-1)
rf_kg.fit(X_train, ykg_train)
r2_kg = r2_score(ykg_test, rf_kg.predict(X_test))
mae_kg = mean_absolute_error(ykg_test, rf_kg.predict(X_test))
print(f"  R² = {r2_kg:.4f}, MAE = {mae_kg:.4f} kg CO2e/kg")

# Feature importance
fi_ha = dict(zip(FEATURES, rf_ha.feature_importances_.round(4)))
fi_ha_sorted = dict(sorted(fi_ha.items(), key=lambda x: x[1], reverse=True))

# Save models
joblib.dump(rf_ha, SAVED_MODELS_DIR / "rf_co2e_ha_model.joblib", compress=3)
joblib.dump(rf_kg, SAVED_MODELS_DIR / "rf_co2e_kg_model.joblib", compress=3)
print(f"\nModels saved to: {SAVED_MODELS_DIR}")

metadata = {
    "model_type": "Random Forest Regressor",
    "n_estimators": 300,
    "training_samples": N,
    "test_samples": len(X_test),
    "data_type": "Synthetic – Tumakuru-calibrated archetypes (primary survey data pending)",
    "features": FEATURES,
    "performance": {
        "ha_model_r2": round(r2_ha, 4),
        "ha_model_mae_kg_co2e_per_ha": round(mae_ha, 1),
        "kg_model_r2": round(r2_kg, 4),
        "kg_model_mae_kg_co2e_per_kg": round(mae_kg, 5)
    },
    "feature_importances": fi_ha_sorted,
    "standards": ["ISO 14040/14044", "IPCC 2019 Refinement"],
    "geography": "Tumakuru District, Karnataka, India",
    "trained_at": "2026-11-03",
    "disclaimer": "Model trained on synthetic data calibrated to Tumakuru farming conditions. Accuracy will improve when real primary survey data is available."
}

with open(SAVED_MODELS_DIR / "model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("\nMetadata saved. Top 5 feature importances (CO2e/ha model):")
for feat, importance in list(fi_ha_sorted.items())[:5]:
    print(f"  {feat}: {importance:.4f}")

print("\n[OK] ML model training complete.")
