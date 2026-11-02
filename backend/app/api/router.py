from fastapi import APIRouter
from app.api import (
    endpoints_calc,
    endpoints_data,
    endpoints_ml,
    endpoints_weather,
    endpoints_report,
    endpoints_intelligence,
    endpoints_sql
)

api_router = APIRouter()

api_router.include_router(endpoints_calc.router, prefix="/lca", tags=["Life Cycle Assessment"])
api_router.include_router(endpoints_data.router, prefix="/data", tags=["Tumakuru Datasets & Provenance"])
api_router.include_router(endpoints_ml.router, prefix="/ml", tags=["Machine Learning Analytics"])
api_router.include_router(endpoints_weather.router, prefix="/weather", tags=["IMD Weather & Water Balance"])
api_router.include_router(endpoints_report.router, prefix="/report", tags=["Reports & Export"])
api_router.include_router(endpoints_intelligence.router, prefix="/intelligence", tags=["Tumakuru Data Intelligence"])
api_router.include_router(endpoints_sql.router, prefix="/sql", tags=["Local SQL Database"])

