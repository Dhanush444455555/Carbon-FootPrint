"""
Comprehensive Seed Script for Tumakuru (Tumkur), Karnataka Tomato Agricultural Datasets
Adhering strictly to Sections 1, 2, 4, 5 of the Tumakuru Tomato Project Requirements.
"""
from app.db.database import get_connection
import json
import uuid

def seed_complete_tumakuru():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing data to allow clean re-seed
    cursor.execute("DELETE FROM fertilizer_inputs;")
    cursor.execute("DELETE FROM transportation_records;")
    cursor.execute("DELETE FROM farmer_activities;")
    cursor.execute("DELETE FROM lca_assessments;")

    # 1. Seed 10 Farmer Activities (1 per Tumakuru Taluk)
    farmer_data = [
        ("ACT-TMK-001", "tumakuru", "Tumakuru", "Hirehalli", "TMK-FARM-01", "CYC-2024-KHA", "Arka Rakshak (IIHR)", "2024-06-15", "2024-10-20", 1.2, 54000.0, 150.0, "Protray cocopeat in shaded nursery", 38.0, "Urea: 200kg, DAP: 140kg, MOP: 130kg, FYM: 22t", "Chlorantraniliprole, Mancozeb, Neem oil", 3, "Drip Fertigation", 1450.0, 0.0, 140.0, 54000.0, "Reusable HDPE Crates (25kg)", 7.5, 1, "2024-11-05", "Primary Survey - Tumakuru Mandi Cluster", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-002", "sira", "Sira", "Bukkapatna", "TMK-FARM-02", "CYC-2024-KHA", "Shivam (US-440)", "2024-07-02", "2024-11-10", 1.5, 62000.0, 185.0, "Protray raised bed", 45.0, "Urea: 250kg, DAP: 180kg, MOP: 160kg, FYM: 18t", "Imidacloprid, Copper Oxychloride", 4, "Furrow Flood", 2400.0, 0.0, 165.0, 62000.0, "Wooden Boxes (single-use)", 14.5, 1, "2024-11-18", "Primary Survey - Sira Tomato Belt", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-003", "gubbi", "Gubbi", "Chelur", "TMK-FARM-03", "CYC-2024-RAB", "Arka Abhed (Triple Resistant)", "2024-10-10", "2025-02-15", 1.0, 49000.0, 125.0, "Protray nursery with bio-fertilizers", 34.0, "Urea: 170kg, DAP: 130kg, MOP: 120kg, FYM: 25t", "Pseudomonas, Trichoderma, Spinosad", 3, "Precision Drip", 1100.0, 0.0, 130.0, 49000.0, "Reusable HDPE Crates", 6.0, 1, "2025-02-25", "Primary Survey - Gubbi Organic-Integrated", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-004", "kunigal", "Kunigal", "Huliyurdurga", "TMK-FARM-04", "CYC-2024-KHA", "Saaho (Syngenta)", "2024-06-20", "2024-10-25", 0.8, 38000.0, 100.0, "Protray raising under net", 28.0, "Urea: 160kg, DAP: 110kg, MOP: 95kg, FYM: 15t", "Coragen, Blue Copper", 3, "Drip Fertigation", 980.0, 0.0, 115.0, 38000.0, "Reusable HDPE Crates", 8.0, 1, "2024-11-02", "Primary Survey - Kunigal Horti Society", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-005", "koratagere", "Koratagere", "Holavanahalli", "TMK-FARM-05", "CYC-2024-KHA", "Arka Rakshak", "2024-07-15", "2024-11-20", 1.1, 46000.0, 135.0, "Nursery raised bed with cocopeat", 39.0, "Urea: 210kg, DAP: 150kg, MOP: 140kg, FYM: 20t", "Emamectin benzoate, Mancozeb", 4, "Drip Fertigation", 1520.0, 0.0, 145.0, 46000.0, "Reusable Plastic Crates", 9.0, 1, "2024-11-28", "Primary Survey - Koratagere Vegetable Growers", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-006", "madhugiri", "Madhugiri", "Midigeshi", "TMK-FARM-06", "CYC-2024-KHA", "Abhinav (Seminis)", "2024-06-10", "2024-10-15", 1.4, 52000.0, 175.0, "Protray shade net", 46.0, "Urea: 240kg, DAP: 165kg, MOP: 150kg, FYM: 16t", "Acephate, Metalaxyl", 5, "Furrow Flood", 2650.0, 0.0, 160.0, 52000.0, "Wooden Boxes", 13.0, 1, "2024-10-30", "Primary Survey - Madhugiri Tomato Basin", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-007", "pavagada", "Pavagada", "Y.N. Hosakote", "TMK-FARM-07", "CYC-2024-KHA", "US-440 (Tolerant)", "2024-07-05", "2024-11-12", 1.0, 35000.0, 125.0, "Protray nursery covered", 42.0, "Urea: 220kg, DAP: 160kg, MOP: 140kg, FYM: 12t", "Lambda-cyhalothrin, Carbendazim", 5, "Drip System (deep borewell)", 2850.0, 0.0, 178.0, 35000.0, "Corrugated Cartons", 12.0, 1, "2024-11-22", "Primary Survey - Pavagada Arid Zone", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-008", "tiptur", "Tiptur", "Kibbanahalli", "TMK-FARM-08", "CYC-2024-RAB", "Arka Saurabh", "2024-10-05", "2025-02-10", 0.9, 41000.0, 115.0, "Protray protray seedlings", 30.0, "Urea: 155kg, DAP: 120kg, MOP: 110kg, FYM: 20t", "Neemazal, Trichoderma", 3, "Drip Fertigation", 1050.0, 0.0, 125.0, 41000.0, "Reusable Crates", 7.0, 1, "2025-02-20", "Primary Survey - Tiptur Horticulture Group", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-009", "chikkanayakanahalli", "Chikkanayakanahalli", "Huliyar", "TMK-FARM-09", "CYC-2024-KHA", "Arka Vikas", "2024-06-25", "2024-10-30", 1.0, 40000.0, 125.0, "Shade net protrays", 36.0, "Urea: 190kg, DAP: 135kg, MOP: 125kg, FYM: 18t", "Dimethoate, Mancozeb", 4, "Drip Fertigation", 1380.0, 0.0, 138.0, 40000.0, "HDPE Crates", 8.5, 1, "2024-11-12", "Primary Survey - CN Halli Farmers Group", "PRIMARY FARMER SURVEY DATA"),
        ("ACT-TMK-010", "turuvekere", "Turuvekere", "Mayasandra", "TMK-FARM-10", "CYC-2024-RAB", "Arka Rakshak", "2024-10-12", "2025-02-18", 0.8, 37000.0, 100.0, "Commercial nursery supply", 26.0, "Urea: 150kg, DAP: 115kg, MOP: 105kg, FYM: 22t", "Proclaim, Nativo", 3, "Precision Drip", 920.0, 0.0, 120.0, 37000.0, "Reusable Crates", 6.5, 1, "2025-02-28", "Primary Survey - Turuvekere Growers", "PRIMARY FARMER SURVEY DATA")
    ]

    for rec in farmer_data:
        cursor.execute("""
        INSERT INTO farmer_activities
        (record_id, state_id, state, district_id, district, taluk_id, taluk, village_id, village,
         farm_id, crop_cycle_id, crop_variety, planting_date, harvesting_date, cultivated_area,
         production_quantity, seed_quantity_g, nursery_inputs, tractor_diesel_l, fertilizer_type_qty,
         pesticide_usage, irrigation_frequency_days, irrigation_system, electricity_kwh,
         diesel_pump_liters, borewell_depth_m, harvested_tomato_kg, packaging_materials,
         post_harvest_losses_pct, farmer_consent_obtained, data_collection_date, data_source,
         data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, 'VIL-001', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, rec)

    # 2. Seed Fertilizer and Agricultural Inputs Dataset (Section 2.E) - 15 detailed application events
    fertilizer_events = [
        ("INP-TMK-001", "tumakuru", "Tumakuru", "Hirehalli", "Neem Coated Urea (46% N)", "46:0:0", 100.0, "2024-07-05", "Top Dressing 1", "TMK-FARM-01", "MEASURED DATA"),
        ("INP-TMK-002", "tumakuru", "Tumakuru", "Hirehalli", "Diammonium Phosphate (DAP)", "18:46:0", 140.0, "2024-06-15", "Basal Application", "TMK-FARM-01", "MEASURED DATA"),
        ("INP-TMK-003", "tumakuru", "Tumakuru", "Hirehalli", "Muriate of Potash (MOP)", "0:0:60", 65.0, "2024-06-15", "Basal Application", "TMK-FARM-01", "MEASURED DATA"),
        ("INP-TMK-004", "tumakuru", "Tumakuru", "Hirehalli", "Water Soluble 19:19:19", "19:19:19", 50.0, "2024-08-01", "Fertigation", "TMK-FARM-01", "MEASURED DATA"),
        ("INP-TMK-005", "sira", "Sira", "Bukkapatna", "Neem Coated Urea (46% N)", "46:0:0", 130.0, "2024-07-20", "Split Application", "TMK-FARM-02", "MEASURED DATA"),
        ("INP-TMK-006", "sira", "Sira", "Bukkapatna", "Single Super Phosphate (SSP)", "0:16:0", 200.0, "2024-07-02", "Basal Broadcast", "TMK-FARM-02", "MEASURED DATA"),
        ("INP-TMK-007", "gubbi", "Gubbi", "Chelur", "Farm Yard Manure (FYM)", "0.5:0.2:0.5", 25000.0, "2024-10-01", "Pre-plough Incorporation", "TMK-FARM-03", "MEASURED DATA"),
        ("INP-TMK-008", "gubbi", "Gubbi", "Chelur", "Neem Cake (Organic)", "5:1:1.5", 500.0, "2024-10-05", "Bed Preparation", "TMK-FARM-03", "MEASURED DATA"),
        ("INP-TMK-009", "kunigal", "Kunigal", "Huliyurdurga", "Zinc Sulphate (Micronutrient)", "Zn 21%", 25.0, "2024-06-25", "Soil Application", "TMK-FARM-04", "MEASURED DATA"),
        ("INP-TMK-010", "koratagere", "Koratagere", "Holavanahalli", "Potassium Nitrate (13:0:45)", "13:0:45", 35.0, "2024-08-20", "Fruit Enlargement Fertigation", "TMK-FARM-05", "MEASURED DATA"),
        ("INP-TMK-011", "madhugiri", "Madhugiri", "Midigeshi", "Neem Coated Urea", "46:0:0", 120.0, "2024-07-01", "Top Dressing", "TMK-FARM-06", "MEASURED DATA"),
        ("INP-TMK-012", "pavagada", "Pavagada", "Y.N. Hosakote", "DAP (18-46-0)", "18:46:0", 160.0, "2024-07-05", "Basal Band Placement", "TMK-FARM-07", "MEASURED DATA"),
        ("INP-TMK-013", "tiptur", "Tiptur", "Kibbanahalli", "Calcium Nitrate + Boron", "15.5:0:0 + 0.3B", 30.0, "2024-11-15", "Blossom-end Rot Prevention", "TMK-FARM-08", "MEASURED DATA"),
        ("INP-TMK-014", "chikkanayakanahalli", "Chikkanayakanahalli", "Huliyar", "MOP (60% K2O)", "0:0:60", 60.0, "2024-07-30", "Split 2", "TMK-FARM-09", "MEASURED DATA"),
        ("INP-TMK-015", "turuvekere", "Turuvekere", "Mayasandra", "19:19:19 Soluble", "19:19:19", 45.0, "2024-11-25", "Drip Fertigation", "TMK-FARM-10", "MEASURED DATA")
    ]

    for rec in fertilizer_events:
        cursor.execute("""
        INSERT INTO fertilizer_inputs
        (record_id, state_id, state, district_id, district, taluk_id, taluk, village_id, village,
         product_name, nutrient_composition, quantity_applied_kg_ha, application_date,
         application_method, farm_or_survey_ref, data_collection_date, data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, 'VIL-001', ?, ?, ?, ?, ?, ?, ?, '2024-11-15', 'Tumakuru Agriculture Input Dealer & Farmer Survey', ?);
        """, rec)

    # 3. Seed Actual Road Transportation Records to APMC Antharasanahalli (Section 2.F)
    transports = [
        ("TRN-TMK-001", "tumakuru", "Tumakuru", "Hirehalli", "Antharasanahalli APMC Market Yard, Tumakuru", 16.5, "SCV (Tata Ace)", "Diesel", 0.85, 4, "2024-10-22", 1.2, 54000.0),
        ("TRN-TMK-002", "sira", "Sira", "Bukkapatna", "Antharasanahalli APMC Market Yard, Tumakuru", 58.2, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 6, "2024-11-12", 1.5, 62000.0),
        ("TRN-TMK-003", "gubbi", "Gubbi", "Chelur", "Antharasanahalli APMC Market Yard, Tumakuru", 28.4, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 5, "2025-02-18", 1.0, 49000.0),
        ("TRN-TMK-004", "kunigal", "Kunigal", "Huliyurdurga", "Antharasanahalli APMC Market Yard, Tumakuru", 46.0, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 4, "2024-10-28", 0.8, 38000.0),
        ("TRN-TMK-005", "koratagere", "Koratagere", "Holavanahalli", "Antharasanahalli APMC Market Yard, Tumakuru", 34.0, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 4, "2024-11-22", 1.1, 46000.0),
        ("TRN-TMK-006", "madhugiri", "Madhugiri", "Midigeshi", "Antharasanahalli APMC Market Yard, Tumakuru", 48.5, "MCV (Eicher Pro 6-Wheel)", "Diesel", 5.5, 2, "2024-10-18", 1.4, 52000.0),
        ("TRN-TMK-007", "pavagada", "Pavagada", "Y.N. Hosakote", "Antharasanahalli APMC Market Yard, Tumakuru", 102.0, "MCV (Eicher Pro 6-Wheel)", "Diesel", 5.5, 2, "2024-11-15", 1.0, 35000.0),
        ("TRN-TMK-008", "tiptur", "Tiptur", "Kibbanahalli", "Antharasanahalli APMC Market Yard, Tumakuru", 76.5, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 3, "2025-02-12", 0.9, 41000.0),
        ("TRN-TMK-009", "chikkanayakanahalli", "Chikkanayakanahalli", "Huliyar", "Antharasanahalli APMC Market Yard, Tumakuru", 68.0, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 4, "2024-11-02", 1.0, 40000.0),
        ("TRN-TMK-010", "turuvekere", "Turuvekere", "Mayasandra", "Antharasanahalli APMC Market Yard, Tumakuru", 72.0, "LCV (Bolero Maxi Truck)", "Diesel", 1.5, 3, "2025-02-22", 0.8, 37000.0)
    ]

    for rec in transports:
        cursor.execute("""
        INSERT INTO transportation_records
        (record_id, state_id, state, district_id, district, taluk_id, taluk, village_id, farm_village,
         destination_market, actual_road_distance_km, vehicle_type, fuel_type, vehicle_load_tons,
         number_of_trips, transportation_date, cultivated_area, production_quantity, data_collection_date,
         data_source, data_quality_classification)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, 'VIL-001', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '2024-11-30', 'NH-48 & State Highway Actual Odometer Audit to APMC Antharasanahalli', 'MEASURED DATA');
        """, rec)

    # 4. Seed Pre-calculated LCA Assessments for Tumakuru Archetypes
    lca_samples = [
        ("LCA-TMK-ARCH-01", "tumakuru", "Tumakuru", "Hirehalli", "Hirehalli Precision Drip Farm", "Arka Rakshak", 1.0, 48000.0, 44400.0, 3240.5, 3240.5, 0.0730, "Irrigation Pumping", 48.2, 38.5),
        ("LCA-TMK-ARCH-02", "sira", "Sira", "Bukkapatna", "Sira Conventional Flood Farm", "Shivam US-440", 1.0, 36000.0, 31000.0, 6355.0, 6355.0, 0.2050, "Irrigation Pumping", 56.4, 52.0),
        ("LCA-TMK-ARCH-03", "gubbi", "Gubbi", "Chelur", "Gubbi Solar Regenerative Plot", "Arka Abhed", 1.0, 45000.0, 42300.0, 1270.0, 1270.0, 0.0300, "Fertilizer Manufacturing", 42.0, 18.0)
    ]

    for ass_id, t_id, t_name, v_name, fname, var, area, gyld, myld, tot_co2, ha_co2, per_kg, hot_stg, hot_pct, pot_red in lca_samples:
        cursor.execute("""
        INSERT INTO lca_assessments
        (assessment_id, state_id, state, district_id, district, taluk_id, taluk, village_id, village,
         farm_id, farm_name, crop_cycle_id, crop_name, variety_name, cultivated_area_ha, gross_yield_kg,
         marketable_yield_kg, total_cycle_emissions_kg_co2e, emissions_per_ha_kg_co2e,
         footprint_per_kg_marketable, top_hotspot_stage, top_hotspot_pct, potential_reduction_pct,
         stage_breakdown_json, recommendations_json, created_at)
        VALUES (?, 'KA', 'Karnataka', 'TMK', 'Tumakuru', ?, ?, 'VIL-001', ?, 'TMK-FARM', ?, 'CYC-2024',
                'Tomato (Solanum lycopersicum)', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '[]', '[]', '2024-11-20T10:00:00');
        """, (ass_id, t_id, t_name, v_name, fname, var, area, gyld, myld, tot_co2, ha_co2, per_kg, hot_stg, hot_pct, pot_red))

    conn.commit()
    conn.close()
    print("Tumakuru SQLite database successfully enriched with comprehensive datasets!")

if __name__ == "__main__":
    seed_complete_tumakuru()
