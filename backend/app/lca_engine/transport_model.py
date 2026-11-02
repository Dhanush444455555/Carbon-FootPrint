"""
Agricultural Transportation & Supply Chain Logistics Emissions Model
Calibrated for Tumakuru District Mandis and Highway Corridors (NH-48).
"""
from typing import Dict, Any

VEHICLE_EMISSION_FACTORS = {
    "scv_tata_ace": {
        "name": "Small Commercial Vehicle (Tata Ace / Jeeto)",
        "default_payload_tons": 0.85,
        "ef_kg_co2e_per_tkm": 0.292,
        "typical_mileage_km_l": 15.0
    },
    "lcv_bolero_dost": {
        "name": "Light Commercial Vehicle (Bolero Maxi / Dost)",
        "default_payload_tons": 1.5,
        "ef_kg_co2e_per_tkm": 0.225,
        "typical_mileage_km_l": 11.5
    },
    "mcv_eicher_6wheel": {
        "name": "Medium Commercial Vehicle (Eicher Pro 6-Wheel)",
        "default_payload_tons": 5.5,
        "ef_kg_co2e_per_tkm": 0.134,
        "typical_mileage_km_l": 6.0
    }
}

def calculate_transport_emissions(
    marketable_cargo_kg: float,
    one_way_distance_km: float,
    vehicle_type: str,
    custom_payload_tons: float = None
) -> Dict[str, Any]:
    """
    Computes freight emissions for delivering tomatoes from farm to wholesale market.
    Accounts for total required trips, vehicle capacity, and return journey allocation.
    """
    vehicle_info = VEHICLE_EMISSION_FACTORS.get(vehicle_type, VEHICLE_EMISSION_FACTORS["lcv_bolero_dost"])
    payload_tons = custom_payload_tons if custom_payload_tons and custom_payload_tons > 0 else vehicle_info["default_payload_tons"]
    
    cargo_tons = marketable_cargo_kg / 1000.0
    import math
    number_of_trips = max(1, math.ceil(cargo_tons / payload_tons))
    
    # In agricultural logistics, round trip includes empty or partially loaded return (typically allocated at 60% freight impact)
    total_travel_distance_km = number_of_trips * one_way_distance_km * 1.6
    
    # Tonne-Kilometers
    total_tkm = cargo_tons * one_way_distance_km
    
    # Emissions = tonne-km * EF_vehicle
    # We apply empty return factor (1.3x on freight emissions standard)
    emissions_kg_co2e = total_tkm * vehicle_info["ef_kg_co2e_per_tkm"] * 1.30

    return {
        "destination_distance_km": one_way_distance_km,
        "cargo_tons": round(cargo_tons, 2),
        "vehicle_type": vehicle_type,
        "vehicle_name": vehicle_info["name"],
        "payload_tons": payload_tons,
        "trips_required": number_of_trips,
        "total_freight_tkm": round(total_tkm, 2),
        "emissions_kg_co2e": round(emissions_kg_co2e, 2),
        "ef_tkm_used": vehicle_info["ef_kg_co2e_per_tkm"]
    }

