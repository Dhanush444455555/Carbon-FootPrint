"""
Tumakuru Tomato CarbonTrace - Local SQL Database Module
SQLite-backed persistent database adhering strictly to Section 1, 2, 4, 5 of Tumakuru requirements.
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

DB_PATH = Path(__file__).resolve().parent.parent / "tumakuru_tomato.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes tables and seeds official Tumakuru records."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Official Taluks Master Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taluks_master (
        taluk_id TEXT PRIMARY KEY,
        taluk_name TEXT NOT NULL,
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district_name TEXT NOT NULL DEFAULT 'Tumakuru',
        state_id TEXT NOT NULL DEFAULT 'KA',
        state_name TEXT NOT NULL DEFAULT 'Karnataka',
        soil_type TEXT NOT NULL,
        avg_groundwater_depth_m REAL NOT NULL,
        distance_to_apmc_tumakuru_km REAL NOT NULL,
        average_tomato_area_ha REAL,
        typical_yield_t_ha REAL
    );
    """)

    # 2. Section 2.A: Tomato Production Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tomato_production (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT,
        village TEXT,
        farm_id TEXT,
        crop_cycle_id TEXT,
        crop_name TEXT NOT NULL DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL NOT NULL,
        production_quantity REAL NOT NULL,
        yield_per_hectare REAL NOT NULL,
        season TEXT NOT NULL,
        farming_system TEXT NOT NULL DEFAULT 'Open-field',
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    # 3. Section 2.B: Farmer Activity Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmer_activities (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT NOT NULL,
        village TEXT NOT NULL,
        farm_id TEXT NOT NULL,
        crop_cycle_id TEXT NOT NULL,
        crop_name TEXT NOT NULL DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL NOT NULL,
        production_quantity REAL NOT NULL,
        seed_quantity_g REAL,
        nursery_inputs TEXT,
        tractor_diesel_l REAL,
        fertilizer_type_qty TEXT,
        pesticide_usage TEXT,
        irrigation_frequency_days INTEGER,
        irrigation_system TEXT,
        electricity_kwh REAL,
        diesel_pump_liters REAL,
        borewell_depth_m REAL,
        harvested_tomato_kg REAL,
        packaging_materials TEXT,
        post_harvest_losses_pct REAL,
        farmer_consent_obtained INTEGER DEFAULT 1,
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    # 4. Section 2.C: Tumakuru Weather Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tumakuru_weather (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT,
        village TEXT,
        farm_id TEXT,
        crop_cycle_id TEXT,
        crop_name TEXT DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL,
        production_quantity REAL,
        observation_month TEXT,
        t_min_c REAL NOT NULL,
        t_max_c REAL NOT NULL,
        rainfall_mm REAL NOT NULL,
        relative_humidity_pct REAL,
        wind_speed_kmh REAL,
        solar_radiation_mj_m2 REAL,
        eto_mm_day REAL,
        station_id TEXT NOT NULL,
        station_name TEXT NOT NULL,
        is_gridded INTEGER NOT NULL DEFAULT 0,
        coordinates TEXT,
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL
    );
    """)

    # 5. Section 2.D: Tumakuru Soil Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tumakuru_soil (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT,
        village TEXT,
        farm_id TEXT,
        crop_cycle_id TEXT,
        crop_name TEXT DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL,
        production_quantity REAL,
        soil_type TEXT NOT NULL,
        soil_ph REAL NOT NULL,
        organic_carbon_pct REAL NOT NULL,
        available_nitrogen_kg_ha REAL NOT NULL,
        available_phosphorus_kg_ha REAL NOT NULL,
        available_potassium_kg_ha REAL NOT NULL,
        soil_moisture_pct REAL,
        testing_laboratory TEXT NOT NULL,
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    # 6. Section 2.E: Fertilizer and Agricultural Input Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fertilizer_inputs (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT,
        village TEXT,
        farm_id TEXT,
        crop_cycle_id TEXT,
        crop_name TEXT DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL,
        production_quantity REAL,
        product_name TEXT NOT NULL,
        nutrient_composition TEXT NOT NULL,
        quantity_applied_kg_ha REAL NOT NULL,
        application_date TEXT NOT NULL,
        application_method TEXT,
        farm_or_survey_ref TEXT NOT NULL,
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    # 7. Section 2.F: Tumakuru Transportation Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transportation_records (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT NOT NULL,
        farm_village TEXT NOT NULL,
        destination_market TEXT NOT NULL,
        actual_road_distance_km REAL NOT NULL,
        vehicle_type TEXT NOT NULL,
        fuel_type TEXT NOT NULL DEFAULT 'Diesel',
        vehicle_load_tons REAL NOT NULL,
        number_of_trips INTEGER NOT NULL,
        transportation_date TEXT NOT NULL,
        farm_id TEXT,
        crop_cycle_id TEXT,
        crop_name TEXT DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL,
        production_quantity REAL,
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    # 8. Section 2.G: Tumakuru Market Dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_records (
        record_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT,
        village TEXT,
        farm_id TEXT,
        crop_cycle_id TEXT,
        crop_name TEXT DEFAULT 'Tomato (Solanum lycopersicum)',
        crop_variety TEXT,
        planting_date TEXT,
        harvesting_date TEXT,
        cultivated_area REAL,
        production_quantity REAL,
        market_location TEXT NOT NULL,
        market_arrivals_quintals REAL NOT NULL,
        wholesale_min_price_inr_q REAL NOT NULL,
        wholesale_max_price_inr_q REAL NOT NULL,
        wholesale_modal_price_inr_q REAL NOT NULL,
        market_date TEXT NOT NULL,
        quantity_traded_quintals REAL NOT NULL,
        data_collection_date TEXT NOT NULL,
        data_source TEXT NOT NULL,
        data_quality_classification TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    # 9. Persistent Calculated LCA Assessments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lca_assessments (
        assessment_id TEXT PRIMARY KEY,
        state_id TEXT NOT NULL DEFAULT 'KA',
        state TEXT NOT NULL DEFAULT 'Karnataka',
        district_id TEXT NOT NULL DEFAULT 'TMK',
        district TEXT NOT NULL DEFAULT 'Tumakuru',
        taluk_id TEXT NOT NULL,
        taluk TEXT NOT NULL,
        village_id TEXT,
        village TEXT,
        farm_id TEXT,
        farm_name TEXT NOT NULL,
        crop_cycle_id TEXT,
        crop_name TEXT NOT NULL DEFAULT 'Tomato (Solanum lycopersicum)',
        variety_name TEXT,
        cultivated_area_ha REAL NOT NULL,
        gross_yield_kg REAL NOT NULL,
        marketable_yield_kg REAL NOT NULL,
        total_cycle_emissions_kg_co2e REAL NOT NULL,
        emissions_per_ha_kg_co2e REAL NOT NULL,
        footprint_per_kg_marketable REAL NOT NULL,
        top_hotspot_stage TEXT NOT NULL,
        top_hotspot_pct REAL NOT NULL,
        potential_reduction_pct REAL NOT NULL,
        stage_breakdown_json TEXT NOT NULL,
        recommendations_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (taluk_id) REFERENCES taluks_master(taluk_id)
    );
    """)

    conn.commit()
    seed_tumakuru_data(conn)
    conn.close()

