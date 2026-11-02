"""
Tomato CarbonTrace Backend Service
API for Life Cycle Assessment, IPCC N2O Modelling, and Carbon Footprint Analytics.
Calibrated for Tumakuru District, Karnataka, India.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title="Tomato CarbonTrace API",
    description="Scientific LCA and Carbon Footprint Quantification for Tomato Farming in Tumakuru, Karnataka, India.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "project": "Tomato CarbonTrace",
        "description": "AI-Based Carbon Footprint Tracking from Seed to Market",
        "geography": "Tumakuru District, Karnataka, India",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "district": "Tumakuru",
        "standards": "ISO 14040/14044 & IPCC 2019 Refinement"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

