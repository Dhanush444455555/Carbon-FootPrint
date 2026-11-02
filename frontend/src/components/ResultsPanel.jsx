import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell
} from 'recharts';
import {
  Leaf, AlertTriangle, Download, TrendingDown, TrendingUp,
  CheckCircle, MapPin, ArrowRight, Loader2, Target
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { exportCsvReport } from '../services/api';

const STAGE_COLORS = [
  '#06b6d4', '#3b82f6', '#f59e0b', '#10b981',
  '#8b5cf6', '#ec4899', '#ef4444'
];

function footprintColor(val) {
  if (val <= 0.08) return { text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', label: 'Low Carbon', icon: CheckCircle };
  if (val <= 0.15) return { text: 'text-amber-400',   bg: 'bg-amber-500/10',   border: 'border-amber-500/30',   label: 'Moderate',   icon: AlertTriangle };
  return { text: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', label: 'High Carbon', icon: AlertTriangle };
}

function pctColor(pct) {
  if (pct >= 35) return 'bg-red-500';
  if (pct >= 20) return 'bg-amber-500';
  if (pct >= 10) return 'bg-blue-500';
  return 'bg-emerald-500';
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs shadow-xl">
      <p className="text-slate-300 font-semibold mb-1">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.fill || p.stroke }}>
          {p.name}: {typeof p.value === 'number' ? p.value.toFixed(2) : p.value} kg CO₂e
        </p>
      ))}
    </div>
  );
};