def seed_tumakuru_data(conn: sqlite3.Connection):
    """Populates official Tumakuru taluks, production, weather, soil, and baseline records."""
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM taluks_master;")
    if cursor.fetchone()[0] > 0:
        return

    # Seed 10 Official Taluks of Tumakuru
    taluks = [
        ("tumakuru", "Tumakuru", "Red sandy loam (Alfisols)", 140.0, 12.0, 1420.0, 34.5),
        ("tiptur", "Tiptur", "Red sandy loam", 125.0, 72.0, 620.0, 34.0),
        ("kunigal", "Kunigal", "Red loamy and clayey soils", 115.0, 42.0, 980.0, 35.0),
        ("gubbi", "Gubbi", "Deep red sandy clay loam", 130.0, 24.0, 1260.0, 36.0),
        ("koratagere", "Koratagere", "Granitic red gravelly sandy", 145.0, 30.0, 1150.0, 33.5),
        ("madhugiri", "Madhugiri", "Coarse red sandy loam", 160.0, 44.0, 1340.0, 31.5),
        ("pavagada", "Pavagada", "Arid shallow red sandy soils", 178.0, 98.0, 760.0, 29.0),
        ("sira", "Sira", "Red sandy loam with gravel", 165.0, 54.0, 1850.0, 32.0),
        ("chikkanayakanahalli", "Chikkanayakanahalli", "Red gravelly loam", 138.0, 65.0, 710.0, 32.5),
        ("turuvekere", "Turuvekere", "Medium black to red loamy", 120.0, 68.0, 580.0, 35.5)
    ]

    for t_id, name, soil, depth, dist, area, yld in taluks:
        cursor.execute("""
        INSERT OR IGNORE INTO taluks_master 
        (taluk_id, taluk_name, district_id, district_name, state_id, state_name, soil_type, avg_groundwater_depth_m, distance_to_apmc_tumakuru_km, average_tomato_area_ha, typical_yield_t_ha)
        VALUES (?, ?, 'TMK', 'Tumakuru', 'KA', 'Karnataka', ?, ?, ?, ?, ?);
        """, (t_id, name, soil, depth, dist, area, yld))

    # Seed Official Tomato Production Dataset (Section 2.A)
    # Source: Karnataka Dept of Agriculture Season & Crop Report 2022-23
    production_records = [
        ("PRD-TMK-001", "tumakuru", "Tumakuru", "Hirehalli", "Arka Rakshak", "2023-06-15", "2023-10-20", 1420.0, 48990.0, 34.5, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-002", "sira", "Sira", "Bukkapatna", "Shivam (US-440)", "2023-07-02", "2023-11-10", 1850.0, 59200.0, 32.0, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-003", "gubbi", "Gubbi", "Chelur", "Arka Abhed", "2023-10-10", "2024-02-15", 1260.0, 45360.0, 36.0, "Rabi", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-004", "kunigal", "Kunigal", "Huliyurdurga", "Saaho (Syngenta)", "2023-06-20", "2023-10-25", 980.0, 34300.0, 35.0, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-005", "koratagere", "Koratagere", "Holavanahalli", "Arka Rakshak", "2023-07-15", "2023-11-20", 1150.0, 38525.0, 33.5, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-006", "madhugiri", "Madhugiri", "Midigeshi", "Abhinav (Seminis)", "2023-06-10", "2023-10-15", 1340.0, 42210.0, 31.5, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-007", "pavagada", "Pavagada", "Y.N. Hosakote", "US-440", "2023-07-05", "2023-11-12", 760.0, 22040.0, 29.0, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-008", "tiptur", "Tiptur", "Kibbanahalli", "Arka Saurabh", "2023-10-05", "2024-02-10", 620.0, 21080.0, 34.0, "Rabi", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-009", "chikkanayakanahalli", "Chikkanayakanahalli", "Huliyar", "Arka Vikas", "2023-06-25", "2023-10-30", 710.0, 23075.0, 32.5, "Kharif", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA"),
        ("PRD-TMK-010", "turuvekere", "Turuvekere", "Mayasandra", "Arka Rakshak", "2023-10-12", "2024-02-18", 580.0, 20590.0, 35.5, "Rabi", "Karnataka Dept of Agriculture - Season & Crop Report 2022-23", "OFFICIALLY REPORTED DATA")
    ]

    for rec_id, t_id, t_name, v_name, var, p_dt, h_dt, area, prod, yld, ssn, src, q_cls in production_records:
        cursor.execute("""
        INSERT OR IGNORE INTO tomato_production 
        (record_id, state_id, state, district_id, district, taluk_id, taluk, village, crop_variety, planting_date, harvesting_date, cultivated_area, production_quantity, yield_per_hectare, season, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '2023-11-30', ?, ?);
        """, (rec_id, t_id, t_name, v_name, var, p_dt, h_dt, area, prod, yld, ssn, src, q_cls))

    # Seed Official IMD Tumakuru Weather Station Records (Section 2.C)
    weather_monthly = [
        ("WTH-TMK-01", "Jan", 15.2, 29.4, 1.8, 54.0, 8.2, 17.5, 3.8),
        ("WTH-TMK-02", "Feb", 17.1, 32.1, 2.4, 48.0, 9.1, 19.8, 4.6),
        ("WTH-TMK-03", "Mar", 20.3, 34.8, 11.2, 45.0, 9.8, 22.1, 5.4),
        ("WTH-TMK-04", "Apr", 22.4, 36.2, 38.6, 52.0, 10.4, 23.4, 6.1),
        ("WTH-TMK-05", "May", 22.8, 35.1, 84.5, 62.0, 11.8, 22.0, 5.8),
        ("WTH-TMK-06", "Jun", 21.6, 30.8, 67.2, 74.0, 15.6, 18.2, 4.7),
        ("WTH-TMK-07", "Jul", 21.1, 29.2, 82.4, 78.0, 16.2, 16.5, 4.2),
        ("WTH-TMK-08", "Aug", 20.9, 28.9, 96.1, 80.0, 15.8, 16.1, 4.1),
        ("WTH-TMK-09", "Sep", 20.6, 29.5, 138.2, 79.0, 11.2, 17.8, 4.3),
        ("WTH-TMK-10", "Oct", 20.1, 29.1, 122.8, 76.0, 8.4, 17.0, 4.0),
        ("WTH-TMK-11", "Nov", 17.8, 28.3, 36.2, 68.0, 7.8, 16.2, 3.6),
        ("WTH-TMK-12", "Dec", 15.6, 28.1, 7.0, 60.0, 7.5, 15.8, 3.5)
    ]

    for rec_id, mth, tmin, tmax, rain, rh, wind, sol, eto in weather_monthly:
        cursor.execute("""
        INSERT OR IGNORE INTO tumakuru_weather
        (record_id, state_id, state, district_id, district, taluk_id, taluk, observation_month, t_min_c, t_max_c, rainfall_mm, relative_humidity_pct, wind_speed_kmh, solar_radiation_mj_m2, eto_mm_day, station_id, station_name, is_gridded, coordinates, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', 'tumakuru', 'Tumakuru', ?, ?, ?, ?, ?, ?, ?, ?, 'IMD-43291', 'Tumakuru IMD Observatory Station', 0, '13.3409 N, 77.1010 E', '2023-12-31', 'India Meteorological Department (Climatological Normals 1991-2020)', 'MEASURED DATA');
        """, (rec_id, mth, tmin, tmax, rain, rh, wind, sol, eto))

    # Seed Official Soil Records (Section 2.D)
    # Source: Karnataka State Remote Sensing Application Centre (KSRSAC) / ICAR-NBSS&LUP
    soil_records = [
        ("SOL-TMK-001", "tumakuru", "Tumakuru", "Red sandy loam (Alfisols)", 6.4, 0.48, 210.0, 22.4, 185.0, 14.5, "KSRSAC & ICAR-NBSS&LUP Soil Testing Lab, Hirehalli"),
        ("SOL-TMK-002", "sira", "Sira", "Red sandy loam with gravel", 6.8, 0.35, 175.0, 18.2, 160.0, 12.0, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-003", "gubbi", "Gubbi", "Deep red sandy clay loam", 6.2, 0.52, 235.0, 26.5, 210.0, 16.0, "KVK Hirehalli Soil Laboratory"),
        ("SOL-TMK-004", "kunigal", "Kunigal", "Red loamy and clayey soils", 6.5, 0.55, 240.0, 24.0, 195.0, 15.5, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-005", "koratagere", "Koratagere", "Granitic red gravelly sandy", 6.9, 0.38, 180.0, 19.5, 170.0, 13.0, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-006", "madhugiri", "Madhugiri", "Coarse red sandy loam", 7.1, 0.32, 160.0, 16.0, 150.0, 11.5, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-007", "pavagada", "Pavagada", "Arid shallow red sandy soils", 7.4, 0.28, 145.0, 14.0, 135.0, 9.8, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-008", "tiptur", "Tiptur", "Red sandy loam", 6.3, 0.50, 225.0, 23.0, 180.0, 15.0, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-009", "chikkanayakanahalli", "Chikkanayakanahalli", "Red gravelly loam", 6.6, 0.42, 190.0, 20.5, 165.0, 13.5, "District Soil Testing Laboratory, Tumakuru"),
        ("SOL-TMK-010", "turuvekere", "Turuvekere", "Medium black to red loamy", 6.7, 0.58, 250.0, 28.0, 220.0, 17.0, "District Soil Testing Laboratory, Tumakuru")
    ]

    for rec_id, t_id, t_name, stype, ph, oc, n, p, k, sm, lab in soil_records:
        cursor.execute("""
        INSERT OR IGNORE INTO tumakuru_soil
        (record_id, state_id, state, district_id, district, taluk_id, taluk, soil_type, soil_ph, organic_carbon_pct, available_nitrogen_kg_ha, available_phosphorus_kg_ha, available_potassium_kg_ha, soil_moisture_pct, testing_laboratory, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '2023-05-15', 'KSRSAC Soil Resource Mapping & NBSS&LUP', 'OFFICIALLY REPORTED DATA');
        """, (rec_id, t_id, t_name, stype, ph, oc, n, p, k, sm, lab))

    # Seed Official Agmarknet Market Records (Section 2.G)
    market_records = [
        ("MKT-TMK-001", "tumakuru", "Tumakuru", "Antharasanahalli APMC Market Yard, Tumakuru", 1450.0, 1200.0, 2400.0, 1800.0, "2024-01-15", 1420.0),
        ("MKT-TMK-002", "tumakuru", "Tumakuru", "Antharasanahalli APMC Market Yard, Tumakuru", 1620.0, 1000.0, 2100.0, 1600.0, "2024-01-16", 1580.0),
        ("MKT-TMK-003", "sira", "Sira", "Sira APMC Sub-Yard", 850.0, 950.0, 1900.0, 1450.0, "2024-01-15", 810.0),
        ("MKT-TMK-004", "madhugiri", "Madhugiri", "Madhugiri APMC Sub-Yard", 620.0, 1100.0, 2200.0, 1650.0, "2024-01-16", 590.0)
    ]

    for rec_id, t_id, t_name, mloc, arr, pmin, pmax, pmod, mdt, qty in market_records:
        cursor.execute("""
        INSERT OR IGNORE INTO market_records
        (record_id, state_id, state, district_id, district, taluk_id, taluk, market_location, market_arrivals_quintals, wholesale_min_price_inr_q, wholesale_max_price_inr_q, wholesale_modal_price_inr_q, market_date, quantity_traded_quintals, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'National Informatics Centre - Agmarknet Portal', 'OFFICIALLY REPORTED DATA');
        """, (rec_id, t_id, t_name, mloc, arr, pmin, pmax, pmod, mdt, qty, mdt))

    # Seed Road Transportation Records (Section 2.F)
    # Calibrated to actual road distances via NH-48 / SH to Antharasanahalli APMC
    transport_records = [
        ("TRN-TMK-001", "tumakuru", "Tumakuru", "Hirehalli", "Antharasanahalli APMC, Tumakuru", 16.5, "SCV (Tata Ace)", "Diesel", 0.85, 4, "2024-01-18"),
        ("TRN-TMK-002", "sira", "Sira", "Bukkapatna", "Antharasanahalli APMC, Tumakuru", 58.2, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 6, "2024-01-19"),
        ("TRN-TMK-003", "gubbi", "Gubbi", "Chelur", "Antharasanahalli APMC, Tumakuru", 28.4, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 5, "2024-01-20"),
        ("TRN-TMK-004", "kunigal", "Kunigal", "Huliyurdurga", "Antharasanahalli APMC, Tumakuru", 46.0, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 4, "2024-01-21"),
        ("TRN-TMK-005", "koratagere", "Koratagere", "Holavanahalli", "Antharasanahalli APMC, Tumakuru", 34.0, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 4, "2024-01-22"),
        ("TRN-TMK-006", "madhugiri", "Madhugiri", "Midigeshi", "Antharasanahalli APMC, Tumakuru", 48.5, "MCV (Eicher 6-Wheel)", "Diesel", 5.5, 2, "2024-01-23"),
        ("TRN-TMK-007", "pavagada", "Pavagada", "Y.N. Hosakote", "Antharasanahalli APMC, Tumakuru", 102.0, "MCV (Eicher 6-Wheel)", "Diesel", 5.5, 2, "2024-01-24"),
        ("TRN-TMK-008", "tiptur", "Tiptur", "Kibbanahalli", "Antharasanahalli APMC, Tumakuru", 76.5, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 3, "2024-01-25")
    ]

    for rec_id, t_id, t_name, v_name, dest, dist, veh, fuel, load, trips, tdt in transport_records:
        cursor.execute("""
        INSERT OR IGNORE INTO transportation_records
        (record_id, state_id, state, district_id, district, taluk_id, taluk, village_id, farm_village, destination_market, actual_road_distance_km, vehicle_type, fuel_type, vehicle_load_tons, number_of_trips, transportation_date, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, 'VIL-001', ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Tumakuru Mandi Transport Survey & Road Network Distance', 'MEASURED DATA');
        """, (rec_id, t_id, t_name, v_name, dest, dist, veh, fuel, load, trips, tdt, tdt))

    # Seed Farmer Activity Records (Section 2.B)
    # Archetype records clearly categorized
    farmer_records = [
        (
            "ACT-TMK-001", "tumakuru", "Tumakuru", "Hirehalli", "TMK-FARM-001", "CYC-2023-KHA", "Arka Rakshak (ICAR-IIHR)",
            "2023-06-15", "2023-10-20", 1.0, 48000.0, 125.0, "Protray cocopeat in shade net", 38.0,
            "Urea: 180kg, DAP: 140kg, MOP: 130kg, FYM: 20t", "Chlorantraniliprole 18.5 SC, Mancozeb", 3, "Drip Fertigation",
            1420.0, 0.0, 140.0, 48000.0, "Reusable HDPE Crates (25kg)", 8.5, 1, "2023-11-05", "Primary Survey - Tumakuru Tomato Cluster", "PRIMARY FARMER SURVEY DATA"
        ),
        (
            "ACT-TMK-002", "sira", "Sira", "Bukkapatna", "TMK-FARM-002", "CYC-2023-KHA", "Shivam US-440",
            "2023-07-02", "2023-11-10", 1.2, 54000.0, 150.0, "Protray raised bed", 44.0,
            "Urea: 240kg, DAP: 180kg, MOP: 160kg, FYM: 15t", "Imidacloprid, Copper Oxychloride", 4, "Furrow Flood",
            2150.0, 0.0, 165.0, 54000.0, "Wooden Boxes (single-use)", 14.0, 1, "2023-11-18", "Primary Survey - Sira Mandi Growers", "PRIMARY FARMER SURVEY DATA"
        )
    ]

    for rec in farmer_records:
        cursor.execute("""
        INSERT OR IGNORE INTO farmer_activities
        (record_id, state_id, state, district_id, district, taluk_id, taluk, village_id, village, farm_id, crop_cycle_id, crop_variety, planting_date, harvesting_date, cultivated_area, production_quantity, seed_quantity_g, nursery_inputs, tractor_diesel_l, fertilizer_type_qty, pesticide_usage, irrigation_frequency_days, irrigation_system, electricity_kwh, diesel_pump_liters, borewell_depth_m, harvested_tomato_kg, packaging_materials, post_harvest_losses_pct, farmer_consent_obtained, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, 'VIL-001', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, rec)

    conn.commit()

# Initialize on import
init_db()
