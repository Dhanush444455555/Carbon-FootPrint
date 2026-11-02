import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "Tomato CarbonTrace – AI-Based Carbon Footprint Tracking"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "ml" / "saved_models"
    DEFAULT_TALUK: str = "tumakuru"
    STATE: str = "Karnataka"
    DISTRICT: str = "Tumakuru"

settings = Settings()

