import React, { useState } from 'react';
import {
  ChevronRight, ChevronLeft, CheckCircle, Loader2,
  Leaf, Droplets, Zap, Truck, Package, Wrench, Sun, Sprout
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { calculateLca } from '../services/api';

const TALUKS = [
  { value: 'tumakuru',          label: 'Tumakuru Taluk' },
  { value: 'sira',              label: 'Sira Taluk' },
  { value: 'gubbi',             label: 'Gubbi Taluk' },
  { value: 'kunigal',           label: 'Kunigal Taluk' },
  { value: 'koratagere',        label: 'Koratagere Taluk' },
  { value: 'madhugiri',         label: 'Madhugiri Taluk' },
  { value: 'pavagada',          label: 'Pavagada Taluk' },
  { value: 'tiptur',            label: 'Tiptur Taluk' },
  { value: 'turuvekere',        label: 'Turuvekere Taluk' },
  { value: 'chiknayakanhalli',  label: 'Chiknayakanhalli Taluk' },
];

const STEPS = [
  { id: 1, label: 'Farm Identity',    icon: Leaf },
  { id: 2, label: 'Seed & Nursery',   icon: Sprout },
  { id: 3, label: 'Land Preparation', icon: Wrench },
  { id: 4, label: 'Fertilizers',      icon: Zap },
  { id: 5, label: 'Irrigation',       icon: Droplets },
  { id: 6, label: 'Crop Maintenance', icon: Sun },
  { id: 7, label: 'Harvest',          icon: Package },
  { id: 8, label: 'Transport',        icon: Truck },
];

const inputCls = `w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100
  placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/30
  transition-colors`;

const labelCls = 'block text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wide';

function Field({ label, children }) {
  return (
    <div>
      <label className={labelCls}>{label}</label>
      {children}
    </div>
  );
}

export default function FarmInputForm() {
  const { setLcaResult, setIsLoading, navTo, VIEWS } = useApp();
  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    // Step 1
    farm_name: '',
    taluk_id: 'tumakuru',
    farm_area_ha: 1.0,
    variety_name: 'Arka Rakshak (ICAR-IIHR)',
    // Step 2
    seed_nursery: {
      seed_rate_g_ha: 125,
      seedling_count_ha: 15000,
      nursery_electricity_kwh: 6.5,
      nursery_to_farm_distance_km: 12,
    },
    // Step 3
    land_prep: {
      disc_plough_passes: 1,
      cultivator_passes: 2,
      rotavator_passes: 2,
      ridger_passes: 1,
      custom_diesel_consumption_l: '',
    },
    // Step 4
    fertilizer: {
      urea_kg_ha: 200,
      dap_kg_ha: 150,
      mop_kg_ha: 150,
      ssp_kg_ha: 0,
      complex_19_19_19_kg_ha: 50,
      fym_tonnes_ha: 20,
      pesticides_active_ingredient_kg_ha: 4.5,
      knapsack_sprayer_petrol_l: 2.5,
    },
    // Step 5
    irrigation: {
      irrigation_system: 'furrow_flood',
      pump_hp: 5,
      energy_source: 'grid_electricity',
      total_water_volume_m3_ha: 8500,
      borewell_dynamic_head_m: 140,
    },
    // Step 6
    crop_maintenance: {
      staking_method: 'bamboo_twine',
      mulching_type: 'polyethylene_silver_black',
      intercultivation_diesel_l: 12.0,
    },
    // Step 7
    harvest: {
      fresh_yield_kg_ha: 45000,
      post_harvest_loss_pct: 12.0,
      packaging_type: 'reusable_hdpe_crate',
      use_cold_storage: false,
      cold_storage_days: 0,
    },
    // Step 8
    transport: {
      destination_market: 'Antharasanahalli APMC',
      transport_distance_km: 28,
      vehicle_type: 'scv_tata_ace',
      payload_tonnes: 1.5,
    },
  });

  function update(path, value) {
    const keys = path.split('.');
    setFormData(prev => {
      const next = { ...prev };
      if (keys.length === 1) {
        next[keys[0]] = value;
      } else {
        next[keys[0]] = { ...next[keys[0]], [keys[1]]: value };
      }
      return next;
    });
  }

  function numVal(v) {
    const n = parseFloat(v);
    return isNaN(n) ? v : n;
  }

  async function handleCalculate() {
    setSubmitting(true);
    setIsLoading(true);
    setError(null);
    try {
      const payload = {
        ...formData,
        land_prep: {
          ...formData.land_prep,
          custom_diesel_consumption_l: formData.land_prep.custom_diesel_consumption_l === ''
            ? undefined
            : numVal(formData.land_prep.custom_diesel_consumption_l),
        },
      };
      const result = await calculateLca(payload);
      setLcaResult(result);
      navTo(VIEWS.RESULTS);
    } catch (e) {
      setError(e.message || 'Calculation failed. Please try again.');
    } finally {
      setSubmitting(false);
      setIsLoading(false);
    }
  }

  const isLast = step === STEPS.length;

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">New LCA Assessment</h1>
        <p className="text-sm text-slate-400 mt-1">
          Enter farm data to calculate the lifecycle carbon footprint of your tomato crop.
        </p>
      </div>

      {/* Step progress bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          {STEPS.map((s) => {
            const Icon = s.icon;
            const done = step > s.id;
            const active = step === s.id;
            return (
              <button
                key={s.id}
                onClick={() => setStep(s.id)}
                className="flex flex-col items-center gap-1 group"
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-all
                  ${done ? 'bg-emerald-500 text-white' : active ? 'bg-emerald-500/20 border-2 border-emerald-500 text-emerald-400' : 'bg-slate-800 border border-slate-700 text-slate-500'}`}>
                  {done ? <CheckCircle className="w-4 h-4" /> : <Icon className="w-3.5 h-3.5" />}
                </div>
                <span className={`hidden sm:block text-[9px] font-medium transition-colors
                  ${active ? 'text-emerald-400' : done ? 'text-slate-300' : 'text-slate-600'}`}>
                  {s.label}
                </span>
              </button>
            );
          })}
        </div>
        <div className="relative h-1 bg-slate-800 rounded-full mt-1">
          <div
            className="absolute h-1 bg-emerald-500 rounded-full transition-all duration-500"
            style={{ width: `${((step - 1) / (STEPS.length - 1)) * 100}%` }}
          />
        </div>
        <p className="text-xs text-slate-500 mt-2">Step {step} of {STEPS.length} — {STEPS[step - 1].label}</p>
      </div>

      {/* Form card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">

        {/* ─── Step 1: Farm Identity ─── */}
        {step === 1 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div className="sm:col-span-2">
              <Field label="Farm / Grower Name">
                <input className={inputCls} placeholder="e.g. Ravi Kumar Farm" value={formData.farm_name}
                  onChange={e => update('farm_name', e.target.value)} />
              </Field>
            </div>
            <Field label="Taluk">
              <select className={inputCls} value={formData.taluk_id} onChange={e => update('taluk_id', e.target.value)}>
                {TALUKS.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </Field>
            <Field label="Cultivated Area (ha)">
              <input type="number" className={inputCls} min="0.1" step="0.1" value={formData.farm_area_ha}
                onChange={e => update('farm_area_ha', numVal(e.target.value))} />
            </Field>
            <div className="sm:col-span-2">
              <Field label="Tomato Variety">
                <input className={inputCls} placeholder="e.g. Arka Rakshak (ICAR-IIHR)" value={formData.variety_name}
                  onChange={e => update('variety_name', e.target.value)} />
              </Field>
            </div>
          </div>
        )}

        {/* ─── Step 2: Seed & Nursery ─── */}
        {step === 2 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Field label="Seed Rate (g/ha)">
              <input type="number" className={inputCls} value={formData.seed_nursery.seed_rate_g_ha}
                onChange={e => update('seed_nursery.seed_rate_g_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Seedling Count (plants/ha)">
              <input type="number" className={inputCls} value={formData.seed_nursery.seedling_count_ha}
                onChange={e => update('seed_nursery.seedling_count_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Nursery Electricity (kWh/ha)">
              <input type="number" className={inputCls} step="0.1" value={formData.seed_nursery.nursery_electricity_kwh}
                onChange={e => update('seed_nursery.nursery_electricity_kwh', numVal(e.target.value))} />
            </Field>
            <Field label="Nursery → Farm Distance (km)">
              <input type="number" className={inputCls} value={formData.seed_nursery.nursery_to_farm_distance_km}
                onChange={e => update('seed_nursery.nursery_to_farm_distance_km', numVal(e.target.value))} />
            </Field>
          </div>
        )}

        {/* ─── Step 3: Land Preparation ─── */}
        {step === 3 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div className="sm:col-span-2 p-3 bg-slate-800/60 rounded-lg text-xs text-slate-400">
              Leave diesel override blank to auto-calculate from tractor passes.
            </div>
            <Field label="Disc Plough Passes">
              <input type="number" className={inputCls} min="0" value={formData.land_prep.disc_plough_passes}
                onChange={e => update('land_prep.disc_plough_passes', numVal(e.target.value))} />
            </Field>
            <Field label="Cultivator Passes">
              <input type="number" className={inputCls} min="0" value={formData.land_prep.cultivator_passes}
                onChange={e => update('land_prep.cultivator_passes', numVal(e.target.value))} />
            </Field>
            <Field label="Rotavator Passes">
              <input type="number" className={inputCls} min="0" value={formData.land_prep.rotavator_passes}
                onChange={e => update('land_prep.rotavator_passes', numVal(e.target.value))} />
            </Field>
            <Field label="Ridger Passes">
              <input type="number" className={inputCls} min="0" value={formData.land_prep.ridger_passes}
                onChange={e => update('land_prep.ridger_passes', numVal(e.target.value))} />
            </Field>
            <div className="sm:col-span-2">
              <Field label="Diesel Override (L/ha) — optional">
                <input type="number" className={inputCls} placeholder="Auto-calculated if blank"
                  value={formData.land_prep.custom_diesel_consumption_l}
                  onChange={e => update('land_prep.custom_diesel_consumption_l', e.target.value)} />
              </Field>
            </div>
          </div>
        )}

        {/* ─── Step 4: Fertilizers & Pesticides ─── */}
        {step === 4 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Field label="Urea (kg/ha)">
              <input type="number" className={inputCls} value={formData.fertilizer.urea_kg_ha}
                onChange={e => update('fertilizer.urea_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="DAP (kg/ha)">
              <input type="number" className={inputCls} value={formData.fertilizer.dap_kg_ha}
                onChange={e => update('fertilizer.dap_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="MOP (kg/ha)">
              <input type="number" className={inputCls} value={formData.fertilizer.mop_kg_ha}
                onChange={e => update('fertilizer.mop_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="SSP (kg/ha)">
              <input type="number" className={inputCls} value={formData.fertilizer.ssp_kg_ha}
                onChange={e => update('fertilizer.ssp_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Complex 19:19:19 (kg/ha)">
              <input type="number" className={inputCls} value={formData.fertilizer.complex_19_19_19_kg_ha}
                onChange={e => update('fertilizer.complex_19_19_19_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="FYM (tonnes/ha)">
              <input type="number" className={inputCls} step="0.5" value={formData.fertilizer.fym_tonnes_ha}
                onChange={e => update('fertilizer.fym_tonnes_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Pesticide Active Ingredient (kg a.i./ha)">
              <input type="number" className={inputCls} step="0.1" value={formData.fertilizer.pesticides_active_ingredient_kg_ha}
                onChange={e => update('fertilizer.pesticides_active_ingredient_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Knapsack Sprayer Petrol (L/ha)">
              <input type="number" className={inputCls} step="0.5" value={formData.fertilizer.knapsack_sprayer_petrol_l}
                onChange={e => update('fertilizer.knapsack_sprayer_petrol_l', numVal(e.target.value))} />
            </Field>
          </div>
        )}

        {/* ─── Step 5: Irrigation ─── */}
        {step === 5 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Field label="Irrigation System">
              <select className={inputCls} value={formData.irrigation.irrigation_system}
                onChange={e => update('irrigation.irrigation_system', e.target.value)}>
                <option value="furrow_flood">Furrow / Flood</option>
                <option value="drip_fertigation">Drip Fertigation</option>
                <option value="sprinkler">Sprinkler</option>
              </select>
            </Field>
            <Field label="Pump HP">
              <input type="number" className={inputCls} value={formData.irrigation.pump_hp}
                onChange={e => update('irrigation.pump_hp', numVal(e.target.value))} />
            </Field>
            <Field label="Energy Source">
              <select className={inputCls} value={formData.irrigation.energy_source}
                onChange={e => update('irrigation.energy_source', e.target.value)}>
                <option value="grid_electricity">Grid Electricity (KPTCL)</option>
                <option value="solar_pv">Solar PV (PM-KUSUM)</option>
                <option value="diesel_generator">Diesel Generator</option>
              </select>
            </Field>
            <Field label="Total Water Volume (m³/ha)">
              <input type="number" className={inputCls} value={formData.irrigation.total_water_volume_m3_ha}
                onChange={e => update('irrigation.total_water_volume_m3_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Borewell Dynamic Head (m)">
              <input type="number" className={inputCls} value={formData.irrigation.borewell_dynamic_head_m}
                onChange={e => update('irrigation.borewell_dynamic_head_m', numVal(e.target.value))} />
            </Field>
          </div>
        )}

        {/* ─── Step 6: Crop Maintenance ─── */}
        {step === 6 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Field label="Staking Method">
              <select className={inputCls} value={formData.crop_maintenance.staking_method}
                onChange={e => update('crop_maintenance.staking_method', e.target.value)}>
                <option value="bamboo_twine">Bamboo + Twine</option>
                <option value="gms_wire">GMS Wire + Polypropylene</option>
              </select>
            </Field>
            <Field label="Mulching Type">
              <select className={inputCls} value={formData.crop_maintenance.mulching_type}
                onChange={e => update('crop_maintenance.mulching_type', e.target.value)}>
                <option value="polyethylene_silver_black">Polyethylene Silver/Black</option>
                <option value="organic_paddy_straw">Organic Paddy Straw</option>
                <option value="none">None</option>
              </select>
            </Field>
            <div className="sm:col-span-2">
              <Field label="Intercultivation Diesel (L/ha)">
                <input type="number" className={inputCls} step="0.5" value={formData.crop_maintenance.intercultivation_diesel_l}
                  onChange={e => update('crop_maintenance.intercultivation_diesel_l', numVal(e.target.value))} />
              </Field>
            </div>
          </div>
        )}

        {/* ─── Step 7: Harvest ─── */}
        {step === 7 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Field label="Fresh Yield (kg/ha)">
              <input type="number" className={inputCls} value={formData.harvest.fresh_yield_kg_ha}
                onChange={e => update('harvest.fresh_yield_kg_ha', numVal(e.target.value))} />
            </Field>
            <Field label="Post-Harvest Loss (%)">
              <input type="number" className={inputCls} step="0.5" min="0" max="100"
                value={formData.harvest.post_harvest_loss_pct}
                onChange={e => update('harvest.post_harvest_loss_pct', numVal(e.target.value))} />
            </Field>
            <Field label="Packaging Type">
              <select className={inputCls} value={formData.harvest.packaging_type}
                onChange={e => update('harvest.packaging_type', e.target.value)}>
                <option value="reusable_hdpe_crate">Reusable HDPE Crate</option>
                <option value="single_use_wooden_crate">Single-use Wooden Crate</option>
              </select>
            </Field>
            <div className="flex flex-col gap-3">
              <label className={labelCls}>Cold Storage?</label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 accent-emerald-500"
                  checked={formData.harvest.use_cold_storage}
                  onChange={e => update('harvest.use_cold_storage', e.target.checked)} />
                <span className="text-sm text-slate-300">Use cold storage</span>
              </label>
              {formData.harvest.use_cold_storage && (
                <Field label="Cold Storage Days">
                  <input type="number" className={inputCls} min="1" value={formData.harvest.cold_storage_days}
                    onChange={e => update('harvest.cold_storage_days', numVal(e.target.value))} />
                </Field>
              )}
            </div>
          </div>
        )}

        {/* ─── Step 8: Transport ─── */}
        {step === 8 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div className="sm:col-span-2">
              <Field label="Destination Market">
                <input className={inputCls} placeholder="e.g. Antharasanahalli APMC"
                  value={formData.transport.destination_market}
                  onChange={e => update('transport.destination_market', e.target.value)} />
              </Field>
            </div>
            <Field label="Transport Distance (km)">
              <input type="number" className={inputCls} value={formData.transport.transport_distance_km}
                onChange={e => update('transport.transport_distance_km', numVal(e.target.value))} />
            </Field>
            <Field label="Vehicle Type">
              <select className={inputCls} value={formData.transport.vehicle_type}
                onChange={e => update('transport.vehicle_type', e.target.value)}>
                <option value="scv_tata_ace">SCV Tata Ace (&lt;1.5T)</option>
                <option value="mcv_eicher_6wheel">MCV Eicher 6-Wheeler</option>
                <option value="lcv_407">LCV 407</option>
              </select>
            </Field>
            <Field label="Payload (tonnes)">
              <input type="number" className={inputCls} step="0.5" value={formData.transport.payload_tonnes}
                onChange={e => update('transport.payload_tonnes', numVal(e.target.value))} />
            </Field>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-400">
            {error}
          </div>
        )}
      </div>

      {/* Navigation buttons */}
      <div className="flex items-center justify-between mt-6">
        <button
          onClick={() => setStep(s => Math.max(1, s - 1))}
          disabled={step === 1}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-slate-400
            border border-slate-700 hover:text-slate-200 hover:border-slate-600 disabled:opacity-30
            disabled:cursor-not-allowed transition-all"
        >
          <ChevronLeft className="w-4 h-4" />
          Back
        </button>

        <span className="text-xs text-slate-600">{step} / {STEPS.length}</span>

        {isLast ? (
          <button
            onClick={handleCalculate}
            disabled={submitting}
            className="flex items-center gap-2 px-6 py-2 rounded-lg text-sm font-semibold
              bg-emerald-600 hover:bg-emerald-500 text-white disabled:opacity-60
              disabled:cursor-not-allowed transition-all shadow-lg shadow-emerald-900/30"
          >
            {submitting ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Calculating…</>
            ) : (
              <><Leaf className="w-4 h-4" /> Calculate Carbon Footprint</>
            )}
          </button>
        ) : (
          <button
            onClick={() => setStep(s => Math.min(STEPS.length, s + 1))}
            className="flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold
              bg-slate-700 hover:bg-slate-600 text-slate-100 transition-all"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
}
