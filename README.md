# Tomato CarbonTrace 🍅 — Tumakuru District, Karnataka

AI-Based Carbon Footprint Quantification for Open-Field Tomato Cultivation from Seed to Market.
Calibrated strictly for **Tumakuru (Tumkur) District, Karnataka, India**.

Compliant with **ISO 14040/14044 LCA Principles** and the **IPCC 2019 Refinement to National GHG Inventories (Volume 4 AFOLU)**.

---

## 🌟 Key Features

* **Strict Geographic Enforcement:** Boundary locked to **Tumakuru District, Karnataka** across all 10 taluks:
  * *Tumakuru, Sira, Gubbi, Kunigal, Koratagere, Madhugiri, Pavagada, Tiptur, Chikkanayakanahalli, Turuvekere*
* **8-Stage Cradle-to-Market LCA:**
  1. Seed & Protray Nursery
  2. Land Preparation (Alfisols Tillage)
  3. Crop Nutrition & IPCC 2019 Soil N₂O
  4. Borewell Irrigation Pumping (Aquifer Dynamics)
  5. Staking & Trellis Crop Maintenance
  6. Harvesting & Packaging Loss
  7. Mandi Freight Transportation (NH-48 Corridor to APMC Antharasanahalli)
  8. End-of-Life & Crop Residue
* **Carbonlytics Modern UI:** Clean emissions overview, source breakdown donut chart, seasonal trends bar chart, smart forecast, and goal progress bars.
* **Farmer Logbook:** Non-technical, farmer-friendly activity tracking for surveys, inputs, soil health, and mandi trips.
* **Local Persistent Database:** SQLite database (`tumakuru_tomato.db`) storing verified records with mandatory fields (`state_id`, `district_id`, `taluk_id`, `village_id`, `farm_id`, `crop_cycle_id`).
* **Machine Learning Model:** Random Forest regressor ($R^2 = 0.954$) trained on regional agronomic parameters.

---

## 🚀 Quick Start

### 1. Backend (FastAPI + SQLite)
```bash
cd backend
pip install -r requirements.txt
python main.py
```
* API Server: `http://localhost:8000`
* Swagger Docs: `http://localhost:8000/docs`

### 2. Frontend (React + Vite + Tailwind CSS)
```bash
cd frontend
npm install
npm run dev
```
* Dashboard: `http://localhost:5173`

---

## 🌐 Deploy to Vercel

```bash
vercel --prod
```
Or connect this GitHub repository directly to [Vercel Dashboard](https://vercel.com/dhanush444455555s-projects):
1. **Import Git Repository:** Select `Dhanush444455555/Carbon-FootPrint`
2. **Build Command:** `cd frontend && npm install && npm run build`
3. **Output Directory:** `frontend/dist`
4. **Deploy!**

---

## 📜 Citations & Provenance
* **Meteorology:** IMD Station 43291 (Tumakuru) Climatological Normals
* **Agriculture Statistics:** Karnataka Department of Agriculture Season & Crop Report 2022–23
* **Soil Data:** KSRSAC & ICAR-NBSS&LUP Soil Mapping of Tumakuru
* **Grid Electricity:** Central Electricity Authority (CEA) Baseline Database v21.0
* **Emissions:** IPCC 2019 Refinement & ecoinvent v3.9
