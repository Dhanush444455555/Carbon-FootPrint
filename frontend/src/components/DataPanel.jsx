import React, { useState, useEffect } from 'react';
import {
  Database, ShieldCheck, AlertTriangle, CheckCircle2,
  FileSpreadsheet, HelpCircle, ArrowUpRight, Search,
  Filter, Layers, MapPin, Building2, Calendar, FileText
} from 'lucide-react';
import { fetchDataCoverage, fetchDataSources, fetchTaluks, fetchEmissionFactors } from '../services/api';

export default function DataPanel() {
  const [coverage, setCoverage] = useState(null);
  const [sources, setSources] = useState(null);
  const [taluks, setTaluks] = useState([]);
  const [emissionFactors, setEmissionFactors] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [talukSearch, setTalukSearch] = useState('');

  useEffect(() => {
    Promise.all([
      fetchDataCoverage().catch(() => null),
      fetchDataSources().catch(() => null),
      fetchTaluks().catch(() => null),
      fetchEmissionFactors().catch(() => null)
    ]).then(([cov, src, tal, ef]) => {
      setCoverage(cov);
      setSources(src);
      if (tal?.taluks) setTaluks(tal.taluks);
      if (ef?.emission_factors) setEmissionFactors(ef.emission_factors);
      setLoading(false);
    });
  }, []);

  const filteredTaluks = taluks.filter(t =>
    t.name.toLowerCase().includes(talukSearch.toLowerCase()) ||
    t.soil_type.toLowerCase().includes(talukSearch.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700/80 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                SECTION 6 COMPLIANCE
              </span>
              <span className="text-xs text-slate-400">Strict District Boundary: Tumakuru, Karnataka</span>
            </div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
              <Database className="w-6 h-6 text-emerald-400" />
              Tumakuru Data Intelligence
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Transparent repository of agricultural activity, weather, soil, market logistics, and scientific emission factor ledgers.
              Strictly partitioned by empirical hierarchy with zero silent proxy blending.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="px-3.5 py-2 rounded-xl bg-slate-800/80 border border-slate-700 text-right">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Validation Boundary</span>
              <p className="text-sm font-bold text-emerald-400">Tumakuru (10 Taluks)</p>
            </div>
          </div>
        </div>

        {/* 5-Category Hierarchy Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5 mt-6 pt-5 border-t border-slate-800">
          <div className="bg-emerald-950/40 border border-emerald-800/50 rounded-xl p-3">
            <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">
              1. MEASURED DATA
            </span>
            <p className="text-sm font-semibold text-white mt-1">IMD Station No. 43291</p>
            <span className="text-[10px] text-slate-400">Verified ground observations</span>
          </div>

          <div className="bg-blue-950/40 border border-blue-800/50 rounded-xl p-3">
            <span className="text-[10px] font-bold text-blue-400 uppercase tracking-wider block">
              2. OFFICIALLY REPORTED
            </span>
            <p className="text-sm font-semibold text-white mt-1">KDA & CEA Baseline v21</p>
            <span className="text-[10px] text-slate-400">Govt statistical yearbooks</span>
          </div>

          <div className="bg-amber-950/40 border border-amber-800/50 rounded-xl p-3">
            <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">
              3. PRIMARY FARMER SURVEY
            </span>
            <p className="text-sm font-semibold text-amber-300 mt-1">Pending Field Work</p>
            <span className="text-[10px] text-slate-400">Farmer consent + harvest audit</span>
          </div>

          <div className="bg-purple-950/40 border border-purple-800/50 rounded-xl p-3">
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wider block">
              4. SCIENTIFIC EF
            </span>
            <p className="text-sm font-semibold text-white mt-1">IPCC 2019 / ecoinvent</p>
            <span className="text-[10px] text-slate-400">N₂O & chemical stoichiometry</span>
          </div>

          <div className="bg-rose-950/40 border border-rose-800/50 rounded-xl p-3">
            <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider block">
              5. MODELLED / ESTIMATED
            </span>
            <p className="text-sm font-semibold text-rose-300 mt-1">Clearly Tagged</p>
            <span className="text-[10px] text-slate-400">Hydrogeological & GIS proxies</span>
          </div>
        </div>
      </div>

      {/* Dataset Statistics Counters */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Taluks Covered</span>
          <p className="text-xl font-bold text-emerald-400 font-mono mt-1">10 / 10</p>
          <span className="text-[10px] text-slate-500">100% Tumakuru</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Villages Mapped</span>
          <p className="text-xl font-bold text-white font-mono mt-1">54</p>
          <span className="text-[10px] text-slate-500">In 10 taluks</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Verified Farms</span>
          <p className="text-xl font-bold text-amber-400 font-mono mt-1">3</p>
          <span className="text-[10px] text-slate-500">Archetypes (Survey pending)</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Production Stats</span>
          <p className="text-xl font-bold text-blue-400 font-mono mt-1">10 Records</p>
          <span className="text-[10px] text-slate-500">KDA Season Report 22-23</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Weather Normals</span>
          <p className="text-xl font-bold text-cyan-400 font-mono mt-1">12 Months</p>
          <span className="text-[10px] text-slate-500">IMD Tumakuru Station</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Soil Records</span>
          <p className="text-xl font-bold text-purple-400 font-mono mt-1">10 Taluk Series</p>
          <span className="text-[10px] text-slate-500">KSRSAC / NBSS&LUP</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Transport Routes</span>
          <p className="text-xl font-bold text-yellow-400 font-mono mt-1">14 Mandi Links</p>
          <span className="text-[10px] text-slate-500">APMC Antharasanahalli</span>
        </div>
      </div>

      {/* Critical Geographic Validation Banner */}
      <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-5">
        <div className="flex items-start gap-3">
          <ShieldCheck className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div className="flex-1">
            <h3 className="text-sm font-bold text-white">Geographical Filter Rules (Strict Enforcement)</h3>
            <p className="text-xs text-slate-300 mt-1">
              Every agricultural activity and input record must pass mandatory validation against the official Karnataka Revenue Department administrative hierarchy:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mt-3 text-xs">
              <div className="bg-slate-800/70 p-2.5 rounded-lg border border-slate-700">
                <span className="text-slate-400 block text-[10px]">State Boundary</span>
                <span className="font-semibold text-white">Karnataka (state_id: KA)</span>
              </div>
              <div className="bg-slate-800/70 p-2.5 rounded-lg border border-slate-700">
                <span className="text-slate-400 block text-[10px]">District Boundary</span>
                <span className="font-semibold text-white">Tumakuru (district_id: TMK)</span>
              </div>
              <div className="bg-slate-800/70 p-2.5 rounded-lg border border-slate-700">
                <span className="text-slate-400 block text-[10px]">Target Crop</span>
                <span className="font-semibold text-white">Tomato (Solanum lycopersicum)</span>
              </div>
              <div className="bg-slate-800/70 p-2.5 rounded-lg border border-red-900/40">
                <span className="text-slate-400 block text-[10px]">Rejected Out-of-Scope</span>
                <span className="font-semibold text-red-400">Bengaluru, Chitradurga, Hassan</span>
              </div>
            </div>
            <p className="text-[11px] text-slate-400 mt-2 italic">
              Mandatory schema attributes retained: <code className="text-emerald-400">state_id</code>, <code className="text-emerald-400">district_id</code>, <code className="text-emerald-400">taluk_id</code>, <code className="text-emerald-400">village_id</code>, <code className="text-emerald-400">farm_id</code>, <code className="text-emerald-400">crop_cycle_id</code>.
            </p>
          </div>
        </div>
      </div>

      {/* Taluk-Wise Administrative & Soil Breakdown */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <MapPin className="w-5 h-5 text-emerald-400" />
              Tumakuru Taluk Inventory & Baseline Hydrogeological Ledger
            </h2>
            <p className="text-xs text-slate-400">All 10 official taluks in Tumakuru district with soil series, groundwater depth, and tomato coverage</p>
          </div>
          <div className="relative w-64">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search taluk or soil..."
              value={talukSearch}
              onChange={(e) => setTalukSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-800/60 text-slate-400 uppercase tracking-wider text-[10px]">
              <tr>
                <th className="py-2.5 px-3 rounded-l">Taluk Name</th>
                <th className="py-2.5 px-3">Soil Type (KSRSAC)</th>
                <th className="py-2.5 px-3">Groundwater Depth (m bgl)</th>
                <th className="py-2.5 px-3">Dist. to APMC Tumakuru</th>
                <th className="py-2.5 px-3">Tomato Area (Ha)</th>
                <th className="py-2.5 px-3">Avg Yield (T/Ha)</th>
                <th className="py-2.5 px-3 rounded-r">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredTaluks.map((t) => (
                <tr key={t.id} className="hover:bg-slate-800/40">
                  <td className="py-2.5 px-3 font-semibold text-white flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-400" />
                    {t.name}
                  </td>
                  <td className="py-2.5 px-3 text-slate-300">{t.soil_type}</td>
                  <td className="py-2.5 px-3 font-mono text-cyan-300">{t.groundwater_depth_m_bgl} m</td>
                  <td className="py-2.5 px-3 font-mono text-yellow-300">{t.distance_to_apmc_tumakuru_km} km</td>
                  <td className="py-2.5 px-3 font-mono text-blue-300">{t.average_tomato_area_ha?.toLocaleString()} ha</td>
                  <td className="py-2.5 px-3 font-mono text-emerald-400">{t.typical_yield_t_ha} t/ha</td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-950/60 text-emerald-400 border border-emerald-800/40">
                      Validated
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Scientific Emission Factor Provenance Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <FileSpreadsheet className="w-5 h-5 text-purple-400" />
              Scientific Emission Factors & Calculation Ledger
            </h2>
            <p className="text-xs text-slate-400">Strictly documented conversion constants used in cradle-to-market LCA</p>
          </div>
          <span className="text-[11px] text-purple-400 bg-purple-950/60 border border-purple-800/40 px-2.5 py-1 rounded-full">
            ISO 14040/14044 & IPCC 2019
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {emissionFactors && Object.entries(emissionFactors).map(([key, item]) => (
            <div key={key} className="bg-slate-800/40 border border-slate-800 rounded-xl p-3.5 hover:border-slate-700 transition-colors">
              <div className="flex items-start justify-between gap-2 mb-1">
                <span className="text-xs font-semibold text-white capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
                <span className="text-[10px] text-purple-400 bg-purple-950/50 px-1.5 py-0.5 rounded shrink-0 font-mono">
                  {item.value} {item.unit}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">
                <strong>Source:</strong> {item.source}
              </p>
              {item.uncertainty_pct && (
                <span className="text-[10px] text-slate-500 mt-2 block">
                  Uncertainty: ±{item.uncertainty_pct}%
                </span>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Missing Datasets & Improvement Roadmap */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Missing Dataset Audit & Field Survey Roadmap
        </h2>
        <p className="text-xs text-slate-400 mb-4">
          In compliance with Section 6, the following data categories are explicitly identified as missing or awaiting primary field collection:
        </p>

        <div className="space-y-3">
          {coverage?.missing_datasets?.map((item, idx) => (
            <div key={idx} className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    item.priority === 'HIGH' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                    item.priority === 'MEDIUM' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                    'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  }`}>
                    {item.priority} PRIORITY
                  </span>
                  <span className="text-sm font-bold text-white">{item.category}</span>
                </div>
                <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{item.description}</p>
                <div className="mt-2 text-xs text-slate-300">
                  <strong className="text-slate-400">Action Plan:</strong> {item.action}
                </div>
              </div>
              <div className="shrink-0 text-left sm:text-right">
                <span className="text-[10px] text-slate-500 block">Affects Subsystems:</span>
                <div className="flex flex-wrap sm:justify-end gap-1 mt-1">
                  {item.affects?.map((aff, i) => (
                    <span key={i} className="text-[10px] bg-slate-700/60 text-slate-300 px-2 py-0.5 rounded">
                      {aff}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )) || (
            <p className="text-xs text-slate-400">Loading missing dataset inventory...</p>
          )}
        </div>
      </div>
    </div>
  );
}
