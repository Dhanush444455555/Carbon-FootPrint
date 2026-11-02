from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent

@router.get("/taluks")
def get_tumakuru_taluks():
    """
    Returns geographical, soil, and hydrogeological data for all 10 taluks of Tumakuru.
    """
    with open(BASE_DIR / "data" / "taluks_tumakuru.json", "r") as f:
        return json.load(f)

@router.get("/emission-factors")
def get_emission_factors_provenance():
    """
    Returns full provenance ledger, measurement units, CEA baseline versions,
    and IPCC 2019 Refinement parameters.
    """
    with open(BASE_DIR / "data" / "emission_factors.json", "r") as f:
        return json.load(f)

