"""
Local SQL Database API Endpoints
Provides direct SQL queries, CRUD operations, and geographic data filtering for Tumakuru datasets.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import sqlite3
import json
from app.db.database import get_connection

router = APIRouter()

class SqlQueryRequest(BaseModel):
    query: str = Field(..., description="Read-only SELECT SQL query to execute")

class FarmerActivityCreateRequest(BaseModel):
    state_id: str = Field("KA", description="State identifier (Must be KA)")
    district_id: str = Field("TMK", description="District identifier (Must be TMK)")
    taluk_id: str = Field(..., description="One of 10 Tumakuru taluks")
    village: str = Field(..., description="Revenue village name")
    farm_id: str = Field(..., description="Farmer ID")
    crop_cycle_id: str = Field(..., description="Cycle ID")
    crop_name: str = Field("Tomato (Solanum lycopersicum)")
    crop_variety: Optional[str] = Field("Arka Rakshak")
    planting_date: str = Field("2024-06-15")
    harvesting_date: str = Field("2024-10-20")
    cultivated_area: float = Field(..., ge=0.01)
    production_quantity: float = Field(..., ge=0.0)
    seed_quantity_g: Optional[float] = Field(125.0)
    nursery_inputs: Optional[str] = Field("Protray shade net")
    tractor_diesel_l: Optional[float] = Field(35.0)
    fertilizer_type_qty: Optional[str] = Field("Urea 180kg, DAP 120kg, MOP 100kg")
    pesticide_usage: Optional[str] = Field("Recommended CIBRC doses")
    irrigation_frequency_days: Optional[int] = Field(3)
    irrigation_system: Optional[str] = Field("Drip Fertigation")
    electricity_kwh: Optional[float] = Field(1200.0)
    diesel_pump_liters: Optional[float] = Field(0.0)
    borewell_depth_m: Optional[float] = Field(140.0)
    harvested_tomato_kg: Optional[float] = Field(45000.0)
    packaging_materials: Optional[str] = Field("Reusable HDPE Crates")
    post_harvest_losses_pct: Optional[float] = Field(8.0)
    farmer_consent_obtained: int = Field(1)
    data_collection_date: str = Field("2024-11-01")
    data_source: str = Field("Primary Survey - Tumakuru Tomato Cluster")
    data_quality_classification: str = Field("PRIMARY FARMER SURVEY DATA")

@router.get("/tables")
def get_tables_summary():
    """Lists all tables in the local SQLite database along with record counts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row["name"] for row in cursor.fetchall()]
    
    summary = []
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) as cnt FROM {tbl};")
        cnt = cursor.fetchone()["cnt"]
        summary.append({"table_name": tbl, "record_count": cnt})
    
    conn.close()
    return {"database": "tumakuru_tomato.db", "tables": summary}

@router.get("/records/{table_name}")
def get_table_records(
    table_name: str,
    taluk_id: Optional[str] = Query(None, description="Filter by Tumakuru taluk ID"),
    limit: int = Query(50, ge=1, le=500)
):
    """Fetches records from a specified table with optional taluk filtering."""
    allowed_tables = {
        "taluks_master", "tomato_production", "farmer_activities",
        "tumakuru_weather", "tumakuru_soil", "fertilizer_inputs",
        "transportation_records", "market_records", "lca_assessments"
    }
    if table_name not in allowed_tables:
        raise HTTPException(status_code=400, detail=f"Invalid table name '{table_name}'.")

    conn = get_connection()
    cursor = conn.cursor()

    if taluk_id:
        cursor.execute(f"SELECT * FROM {table_name} WHERE taluk_id = ? LIMIT ?;", (taluk_id.lower(), limit))
    else:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT ?;", (limit,))

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"table": table_name, "count": len(rows), "records": rows}

@router.post("/execute")
def execute_sql_query(req: SqlQueryRequest):
    """Executes a safe read-only SQL query against the local SQLite database."""
    query_clean = req.query.strip()
    if not query_clean.lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed via this endpoint.")
    
    # Check for forbidden keywords
    forbidden = ["drop", "delete", "truncate", "update", "insert", "alter", "create"]
    tokens = query_clean.lower().split()
    if any(f in tokens for f in forbidden):
        raise HTTPException(status_code=400, detail="Query contains forbidden modification statements.")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query_clean)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"query": query_clean, "row_count": len(rows), "results": rows}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"SQL error: {str(e)}")

@router.post("/farmer-activities")
def create_farmer_activity_record(record: FarmerActivityCreateRequest):
    """Inserts a new primary farmer activity record into the SQLite database."""
    # Validate Tumakuru boundary
    if record.district_id.upper() not in {"TMK", "TUMAKURU"}:
        raise HTTPException(status_code=400, detail="District must be Tumakuru.")
    if record.state_id.upper() not in {"KA", "KARNATAKA"}:
        raise HTTPException(status_code=400, detail="State must be Karnataka.")
    
    valid_taluks = {
        "tumakuru", "tiptur", "kunigal", "gubbi", "koratagere",
        "madhugiri", "pavagada", "sira", "chikkanayakanahalli", "turuvekere"
    }
    if record.taluk_id.lower() not in valid_taluks:
        raise HTTPException(status_code=400, detail=f"Taluk '{record.taluk_id}' is not in Tumakuru district.")

    import uuid
    rec_id = f"ACT-TMK-{uuid.uuid4().hex[:6].upper()}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO farmer_activities
    (record_id, state_id, state, district_id, district, taluk_id, taluk, village_id, village,
     farm_id, crop_cycle_id, crop_name, crop_variety, planting_date, harvesting_date,
     cultivated_area, production_quantity, seed_quantity_g, nursery_inputs, tractor_diesel_l,
     fertilizer_type_qty, pesticide_usage, irrigation_frequency_days, irrigation_system,
     electricity_kwh, diesel_pump_liters, borewell_depth_m, harvested_tomato_kg,
     packaging_materials, post_harvest_losses_pct, farmer_consent_obtained,
     data_collection_date, data_source, data_quality_classification)
    VALUES (?, ?, 'Karnataka', ?, 'Tumakuru', ?, ?, 'VIL-001', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        rec_id, record.state_id.upper(), record.district_id.upper(), record.taluk_id.lower(),
        record.taluk_id.capitalize(), record.village, record.farm_id, record.crop_cycle_id,
        record.crop_name, record.crop_variety, record.planting_date, record.harvesting_date,
        record.cultivated_area, record.production_quantity, record.seed_quantity_g,
        record.nursery_inputs, record.tractor_diesel_l, record.fertilizer_type_qty,
        record.pesticide_usage, record.irrigation_frequency_days, record.irrigation_system,
        record.electricity_kwh, record.diesel_pump_liters, record.borewell_depth_m,
        record.harvested_tomato_kg, record.packaging_materials, record.post_harvest_losses_pct,
        record.farmer_consent_obtained, record.data_collection_date, record.data_source,
        record.data_quality_classification
    ))
    conn.commit()
    conn.close()

    return {"status": "success", "record_id": rec_id, "message": "Record inserted into local SQLite database"}
