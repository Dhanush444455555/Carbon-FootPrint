"""
Tumakuru Data Intelligence API
Provides dataset coverage, provenance, and transparency metrics for
the Tumakuru Tomato Carbon Footprint project.
"""
from fastapi import APIRouter
from typing import Dict, Any, List
import json
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent


@router.get("/coverage")
def get_data_coverage() -> Dict[str, Any]:
    """
    Returns a structured summary of data coverage for the Tumakuru district.
    Separates MEASURED, OFFICIALLY REPORTED, SCIENTIFIC EF, and MODELLED data.
    """
    return {
        "geography": {
            "country": "India",
            "state": "Karnataka",
            "district": "Tumakuru",
            "total_taluks": 10,
            "taluks_with_data": 10,
            "district_validation": "ACTIVE",
            "boundary_source": "Karnataka Government – Tumakuru District Administration"
        },
        "data_categories": {
            "measured_data": {
                "label": "MEASURED DATA",
                "color": "emerald",
                "description": "Directly observed or experimentally measured values",
                "records": [
                    {
                        "name": "IMD Climatological Normals 1991–2020",
                        "type": "Weather Station Observations",
                        "station": "Tumakuru (IMD Station No. 43291)",
                        "variables": ["Temperature", "Rainfall", "Humidity"],
                        "status": "available",
                        "record_count": 12,
                        "unit": "monthly normals",
                        "source": "India Meteorological Department",
                        "quality": "HIGH"
                    },
                    {
                        "name": "Karnataka Dept of Agriculture – Season & Crop Report 2022–23",
                        "type": "Official Production Statistics",
                        "variables": ["Cultivated Area", "Production", "Yield"],
                        "status": "available",
                        "record_count": 10,
                        "unit": "taluk-level records",
                        "source": "Karnataka Dept of Agriculture",
                        "quality": "HIGH"
                    }
                ]
            },
            "officially_reported": {
                "label": "OFFICIALLY REPORTED DATA",
                "color": "blue",
                "description": "Statistics published by government bodies and regulatory agencies",
                "records": [
                    {
                        "name": "CEA CO2 Baseline Database v21.0",
                        "type": "Grid Emission Factor",
                        "variables": ["Southern Grid EF: 0.835 kg CO2e/kWh"],
                        "status": "available",
                        "source": "Central Electricity Authority, Ministry of Power, India",
                        "quality": "HIGH"
                    },
                    {
                        "name": "Agmarknet Market Arrivals & Prices",
                        "type": "Market Data",
                        "variables": ["Market arrivals", "Wholesale prices"],
                        "status": "partial",
                        "markets": ["Antharasanahalli APMC Tumakuru", "Sira APMC"],
                        "source": "National Informatics Centre – Agmarknet Portal",
                        "quality": "MEDIUM",
                        "note": "Historical records available; real-time API access requires registration"
                    },
                    {
                        "name": "KSRSAC / NBSS&LUP Soil Survey Karnataka",
                        "type": "Soil Data",
                        "variables": ["Soil type", "pH", "Organic carbon", "N/P/K"],
                        "status": "partial",
                        "source": "Karnataka State Remote Sensing Application Centre & ICAR-NBSS&LUP",
                        "quality": "MEDIUM",
                        "note": "District-level soil data available; farm-level soil testing pending"
                    }
                ]
            },
            "scientific_emission_factors": {
                "label": "SCIENTIFIC EMISSION FACTORS",
                "color": "purple",
                "description": "Peer-reviewed emission conversion factors from international scientific sources",
                "records": [
                    {
                        "name": "IPCC 2019 Refinement – Table 11.1",
                        "factor": "EF1 Synthetic N – 0.010 kg N2O-N / kg N",
                        "standard": "IPCC 2019 Refinement to 2006 IPCC Guidelines",
                        "status": "applied",
                        "quality": "HIGH"
                    },
                    {
                        "name": "Fertilizers Europe / ecoinvent 3.9",
                        "factor": "Urea manufacturing – 2.62 kg CO2e/kg",
                        "standard": "LCA database ecoinvent v3.9",
                        "status": "applied",
                        "quality": "HIGH"
                    },
                    {
                        "name": "India GHG Program – Diesel EF",
                        "factor": "Diesel well-to-wheel – 3.204 kg CO2e/L",
                        "standard": "India GHG Program & IPCC 2006",
                        "status": "applied",
                        "quality": "HIGH"
                    }
                ]
            },
            "modelled_estimated": {
                "label": "MODELLED / ESTIMATED DATA",
                "color": "amber",
                "description": "Values derived from models, proxies, or interpolation — clearly labelled as estimates",
                "records": [
                    {
                        "name": "Borewell Groundwater Depth (Hydrogeological Model)",
                        "type": "Estimated",
                        "source": "CGWB Karnataka Aquifer Mapping 2020 (district average)",
                        "note": "Taluk-level groundwater depth estimates used where farm-level data unavailable",
                        "quality": "MEDIUM"
                    },
                    {
                        "name": "Transport Distance (Road Network Estimate)",
                        "type": "Estimated",
                        "source": "OpenStreetMap Karnataka road network",
                        "note": "Road distances estimated from OSM; actual GPS-tracked routes not yet collected",
                        "quality": "MEDIUM"
                    },
                    {
                        "name": "Farmer Activity Data (Archetype Scenarios)",
                        "type": "Estimated",
                        "source": "UAS Dharwad + ICAR-IIHR advisory publications for Karnataka tomato cultivation",
                        "note": "Pre-configured farming archetypes based on extension advisory; NOT primary survey data. Primary survey data collection pending.",
                        "quality": "LOW"
                    }
                ]
            }
        },
        "dataset_counts": {
            "taluks_represented": 10,
            "villages_represented": "Expanding – primary survey pending",
            "verified_farm_records": 0,
            "production_records": 10,
            "weather_observations": 12,
            "soil_records": 10,
            "transportation_records": 0,
            "market_records": "Agmarknet (historical)"
        },
        "missing_datasets": [
            {
                "category": "Primary Farmer Survey Data",
                "priority": "HIGH",
                "description": "Farm-level primary survey data from individual tomato farmers in Tumakuru taluks is not yet collected.",
                "action": "Conduct structured field surveys across at least 5 taluks with minimum 30 farmers per taluk.",
                "affects": ["Farmer Activity Dataset", "Input Use Dataset", "Post-harvest Loss Dataset"]
            },
            {
                "category": "Real-time Weather Station Data",
                "priority": "MEDIUM",
                "description": "Current IMD data is based on 1991–2020 climatological normals. Real-time or recent-year station data not integrated.",
                "action": "Request official data from IMD Station 43291 Tumakuru for 2020–2025.",
                "affects": ["Weather Dataset", "Irrigation Water Balance"]
            },
            {
                "category": "Farm-level Soil Testing",
                "priority": "MEDIUM",
                "description": "District-level KSRSAC soil data is used. Individual farm-level soil test reports (N/P/K, pH, OC) are not collected.",
                "action": "Collect soil test reports from Karnataka Soil Testing Laboratories for sampled farms.",
                "affects": ["Soil Dataset", "Fertilizer Recommendation Accuracy"]
            },
            {
                "category": "GPS-tracked Transportation Routes",
                "priority": "MEDIUM",
                "description": "Actual road distances and routes used by farmers to transport tomatoes to APMC markets are not yet verified.",
                "action": "GPS track at least 50 farm-to-market trips across different taluks.",
                "affects": ["Transportation Dataset", "Stage 7 Emission Accuracy"]
            },
            {
                "category": "Electricity Consumption Records",
                "priority": "LOW",
                "description": "Farm-level electricity meter readings for borewell irrigation are not collected.",
                "action": "Collect BESCOM/electricity board meter records or farmer bills for surveyed farms.",
                "affects": ["Irrigation Energy Dataset"]
            }
        ],
        "collection_dates": {
            "weather_data": "IMD Normals 1991–2020",
            "production_data": "Karnataka Season & Crop Report 2022–23",
            "emission_factors": "IPCC 2019, CEA v21.0 (2023), ecoinvent 3.9",
            "soil_data": "KSRSAC/NBSS&LUP surveys (various years)",
            "market_data": "Agmarknet historical records",
            "project_start": "2026-11-03"
        },
        "geographic_validation": {
            "state_filter": "Karnataka",
            "district_filter": "Tumakuru",
            "excluded_districts": [
                "Bengaluru Urban", "Bengaluru Rural", "Chitradurga",
                "Hassan", "Mysuru", "Chikmagalur", "Mandya"
            ],
            "crop_filter": "Tomato (Solanum lycopersicum)",
            "validation_status": "ACTIVE – all records screened for Tumakuru boundary compliance"
        }
    }


