import React, { useState, useEffect } from 'react';
import {
  FileText, Plus, Filter, Search, CheckCircle2,
  Calendar, MapPin, Truck, Droplets, Sprout, TrendingUp,
  X, Check, AlertCircle, RefreshCw, Layers
} from 'lucide-react';

const API_BASE = '/api/v1';

const DATA_TABS = [
  { id: 'farmer_activities', label: 'Farmer Surveys & Activities', icon: Sprout },
  { id: 'tomato_production', label: 'Taluk Production & Yields', icon: FileText },
  { id: 'fertilizer_inputs', label: 'Fertilizer & Manure Logs', icon: Droplets },
  { id: 'transportation_records', label: 'Mandi Transport Trips', icon: Truck },
  { id: 'tumakuru_soil', label: 'Soil Health Records', icon: MapPin },
  { id: 'market_records', label: 'APMC Market Prices', icon: TrendingUp }
];

export default function FarmRecordsLogbook() {
  const [activeTab, setActiveTab] = useState('farmer_activities');
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [talukFilter, setTalukFilter] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  // New Farmer Record Form State
  const [formData, setFormData] = useState({
    taluk_id: 'tumakuru',
    village: 'Hirehalli',
    farm_id: 'TMK-FARM-101',
    crop_cycle_id: 'CYC-2024-KHA',
    crop_variety: 'Arka Rakshak (IIHR)',
    cultivated_area: 1.0,
    production_quantity: 45000.0,
    planting_date: '2024-06-15',
    harvesting_date: '2024-10-20',
    tractor_diesel_l: 36.0,
    fertilizer_type_qty: 'Urea: 180kg, DAP: 120kg, MOP: 100kg, FYM: 20t',
    irrigation_system: 'Drip Fertigation',
    electricity_kwh: 1250.0,
    packaging_materials: 'Reusable HDPE Crates (25kg)',
    post_harvest_losses_pct: 8.0
  });

  const loadRecords = async (table, taluk = '') => {
    setLoading(true);
    try {
      const url = taluk
        ? `${API_BASE}/sql/records/${table}?taluk_id=${taluk}&limit=50`
        : `${API_BASE}/sql/records/${table}?limit=50`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setRecords(data.records || []);
      }
    } catch (e) {
      console.error('Failed to load farm records', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecords(activeTab, talukFilter);
  }, [activeTab, talukFilter]);

  const handleAddFarmerRecord = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/sql/farmer-activities`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          state_id: 'KA',
          district_id: 'TMK',
          crop_name: 'Tomato (Solanum lycopersicum)',
          farmer_consent_obtained: 1,
          data_collection_date: new Date().toISOString().split('T')[0],
          data_source: 'Primary Farmer Survey - Tumakuru Tomato Cluster',
          data_quality_classification: 'PRIMARY FARMER SURVEY DATA'
        })
      });

      if (res.ok) {
        setShowAddModal(false);
        setSuccessMsg('Farmer activity record successfully logged to Tumakuru database!');
        setTimeout(() => setSuccessMsg(''), 5000);
        loadRecords(activeTab, talukFilter);
      } else {
        const err = await res.json();
        alert(`Error saving record: ${err.detail}`);
      }
    } catch (err) {
      alert(`Save failed: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700/80 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                TUMAKURU AGRICULTURAL LOGBOOK
              </span>
              <span className="text-xs text-slate-400">10 Taluks Covered · Karnataka</span>
            </div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
              <FileText className="w-6 h-6 text-emerald-400" />
              Tumakuru Farmer Activity &amp; Crop Logbook
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Local repository of tomato cultivation records, farmer inputs, fertilizer applications, and mandi transport trips across all 10 taluks of Tumakuru district.
            </p>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-emerald-900/30 transition-all"
            >
              <Plus className="w-4 h-4" />
              <span>Add Farm Survey Record</span>
            </button>
            <button
              onClick={() => loadRecords(activeTab, talukFilter)}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg transition-colors"
              title="Refresh Records"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Tab Selection */}
        <div className="flex flex-wrap gap-2 mt-5 pt-4 border-t border-slate-800">
          {DATA_TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-sm'
                    : 'bg-slate-800/60 text-slate-400 border border-slate-700/60 hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Success alert */}
      {successMsg && (
        <div className="p-3.5 bg-emerald-950/60 border border-emerald-800/60 rounded-xl text-xs text-emerald-300 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>{successMsg}</span>
          </div>
          <button onClick={() => setSuccessMsg('')} className="text-slate-400 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Main Records Viewer */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h2 className="text-sm font-semibold text-white">
              {DATA_TABS.find(t => t.id === activeTab)?.label}
            </h2>
            <p className="text-xs text-slate-400">
              Showing verified entries from Tumakuru district database
            </p>
          </div>

          {/* Taluk Filter Dropdown */}
          <div className="flex items-center gap-2">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={talukFilter}
              onChange={(e) => setTalukFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg text-xs text-white px-3 py-1.5 focus:outline-none focus:border-emerald-500"
            >
              <option value="">All 10 Taluks</option>
              <option value="tumakuru">Tumakuru</option>
              <option value="sira">Sira</option>
              <option value="gubbi">Gubbi</option>
              <option value="kunigal">Kunigal</option>
              <option value="koratagere">Koratagere</option>
              <option value="madhugiri">Madhugiri</option>
              <option value="pavagada">Pavagada</option>
              <option value="tiptur">Tiptur</option>
              <option value="chikkanayakanahalli">Chikkanayakanahalli</option>
              <option value="turuvekere">Turuvekere</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="py-16 text-center text-slate-500 text-xs">
            Loading farm records...
          </div>
        ) : records.length === 0 ? (
          <div className="py-16 text-center text-slate-500 text-xs">
            No records found for the selected taluk.
          </div>
        ) : (
          <div className="overflow-x-auto max-h-[500px] rounded-xl border border-slate-800">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-800/90 text-slate-400 uppercase text-[10px] sticky top-0 backdrop-blur">
                <tr>
                  {Object.keys(records[0])
                    .filter(c => !['record_id', 'state_id', 'district_id', 'village_id', 'crop_name'].includes(c))
                    .map((col) => (
                      <th key={col} className="py-2.5 px-3 whitespace-nowrap">
                        {col.replace(/_/g, ' ')}
                      </th>
                    ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {records.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    {Object.entries(row)
                      .filter(([k]) => !['record_id', 'state_id', 'district_id', 'village_id', 'crop_name'].includes(k))
                      .map(([col, val], j) => (
                        <td key={j} className="py-2.5 px-3 whitespace-nowrap text-[11px] max-w-xs truncate">
                          {col.includes('classification') ? (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                              {String(val)}
                            </span>
                          ) : col.includes('area') || col.includes('yield') || col.includes('quantity') ? (
                            <span className="font-mono text-emerald-300 font-semibold">{String(val)}</span>
                          ) : col.includes('taluk') ? (
                            <span className="font-semibold text-white">{String(val)}</span>
                          ) : (
                            String(val ?? '—')
                          )}
                        </td>
                      ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal: Add Farmer Survey Record */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Plus className="w-5 h-5 text-emerald-400" />
                Record New Farmer Activity Entry (Tumakuru)
              </h3>
              <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <p className="text-xs text-slate-400 mb-5">
              Enter verified field inputs collected from a tomato farmer in Tumakuru district.
            </p>

            <form onSubmit={handleAddFarmerRecord} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Tumakuru Taluk</label>
                  <select
                    value={formData.taluk_id}
                    onChange={(e) => setFormData({ ...formData, taluk_id: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs"
                  >
                    <option value="tumakuru">Tumakuru</option>
                    <option value="sira">Sira</option>
                    <option value="gubbi">Gubbi</option>
                    <option value="kunigal">Kunigal</option>
                    <option value="koratagere">Koratagere</option>
                    <option value="madhugiri">Madhugiri</option>
                    <option value="pavagada">Pavagada</option>
                    <option value="tiptur">Tiptur</option>
                    <option value="chikkanayakanahalli">Chikkanayakanahalli</option>
                    <option value="turuvekere">Turuvekere</option>
                  </select>
                </div>

                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Village Name</label>
                  <input
                    type="text"
                    value={formData.village}
                    onChange={(e) => setFormData({ ...formData, village: e.target.value })}
                    placeholder="e.g. Hirehalli, Chelur, Bukkapatna"
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Cultivated Area (Hectares)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.cultivated_area}
                    onChange={(e) => setFormData({ ...formData, cultivated_area: parseFloat(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs font-mono"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Gross Harvest Yield (kg)</label>
                  <input
                    type="number"
                    value={formData.production_quantity}
                    onChange={(e) => setFormData({ ...formData, production_quantity: parseFloat(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs font-mono"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Tomato Variety</label>
                  <input
                    type="text"
                    value={formData.crop_variety}
                    onChange={(e) => setFormData({ ...formData, crop_variety: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Irrigation System</label>
                  <select
                    value={formData.irrigation_system}
                    onChange={(e) => setFormData({ ...formData, irrigation_system: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs"
                  >
                    <option value="Drip Fertigation">Drip Fertigation (Water-saving)</option>
                    <option value="Furrow Flood">Furrow Flood (Traditional)</option>
                  </select>
                </div>

                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Tractor Diesel Used (Liters)</label>
                  <input
                    type="number"
                    value={formData.tractor_diesel_l}
                    onChange={(e) => setFormData({ ...formData, tractor_diesel_l: parseFloat(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs font-mono"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Fertilizer Inputs Used</label>
                  <input
                    type="text"
                    value={formData.fertilizer_type_qty}
                    onChange={(e) => setFormData({ ...formData, fertilizer_type_qty: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs"
                    placeholder="Urea, DAP, MOP, FYM quantities"
                  />
                </div>

                <div>
                  <label className="text-slate-300 block mb-1 font-medium">Packaging Material</label>
                  <select
                    value={formData.packaging_materials}
                    onChange={(e) => setFormData({ ...formData, packaging_materials: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white text-xs"
                  >
                    <option value="Reusable HDPE Crates (25kg)">Reusable Plastic HDPE Crates (25kg)</option>
                    <option value="Wooden Boxes (single-use)">Wooden Boxes (single-use)</option>
                    <option value="Corrugated Cartons">Corrugated Paper Cartons</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg text-xs shadow-md shadow-emerald-900/30"
                >
                  Save Entry
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
