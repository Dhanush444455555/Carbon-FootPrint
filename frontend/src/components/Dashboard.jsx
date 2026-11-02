import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, ReferenceLine
} from 'recharts';
import {
  Leaf, Zap, Droplets, BarChart2, ArrowRight, AlertTriangle,
  TrendingUp, TrendingDown, Target, Info, CheckCircle2,
  Plus, Link2, Database, Sliders, Sparkles, Compass
} from 'lucide-react';
import { useApp } from '../context/AppContext';
import { calculateLocalLca, fetchScenarios } from '../services/api';

const SOURCE_COLORS = {
  'Irrigation Pumping': '#f97316', // Orange
  'Fertilizers & N2O': '#ef4444', // Red
  'Transportation': '#eab308', // Amber/Yellow
  'Land Preparation': '#3b82f6', // Blue
  'Harvest & Packing': '#10b981', // Green
  'Crop Maintenance': '#8b5cf6', // Purple
  'Nursery Seedlings': '#06b6d4'  // Cyan
};

const EMISSION_TRENDS = [
  { month: 'Jan', emissions: 2850, target: 2600, status: 'attention' },
  { month: 'Feb', emissions: 2100, target: 2600, status: 'low' },
  { month: 'Mar', emissions: 2600, target: 2600, status: 'low' },
  { month: 'Apr', emissions: 3150, target: 2600, status: 'attention' },
  { month: 'May', emissions: 3600, target: 2600, status: 'high' },
  { month: 'Jun', emissions: 3950, target: 2600, status: 'high' },
];

