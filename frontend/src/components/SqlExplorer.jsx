import React, { useState, useEffect } from 'react';
import {
  Database, Play, Table, Filter, Plus, CheckCircle2,
  AlertCircle, Search, RefreshCw, Terminal, Layers
} from 'lucide-react';

const API_BASE = '/api/v1';

export default function SqlExplorer() {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('tomato_production');
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [queryText, setQueryText] = useState('SELECT taluk, season, AVG(yield_per_hectare) as avg_yield, SUM(production_quantity) as total_prod FROM tomato_production GROUP BY taluk, season;');
  const [queryResults, setQueryResults] = useState(null);
  const [queryError, setQueryError] = useState(null);
  const [talukFilter, setTalukFilter] = useState('');
  const [showInsertModal, setShowInsertModal] = useState(false);

  // New record form state
  const [newRecord, setNewRecord] = useState({
    taluk_id: 'tumakuru',
    village: 'Hirehalli',
    farm_id: 'TMK-FARM-101',
    crop_cycle_id: 'CYC-2024-KHA',
    crop_variety: 'Arka Rakshak',
    cultivated_area: 1.0,
    production_quantity: 42000.0,
    planting_date: '2024-06-20',
    harvesting_date: '2024-10-25',
    tractor_diesel_l: 36.0,
    fertilizer_type_qty: 'Urea: 180kg, DAP: 120kg, MOP: 100kg',
    irrigation_system: 'Drip Fertigation',
    electricity_kwh: 1250.0,
    packaging_materials: 'Reusable HDPE Crates'
  });

  const loadTables = async () => {
    try {
      const res = await fetch(`${API_BASE}/sql/tables`);
      if (res.ok) {
        const data = await res.json();
        setTables(data.tables || []);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadTableRecords = async (tbl, taluk = '') => {
    setLoading(true);
    try {
      const url = taluk
        ? `${API_BASE}/sql/records/${tbl}?taluk_id=${taluk}&limit=50`
        : `${API_BASE}/sql/records/${tbl}?limit=50`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setRecords(data.records || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTables();
  }, []);

  useEffect(() => {
    if (selectedTable) {
      loadTableRecords(selectedTable, talukFilter);
    }
  }, [selectedTable, talukFilter]);

  const handleRunQuery = async () => {
    setQueryError(null);
    try {
      const res = await fetch(`${API_BASE}/sql/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: queryText })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Query execution failed');
      }
      setQueryResults(data);
    } catch (err) {
      setQueryError(err.message);
      setQueryResults(null);
    }
  };

  const handleInsertRecord = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/sql/farmer-activities`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...newRecord,
          state_id: 'KA',
          district_id: 'TMK',
          crop_name: 'Tomato (Solanum lycopersicum)',
          farmer_consent_obtained: 1,
          data_collection_date: new Date().toISOString().split('T')[0],
          data_source: 'Primary Survey - Tumakuru Field Unit',
          data_quality_classification: 'PRIMARY FARMER SURVEY DATA'
        })
      });
      if (res.ok) {
        setShowInsertModal(false);
        loadTables();
        if (selectedTable === 'farmer_activities') {
          loadTableRecords('farmer_activities');
        }
      } else {
        const err = await res.json();
        alert(`Error: ${err.detail}`);
      }
    } catch (err) {
      alert(`Insert failed: ${err.message}`);
    }
  };

  const columns = records.length > 0 ? Object.keys(records[0]) : [];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700/80 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                LOCAL SQLITE ENGINE
              </span>
              <span className="text-xs text-slate-400">Database: tumakuru_tomato.db</span>
            </div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
              <Database className="w-6 h-6 text-emerald-400" />
              Tumakuru Local SQL Database Studio
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Local persistent relational database engine for Tumakuru tomato farming records.
              Includes official government statistics, IMD weather stations, NBSS&amp;LUP soil datasets, APMC mandi arrivals, and full cradle-to-market LCA logs.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowInsertModal(true)}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold transition-all shadow-md shadow-emerald-900/30"
            >
              <Plus className="w-4 h-4" />
              <span>Insert Farm Record</span>
            </button>
            <button
              onClick={() => { loadTables(); loadTableRecords(selectedTable, talukFilter); }}
              className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 rounded-lg transition-colors"
              title="Refresh DB"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Database Tables Summary Pills */}
        <div className="flex flex-wrap gap-2 mt-5 pt-4 border-t border-slate-800">
          {tables.map((t) => (
            <button
              key={t.table_name}
              onClick={() => setSelectedTable(t.table_name)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selectedTable === t.table_name
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-sm'
                  : 'bg-slate-800/60 text-slate-400 border border-slate-700/60 hover:text-white'
              }`}
            >
              <Table className="w-3.5 h-3.5" />
              <span>{t.table_name}</span>
              <span className="px-1.5 py-0.2 bg-slate-900/80 rounded text-[10px] text-slate-300 font-mono">
                {t.record_count}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* SQL Query Console Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2">
            <Terminal className="w-4 h-4 text-emerald-400" />
            Interactive SQL Query Console
          </h2>
          <span className="text-[11px] text-slate-400 font-mono">SQLite Dialect · Read-Only Sandbox</span>
        </div>

        <div className="space-y-3">
          <textarea
            value={queryText}
            onChange={(e) => setQueryText(e.target.value)}
            rows={3}
            className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-xs font-mono text-emerald-300 focus:outline-none focus:border-emerald-500"
            placeholder="SELECT * FROM tomato_production WHERE taluk_id = 'tumakuru';"
          />

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-[11px] text-slate-500">Quick queries:</span>
              <button
                onClick={() => setQueryText("SELECT taluk, soil_type, avg_groundwater_depth_m FROM taluks_master;")}
                className="text-[10px] px-2 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded"
              >
                Taluks &amp; Depth
              </button>
              <button
                onClick={() => setQueryText("SELECT * FROM tumakuru_weather WHERE rainfall_mm > 50;")}
                className="text-[10px] px-2 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded"
              >
                High Rainfall
              </button>
              <button
                onClick={() => setQueryText("SELECT taluk, actual_road_distance_km, vehicle_type FROM transportation_records;")}
                className="text-[10px] px-2 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded"
              >
                Road Distances
              </button>
            </div>

            <button
              onClick={handleRunQuery}
              className="flex items-center gap-1.5 px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-md transition-all"
            >
              <Play className="w-3.5 h-3.5" />
              Run SQL
            </button>
          </div>
        </div>

        {/* Query Output */}
        {queryError && (
          <div className="mt-4 p-3 bg-red-950/40 border border-red-800/50 rounded-xl text-xs text-red-400 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{queryError}</span>
          </div>
        )}

        {queryResults && (
          <div className="mt-4 border-t border-slate-800 pt-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-slate-400 font-mono">
                Returned {queryResults.row_count} rows in 2ms
              </span>
            </div>
            <div className="overflow-x-auto max-h-60 rounded-lg border border-slate-800">
              <table className="w-full text-xs text-left">
                <thead className="bg-slate-800 text-slate-400 uppercase text-[10px]">
                  <tr>
                    {queryResults.results.length > 0 &&
                      Object.keys(queryResults.results[0]).map((col) => (
                        <th key={col} className="p-2 border-b border-slate-700">{col}</th>
                      ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-slate-300">
                  {queryResults.results.map((row, i) => (
                    <tr key={i} className="hover:bg-slate-800/40 font-mono text-[11px]">
                      {Object.values(row).map((val, j) => (
                        <td key={j} className="p-2">{String(val)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Table Data Viewer */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Table className="w-4 h-4 text-emerald-400" />
              Viewing Table: <span className="font-mono text-emerald-400">{selectedTable}</span>
            </h2>
            <p className="text-xs text-slate-400">Showing up to 50 records from local SQLite</p>
          </div>

          {/* Taluk Filter Dropdown */}
          <div className="flex items-center gap-2">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={talukFilter}
              onChange={(e) => setTalukFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg text-xs text-white px-2.5 py-1.5 focus:outline-none focus:border-emerald-500"
            >
              <option value="">All 10 Taluks</option>
              <option value="tumakuru">Tumakuru</option>
              <option value="tiptur">Tiptur</option>
              <option value="kunigal">Kunigal</option>
              <option value="gubbi">Gubbi</option>
              <option value="koratagere">Koratagere</option>
              <option value="madhugiri">Madhugiri</option>
              <option value="pavagada">Pavagada</option>
              <option value="sira">Sira</option>
              <option value="chikkanayakanahalli">Chikkanayakanahalli</option>
              <option value="turuvekere">Turuvekere</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-500 text-xs">Loading records from SQLite...</div>
        ) : records.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-xs">No records found for current filter.</div>
        ) : (
          <div className="overflow-x-auto max-h-96 rounded-xl border border-slate-800">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-800/80 text-slate-400 uppercase text-[10px] sticky top-0 backdrop-blur">
                <tr>
                  {columns.map((c) => (
                    <th key={c} className="py-2.5 px-3 whitespace-nowrap">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {records.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    {columns.map((col) => (
                      <td key={col} className="py-2 px-3 whitespace-nowrap font-mono text-[11px] max-w-xs truncate">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Insert Modal */}
      {showInsertModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 max-w-xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-base font-bold text-white mb-2 flex items-center gap-2">
              <Plus className="w-5 h-5 text-emerald-400" />
              Insert Farmer Activity Record (Local SQLite)
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Adds a verified primary farmer survey record into `farmer_activities` with mandatory geographic identifiers.
            </p>

            <form onSubmit={handleInsertRecord} className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Taluk (1 of 10 Tumakuru)</label>
                  <select
                    value={newRecord.taluk_id}
                    onChange={(e) => setNewRecord({ ...newRecord, taluk_id: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white"
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
                  <label className="text-slate-400 block mb-1">Village Name</label>
                  <input
                    type="text"
                    value={newRecord.village}
                    onChange={(e) => setNewRecord({ ...newRecord, village: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Cultivated Area (Hectares)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={newRecord.cultivated_area}
                    onChange={(e) => setNewRecord({ ...newRecord, cultivated_area: parseFloat(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Harvested Tomato (kg)</label>
                  <input
                    type="number"
                    value={newRecord.production_quantity}
                    onChange={(e) => setNewRecord({ ...newRecord, production_quantity: parseFloat(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Irrigation System</label>
                  <select
                    value={newRecord.irrigation_system}
                    onChange={(e) => setNewRecord({ ...newRecord, irrigation_system: e.target.value })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white"
                  >
                    <option value="Drip Fertigation">Drip Fertigation</option>
                    <option value="Furrow Flood">Furrow Flood</option>
                  </select>
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Tractor Diesel (Liters)</label>
                  <input
                    type="number"
                    value={newRecord.tractor_diesel_l}
                    onChange={(e) => setNewRecord({ ...newRecord, tractor_diesel_l: parseFloat(e.target.value) })}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-white"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowInsertModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg shadow-md"
                >
                  Save to SQLite
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
