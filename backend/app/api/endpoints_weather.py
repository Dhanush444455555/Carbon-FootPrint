from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent

@router.get("")
def get_tumakuru_weather():
    """
    Returns monthly IMD climatological normals for Tumakuru, Karnataka,
    along with tomato growth stage durations, crop coefficients (Kc), and evapotranspiration (ETo).
    """
    with open(BASE_DIR / "data" / "weather_normals.json", "r") as f:
        return json.load(f)