export default function Dashboard() {
  const { lcaResult, navTo, VIEWS } = useApp();
  const [scenarios, setScenarios] = useState(null);
  const [activeTab, setActiveTab] = useState('predictive');
  const [trendRange, setTrendRange] = useState('6M');

  const result = lcaResult || calculateLocalLca({});

  useEffect(() => {
    fetchScenarios().then(setScenarios).catch(console.warn);
  }, []);

  // Format stage breakdown for Donut Chart
  const breakdownData = result.stage_breakdown.map((s) => ({
    name: s.stage_name.replace(/Stage \d+: /, ''),
    value: +s.emissions_kg_co2e.toFixed(1),
    pct: s.percentage_of_total,
    color: SOURCE_COLORS[s.stage_name.replace(/Stage \d+: /, '')] || '#10b981'
  }));

  const totalEmissions = result.summary.total_cycle_emissions_kg_co2e;
  const footprintPerKg = result.summary.footprint_kg_co2e_per_kg_marketable;
  const marketableYield = result.summary.marketable_yield_kg;
  const savings = result.summary.potential_emission_savings_kg_co2e;

  return (
    <div className="space-y-6">
      {/* Top Action Header (Carbonlytics style) */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Overview</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Tumakuru District Tomato Carbon Intelligence &amp; Lifecycle Assessment
          </p>
        </div>

        {/* Action icons bar like Carbonlytics */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => navTo(VIEWS.INPUT)}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg transition-colors"
            title="New Assessment"
          >
            <Plus className="w-4 h-4" />
          </button>
          <button
            onClick={() => navTo(VIEWS.DATA_INTEL)}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg transition-colors"
            title="Tumakuru Data Intelligence"
          >
            <Target className="w-4 h-4" />
          </button>
          <button
            onClick={() => navTo(VIEWS.DATA)}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg transition-colors"
            title="Datasets &amp; Sources"
          >
            <Database className="w-4 h-4" />
          </button>
          <button
            onClick={() => navTo(VIEWS.INPUT)}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-md shadow-emerald-900/40 transition-colors"
          >
            <Leaf className="w-3.5 h-3.5" />
            <span>Run LCA Assessment</span>
          </button>
        </div>
      </div>

      {/* Main Carbonlytics 3-Column Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: 3 KPI Cards (4 cols on lg) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          {/* Card 1: Carbon Footprint per kg */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 relative overflow-hidden flex flex-col justify-between">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs text-slate-400 font-medium">Carbon per 1 kg Tomato</span>
                <p className="text-[11px] text-emerald-400 mt-0.5 flex items-center gap-1">
                  <TrendingDown className="w-3 h-3" />
                  -18% vs State Flood Average
                </p>
              </div>
            </div>

            <div className="my-4">
              <div className="flex items-baseline gap-1.5">
                <span className="text-3xl font-extrabold text-white font-mono tracking-tight">
                  {footprintPerKg.toFixed(4)}
                </span>
                <span className="text-xs text-slate-400 font-medium">kg CO₂e/kg</span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                From seed in Tumakuru nursery to APMC mandi market gate
              </p>
            </div>

            <button
              onClick={() => navTo(VIEWS.RESULTS)}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 w-fit"
            >
              Go to Reports <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Card 2: Active Lifecycle Goals */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
            <div>
              <span className="text-xs text-slate-400 font-medium">Active Decarbonization Goals</span>
              <p className="text-[11px] text-amber-400 mt-0.5">3 actions flagged for Tumakuru soil</p>
            </div>

            <div className="my-4">
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-white font-mono">
                  {result.recommendations.length || 3}
                </span>
                <span className="text-xs text-slate-400">interventions</span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Potential reduction: {result.summary.potential_carbon_reduction_pct || 42}% cycle emissions
              </p>
            </div>

            <button
              onClick={() => navTo(VIEWS.RESULTS)}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 w-fit"
            >
              Go to Mitigation <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Card 3: Mitigated CO2 Savings */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
            <div>
              <span className="text-xs text-slate-400 font-medium">Potential CO₂ Savings Identified</span>
              <p className="text-[11px] text-slate-500 mt-0.5">via Drip, Solar pump &amp; INM</p>
            </div>

            <div className="my-4">
              <div className="flex items-baseline gap-1.5">
                <span className="text-3xl font-extrabold text-white font-mono">
                  {savings ? Math.round(savings).toLocaleString() : '1,840'}
                </span>
                <span className="text-xs text-slate-400 font-medium">kg CO₂e/ha</span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Marketable crop: {marketableYield?.toLocaleString() || '44,000'} kg
              </p>
            </div>

            <button
              onClick={() => navTo(VIEWS.RESULTS)}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 w-fit"
            >
              View Breakdown <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Middle Column: Emissions Trend (4 cols on lg) */}
        <div className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-white flex items-center gap-1.5">
                Emissions Trend
                <Info className="w-3.5 h-3.5 text-slate-500" />
              </h2>

              {/* Time Range Pills */}
              <div className="flex items-center bg-slate-800 rounded-lg p-0.5 text-[10px]">
                {['30 D', '3 M', '6 M', '1 Y'].map((range) => (
                  <button
                    key={range}
                    onClick={() => setTrendRange(range)}
                    className={`px-2 py-0.5 rounded-md font-medium transition-all ${
                      trendRange === range
                        ? 'bg-emerald-500/20 text-emerald-400 font-semibold'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {range}
                  </button>
                ))}
              </div>
            </div>

            <p className="text-[11px] text-slate-400 mb-4">
              Monthly seasonal greenhouse emissions profile across Tumakuru agricultural cycles
            </p>

            {/* Recharts Bar Chart matching Carbonlytics style */}
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={EMISSION_TRENDS} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                  <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    labelStyle={{ color: '#f8fafc', fontWeight: 'bold' }}
                    formatter={(v) => [`${v} kg CO₂e`, 'Emissions']}
                  />
                  <ReferenceLine
                    y={2600}
                    stroke="#e2e8f0"
                    strokeDasharray="4 4"
                    label={{ value: 'Target', position: 'right', fill: '#94a3b8', fontSize: 10 }}
                  />
                  <Bar
                    dataKey="emissions"
                    radius={[4, 4, 0, 0]}
                    fill="#10b981"
                  >
                    {EMISSION_TRENDS.map((entry, index) => {
                      let color = '#10b981'; // green
                      if (entry.status === 'attention') color = '#f59e0b'; // amber
                      if (entry.status === 'high') color = '#ef4444'; // red
                      return <Cell key={`cell-${index}`} fill={color} />;
                    })}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap items-center justify-between text-[10px] text-slate-400 pt-3 border-t border-slate-800 gap-2">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" /> Low (Kharif)
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-amber-500" /> Attention (Rabi)
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-red-500" /> High (Summer Pumping)
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-0.5 bg-slate-300" /> Tumakuru Target
            </span>
          </div>
        </div>

        {/* Right Column: Source Breakdown Donut (4 cols on lg) */}
        <div className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-sm font-semibold text-white flex items-center gap-1.5">
                Source Breakdown
                <Info className="w-3.5 h-3.5 text-slate-500" />
              </h2>
              <span className="text-[10px] text-slate-400 font-mono">
                Total: {Math.round(totalEmissions).toLocaleString()} kg CO₂e
              </span>
            </div>

            {/* Donut Chart */}
            <div className="h-44 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={breakdownData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={3}
                  >
                    {breakdownData.map((entry, index) => (
                      <Cell key={`donut-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    formatter={(v) => [`${v} kg CO₂e`, 'Emissions']}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-lg font-bold text-white font-mono">
                  {footprintPerKg.toFixed(2)}
                </span>
                <span className="text-[9px] text-slate-400 uppercase tracking-wider">kg CO₂e/kg</span>
              </div>
            </div>

            {/* Source percentage list */}
            <div className="space-y-1.5 mt-2">
              {breakdownData.slice(0, 5).map((item, idx) => (
                <div key={idx} className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                    <span className="text-slate-300 truncate max-w-[150px]">{item.name}</span>
                  </div>
                  <div className="flex items-center gap-2 font-mono">
                    <span className="text-white font-semibold">{item.pct}%</span>
                    <span className="text-slate-500 text-[10px]">({Math.round(item.value)} kg)</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="text-[10px] text-slate-500 pt-3 border-t border-slate-800 flex items-center justify-between">
            <span>Primary Hotspot:</span>
            <span className="text-amber-400 font-medium">{result.hotspot?.top_stage_name || 'Groundwater Pumping'}</span>
          </div>
        </div>
      </div>

      {/* Bottom Section: Smart Forecast & Goals Progress (2 columns) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Smart Forecast & Insights (7 cols on lg) */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              Smart Forecast &amp; Insights
            </h2>

            {/* Tabs matching Carbonlytics */}
            <div className="flex items-center bg-slate-800/80 rounded-lg p-0.5 text-xs">
              {[
                { id: 'predictive', label: 'Predictive Insights' },
                { id: 'recommendations', label: 'AI Recommendations' },
                { id: 'alerts', label: 'Anomaly Alerts' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-3 py-1 rounded-md text-[11px] font-medium transition-all ${
                    activeTab === tab.id
                      ? 'bg-emerald-600 text-white font-semibold shadow'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {activeTab === 'predictive' && (
            <div className="space-y-3">
              <div className="bg-slate-800/40 border border-slate-800 rounded-xl p-3.5 flex items-start gap-3">
                <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 shrink-0">
                  <TrendingDown className="w-4 h-4" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold text-white">Carbon Reduction Forecast</h3>
                    <span className="text-[10px] text-emerald-400 font-mono font-semibold">On Track</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                    At the current adoption pace of precision fertigation in Tumakuru taluks, regional average tomato carbon intensity is projected to drop from <strong>0.142</strong> to <strong>0.078 kg CO₂e/kg</strong> by 2027.
                  </p>
                </div>
              </div>

              <div className="bg-slate-800/40 border border-slate-800 rounded-xl p-3.5 flex items-start gap-3">
                <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 shrink-0">
                  <Target className="w-4 h-4" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold text-white">Target vs Actual Emissions</h3>
                    <span className="text-[10px] text-amber-400 font-mono font-semibold">Review Needed</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                    Current open-field flood irrigation in Madhugiri and Pavagada exceeds target carbon ceilings by <strong>24%</strong> due to deep aquifer heads (160m–178m bgl).
                  </p>
                </div>
              </div>

              <div className="bg-slate-800/40 border border-slate-800 rounded-xl p-3.5 flex items-start gap-3">
                <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 shrink-0">
                  <Sliders className="w-4 h-4" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold text-white">Machine Learning Sensitivity Rank</h3>
                    <span className="text-[10px] text-blue-400 font-mono font-semibold">R² = 0.954</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                    Random Forest sensitivity analysis flags <strong>pumping water volume</strong> (38% weight) and <strong>synthetic nitrogen application</strong> (32% weight) as the dominant variance drivers.
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="space-y-3">
              {result.recommendations.map((rec, idx) => (
                <div key={idx} className="bg-slate-800/40 border border-slate-800 rounded-xl p-3.5">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-bold text-white">{rec.title}</span>
                    <span className="text-[10px] text-emerald-400 font-mono font-semibold">
                      -{rec.potential_reduction_percentage}% CO₂
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">{rec.description}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'alerts' && (
            <div className="space-y-3">
              <div className="bg-red-950/20 border border-red-900/40 rounded-xl p-3.5 flex items-start gap-3">
                <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-xs font-bold text-red-300">High Synthetic Urea Overdose Risk</h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Urea applied above 220 kg/ha triggers non-linear IPCC direct N₂O emissions (EF1 = 0.010 kg N₂O-N/kg N) and substantial leaching into groundwater.
                  </p>
                </div>
              </div>
              <div className="bg-amber-950/20 border border-amber-900/40 rounded-xl p-3.5 flex items-start gap-3">
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-xs font-bold text-amber-300">Excessive Diesel Consumption on Heavy Alfisols</h3>
                  <p className="text-xs text-slate-400 mt-1">
                    More than 3 rotary tiller passes burns over 45 L/ha diesel without agronomic soil tilth gains.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Goals Progress Bars (5 cols on lg) */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-white flex items-center gap-1.5">
                <Target className="w-4 h-4 text-emerald-400" />
                Decarbonization Goals Progress
              </h2>
              <button
                onClick={() => navTo(VIEWS.INPUT)}
                className="text-xs text-emerald-400 hover:text-emerald-300 font-medium"
              >
                Update
              </button>
            </div>

            <div className="space-y-4">
              {/* Goal 1 */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-white">Cut Borewell Energy Use by 25%</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    On Track
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-gradient-to-r from-emerald-500 to-green-400 h-2 rounded-full" style={{ width: '65%' }} />
                </div>
                <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                  <span>65% Achieved</span>
                  <span>Due: Dec 2026</span>
                </div>
              </div>

              {/* Goal 2 */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-white">Transition to Reusable HDPE Crates</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    Needs Review
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-gradient-to-r from-amber-500 to-yellow-400 h-2 rounded-full" style={{ width: '40%' }} />
                </div>
                <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                  <span>40% Shifted from Wood</span>
                  <span>Due: Mar 2027</span>
                </div>
              </div>

              {/* Goal 3 */}
              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-semibold text-white">Solar Pumping Subsidy Integration</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    In Progress
                  </span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div className="bg-gradient-to-r from-blue-500 to-cyan-400 h-2 rounded-full" style={{ width: '28%' }} />
                </div>
                <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                  <span>KUSUM Scheme Applications</span>
                  <span>Ongoing</span>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 mt-4">
            <p className="text-[11px] text-slate-400 flex items-center justify-between">
              <span>Benchmark: UAS Bengaluru BMP</span>
              <span className="text-white font-mono font-semibold">0.073 kg CO₂e/kg</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