@router.get("/sources")
def get_data_sources() -> List[Dict[str, Any]]:
    """
    Returns the prioritised data source hierarchy for the Tumakuru project.
    """
    return [
        {
            "rank": 1,
            "category": "District Government Records",
            "source": "Tumakuru District Administration – Agriculture Department",
            "status": "PARTIAL",
            "data_available": ["Horticulture area", "Production statistics"]
        },
        {
            "rank": 2,
            "category": "Karnataka Dept of Agriculture",
            "source": "KDA Season & Crop Report, Annual Statistical Reports",
            "status": "AVAILABLE",
            "data_available": ["Taluk-wise area", "Production", "Yield per ha"]
        },
        {
            "rank": 3,
            "category": "Karnataka Govt Statistical Publications",
            "source": "Directorate of Economics and Statistics Karnataka",
            "status": "AVAILABLE",
            "data_available": ["District agricultural statistics", "Input use surveys"]
        },
        {
            "rank": 4,
            "category": "Local Agricultural Research",
            "source": "UAS Dharwad, ICAR-IIHR Bangalore, KVK Tumakuru",
            "status": "PARTIAL",
            "data_available": ["Variety performance data", "Fertilizer recommendations"]
        },
        {
            "rank": 5,
            "category": "Official Weather Observations",
            "source": "IMD Station 43291 – Tumakuru",
            "status": "AVAILABLE (normals)",
            "data_available": ["Monthly climatological normals 1991–2020", "ETo estimates"]
        },
        {
            "rank": 6,
            "category": "Official Market Records",
            "source": "Agmarknet – Antharasanahalli APMC Tumakuru",
            "status": "AVAILABLE (historical)",
            "data_available": ["Market arrivals", "Wholesale prices", "Seasonal trends"]
        },
        {
            "rank": 7,
            "category": "Primary Farmer Survey",
            "source": "Direct survey of tomato farmers in Tumakuru",
            "status": "PENDING",
            "data_available": []
        },
        {
            "rank": 8,
            "category": "Scientific Emission Factors",
            "source": "IPCC 2019, ecoinvent 3.9, CEA v21.0, India GHG Program",
            "status": "AVAILABLE",
            "data_available": ["N2O emission factors", "Fertilizer manufacturing EFs", "Grid electricity EF", "Diesel EF", "Transport EFs"]
        }
    ]