export default function ResultsPanel() {
  const { lcaResult, navTo, VIEWS } = useApp();
  const [exporting, setExporting] = useState(false);
  const [exportError, setExportError] = useState(null);

  if (!lcaResult) {
    return (
      <div className="flex flex-col items-center justify-center h-80 gap-4 text-slate-500">
        <Leaf className="w-12 h-12 opacity-30" />
        <p className="text-sm">No LCA results yet.</p>
        <button
          onClick={() => navTo(VIEWS.INPUT)}
          className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500
            text-white rounded-lg text-sm font-medium transition-colors"
        >
          Start New Assessment <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  const { summary, stage_breakdown = [], hotspot, recommendations = [], benchmarks = [], inefficiencies_flagged = [], meta } = lcaResult;
  const fp = summary.footprint_kg_co2e_per_kg_marketable;
  const statusInfo = footprintColor(fp);
  const StatusIcon = statusInfo.icon;

  const chartData = stage_breakdown.map((s, i) => ({
    name: s.stage_name.replace(/Stage \d+: /, ''),
    emissions: s.emissions_kg_co2e,
    pct: s.percentage_of_total,
    color: STAGE_COLORS[i % STAGE_COLORS.length],
  }));

  async function handleExport() {
    setExporting(true);
    setExportError(null);
    try {
      const csv = await exportCsvReport(lcaResult);
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `tomato-carbontrace-lca-${Date.now()}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      // Fallback: build CSV locally
      const rows = [
        ['Stage', 'Emissions (kg CO2e)', '% of Total', 'Primary Driver'],
        ...stage_breakdown.map(s => [
          s.stage_name, s.emissions_kg_co2e, s.percentage_of_total, s.primary_driver
        ]),
        [],
        ['Total Emissions (kg CO2e)', summary.total_cycle_emissions_kg_co2e],
        ['Carbon Footprint (kg CO2e/kg)', fp],
        ['Marketable Yield (kg)', summary.marketable_yield_kg],
      ];
      const csv = rows.map(r => r.join(',')).join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `tomato-carbontrace-lca-${Date.now()}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } finally {
      setExporting(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">LCA Results</h1>
          <p className="text-sm text-slate-400 mt-0.5">
            Full lifecycle carbon footprint · ISO 14040/44 · IPCC 2019
          </p>
        </div>
        <button
          onClick={handleExport}
          disabled={exporting}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700
            border border-slate-700 text-slate-300 rounded-lg text-sm font-medium
            transition-colors disabled:opacity-50"
        >
          {exporting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
          Export CSV
        </button>
      </div>

      {/* ── Hero card ── */}
      <div className={`rounded-xl border p-6 ${statusInfo.bg} ${statusInfo.border}`}>
        <div className="flex flex-col sm:flex-row sm:items-center gap-4">
          <div className="flex-1">
            <p className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-1">
              Carbon Footprint
            </p>
            <div className="flex items-end gap-3">
              <span className={`text-5xl font-black ${statusInfo.text}`}>
                {fp.toFixed(4)}
              </span>
              <span className="text-slate-400 text-sm pb-1">kg CO₂e / kg tomato</span>
            </div>
            <div className={`inline-flex items-center gap-1.5 mt-3 px-2.5 py-1 rounded-full text-xs font-semibold ${statusInfo.bg} ${statusInfo.text} border ${statusInfo.border}`}>
              <StatusIcon className="w-3 h-3" />
              {statusInfo.label}
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-1 gap-3 sm:text-right">
            <div>
              <p className="text-xs text-slate-500">Total Emissions</p>
              <p className="text-lg font-bold text-slate-200">
                {summary.total_cycle_emissions_kg_co2e.toLocaleString()} <span className="text-xs font-normal text-slate-500">kg CO₂e</span>
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Marketable Yield</p>
              <p className="text-lg font-bold text-slate-200">
                {summary.marketable_yield_kg.toLocaleString()} <span className="text-xs font-normal text-slate-500">kg</span>
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Area</p>
              <p className="text-lg font-bold text-slate-200">
                {meta?.crop?.cultivated_area_ha ?? '—'} <span className="text-xs font-normal text-slate-500">ha</span>
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Potential Savings</p>
              <p className="text-lg font-bold text-emerald-400">
                {summary.potential_carbon_reduction_pct}% <span className="text-xs font-normal text-slate-500">reduction possible</span>
              </p>
            </div>
          </div>
        </div>

        {/* Geographic badge */}
        {meta?.location && (
          <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-500">
            <span className="flex items-center gap-1 bg-slate-800/50 px-2 py-0.5 rounded-full">
              <MapPin className="w-3 h-3" /> {meta.location.district}, {meta.location.state}
            </span>
            <span className="bg-slate-800/50 px-2 py-0.5 rounded-full">{meta.crop?.variety_name}</span>
            <span className="bg-slate-800/50 px-2 py-0.5 rounded-full">ISO 14040/44 · IPCC 2019</span>
          </div>
        )}
      </div>

      {/* ── Stage breakdown bar chart ── */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-sm font-bold text-slate-200 mb-4">Emission by Lifecycle Stage (kg CO₂e)</h2>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 8, right: 24, top: 4, bottom: 4 }}>
            <XAxis type="number" tick={{ fontSize: 11, fill: '#64748b' }} tickLine={false} axisLine={false} />
            <YAxis type="category" dataKey="name" width={160} tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="emissions" radius={[0, 4, 4, 0]} name="Emissions">
              {chartData.map((entry, i) => (
                <Cell key={i} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ── Stage cards ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {stage_breakdown.map((s, i) => (
          <div key={s.stage_id} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="flex items-start justify-between mb-2">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                {s.stage_name.replace(/Stage \d+: /, '')}
              </span>
              <span
                className="text-xs font-bold px-1.5 py-0.5 rounded text-white"
                style={{ background: STAGE_COLORS[i % STAGE_COLORS.length] }}
              >
                {s.percentage_of_total}%
              </span>
            </div>
            <p className="text-xl font-black text-slate-100">
              {s.emissions_kg_co2e.toLocaleString()}
              <span className="text-xs font-normal text-slate-500 ml-1">kg CO₂e</span>
            </p>
            <div className="mt-2 h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full"
                style={{
                  width: `${s.percentage_of_total}%`,
                  background: STAGE_COLORS[i % STAGE_COLORS.length]
                }}
              />
            </div>
            <p className="text-xs text-slate-500 mt-2 leading-snug line-clamp-2">{s.primary_driver}</p>
          </div>
        ))}
      </div>

      {/* ── Hotspot Analysis ── */}
      {hotspot && (
        <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <h2 className="text-sm font-bold text-slate-200">Hotspot Analysis</h2>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <div className="flex-1">
              <p className="text-xs text-slate-500 mb-0.5">Largest Emission Source</p>
              <p className="text-base font-bold text-red-400">{hotspot.top_stage_name}</p>
              <p className="text-xs text-slate-400 mt-1 leading-snug">{hotspot.primary_cause}</p>
            </div>
            <div className="text-right shrink-0">
              <p className="text-3xl font-black text-red-400">{hotspot.percentage_of_total}%</p>
              <p className="text-xs text-slate-500">of total</p>
              <p className="text-xs text-emerald-400 mt-1">
                <TrendingDown className="w-3 h-3 inline mr-0.5" />
                {hotspot.mitigation_potential_kg_co2e} kg CO₂e saveable
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ── Benchmark comparison ── */}
      {benchmarks.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-bold text-slate-200 mb-4">Benchmark Comparison</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left pb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Benchmark</th>
                  <th className="text-right pb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">kg CO₂e/kg</th>
                  <th className="text-right pb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">vs Your Farm</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {/* Your farm row */}
                <tr className="bg-emerald-500/5">
                  <td className="py-3 text-slate-200 font-semibold">Your Farm</td>
                  <td className="py-3 text-right font-mono text-emerald-400 font-bold">{fp.toFixed(4)}</td>
                  <td className="py-3 text-right text-slate-500">—</td>
                </tr>
                {benchmarks.map((b, i) => {
                  const diff = b.difference_percentage;
                  const better = diff < 0;
                  return (
                    <tr key={i}>
                      <td className="py-3 text-slate-300">{b.benchmark_name}</td>
                      <td className="py-3 text-right font-mono text-slate-400">{b.carbon_footprint_kg_co2e_per_kg.toFixed(4)}</td>
                      <td className="py-3 text-right">
                        <span className={`inline-flex items-center gap-0.5 text-xs font-semibold
                          ${better ? 'text-emerald-400' : 'text-red-400'}`}>
                          {better ? <TrendingDown className="w-3 h-3" /> : <TrendingUp className="w-3 h-3" />}
                          {Math.abs(diff).toFixed(1)}%
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Inefficiencies ── */}
      {inefficiencies_flagged.length > 0 && (
        <div className="bg-slate-900 border border-amber-500/20 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <h2 className="text-sm font-bold text-slate-200">Inefficiencies Flagged</h2>
          </div>
          <div className="space-y-3">
            {inefficiencies_flagged.map((item, i) => (
              <div key={i} className="flex items-start gap-3 p-3 bg-amber-500/5 border border-amber-500/20 rounded-lg">
                <span className={`text-xs font-bold px-1.5 py-0.5 rounded mt-0.5 shrink-0
                  ${item.severity === 'CRITICAL' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'}`}>
                  {item.severity}
                </span>
                <div>
                  <p className="text-sm font-semibold text-slate-200">{item.title}</p>
                  <p className="text-xs text-slate-400 mt-0.5 leading-snug">{item.detail}</p>
                  <p className="text-xs text-red-400 mt-1">
                    Carbon penalty: +{item.carbon_penalty_kg_co2e} kg CO₂e
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Recommendations ── */}
      {recommendations.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm font-bold text-slate-200">Recommendations</h2>
          </div>
          <div className="grid grid-cols-1 gap-4">
            {recommendations.map((r, i) => (
              <div key={i} className="border border-slate-800 rounded-lg p-4 hover:border-emerald-500/30 transition-colors">
                <div className="flex items-start justify-between gap-3 mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                    {r.category}
                  </span>
                  <span className="text-xs text-emerald-400 font-semibold shrink-0">
                    <TrendingDown className="w-3 h-3 inline mr-0.5" />
                    −{r.potential_reduction_percentage}%
                  </span>
                </div>
                <h3 className="text-sm font-bold text-slate-100 mb-1">{r.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed mb-2">{r.description}</p>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-emerald-400">Save {r.potential_reduction_kg_co2e} kg CO₂e</span>
                  <span className="text-slate-500 italic">{r.scientific_basis?.split('&')[0]}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {exportError && (
        <p className="text-xs text-red-400">{exportError}</p>
      )}
    </div>
  );
}
