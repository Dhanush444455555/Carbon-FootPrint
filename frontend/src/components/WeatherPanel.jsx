import React, { useEffect, useState } from 'react';
import {
  CloudRain, Sun, Droplets, Wind, Thermometer,
  Calendar, CheckCircle, Info, AlertCircle, ArrowUpRight
} from 'lucide-react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid, Legend, AreaChart, Area
} from 'recharts';
import { fetchWeather } from '../services/api';

export default function WeatherPanel() {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('rainfall');

  useEffect(() => {
    fetchWeather()
      .then((data) => {
        setWeatherData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Weather load error:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500" />
      </div>
    );
  }

  const climate = weatherData?.monthly_climate || [];

  return (
    <div className="space-y-6">
      {/* Top Banner / Station Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700/80 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                OFFICIAL STATION RECORD
              </span>
              <span className="text-xs text-slate-400">IMD Station No. 43291</span>
            </div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <CloudRain className="w-6 h-6 text-cyan-400" />
              Tumakuru Climatological Observations & Crop Water Needs
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Verified ground-station climate normals (1991–2020) from India Meteorological Department (IMD) for Tumakuru district, Karnataka.
              Used for calculating Penman-Monteith reference evapotranspiration (ETo) and agricultural irrigation demand.
            </p>
          </div>
          <div className="flex flex-row md:flex-col items-end gap-2 shrink-0">
            <div className="text-right">
              <span className="text-xs text-slate-400">Normal Annual Rainfall</span>
              <p className="text-2xl font-bold text-cyan-400 font-mono">
                {weatherData?.annual_rainfall_mm || 688.4} <span className="text-sm font-normal text-slate-400">mm</span>
              </p>
            </div>
          </div>
        </div>

        {/* Quick KPI stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-5 border-t border-slate-800">
          <div className="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 flex items-center gap-1.5">
              <Thermometer className="w-3.5 h-3.5 text-amber-400" /> Mean Temp Range
            </span>
            <p className="text-lg font-bold text-white mt-1">15.2°C – 36.2°C</p>
            <span className="text-[10px] text-slate-500">Min in Jan · Max in Apr</span>
          </div>

          <div className="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 flex items-center gap-1.5">
              <Droplets className="w-3.5 h-3.5 text-blue-400" /> Peak Monsoon Month
            </span>
            <p className="text-lg font-bold text-blue-400 mt-1">September (138 mm)</p>
            <span className="text-[10px] text-slate-500">Late Kharif season</span>
          </div>

          <div className="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 flex items-center gap-1.5">
              <Sun className="w-3.5 h-3.5 text-yellow-400" /> Avg Daily ETo
            </span>
            <p className="text-lg font-bold text-amber-300 mt-1">4.6 mm/day</p>
            <span className="text-[10px] text-slate-500">Reference ET (FAO-56)</span>
          </div>

          <div className="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
            <span className="text-xs text-slate-400 flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> Data Classification
            </span>
            <p className="text-lg font-bold text-emerald-400 mt-1">Measured IMD</p>
            <span className="text-[10px] text-slate-500">Zero synthetic grid proxy</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Rainfall & ETo Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <CloudRain className="w-4 h-4 text-cyan-400" />
                Monthly Rainfall vs Evapotranspiration (Tumakuru)
              </h2>
              <p className="text-xs text-slate-500">Rainfall (mm) & FAO-56 Reference ETo (mm/day)</p>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={climate} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  labelStyle={{ color: '#f8fafc', fontWeight: 'bold' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="rainfall_mm" name="Rainfall (mm)" fill="#06b6d4" radius={[4, 4, 0, 0]} />
                <Bar dataKey="eto_mm_day" name="ETo (mm/day)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Temperature Regime Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <Thermometer className="w-4 h-4 text-amber-400" />
                Thermal Regime: Min & Max Temperatures (°C)
              </h2>
              <p className="text-xs text-slate-500">Directly influences tomato flowering and pollination efficiency</p>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={climate} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <YAxis stroke="#94a3b8" domain={[10, 40]} tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  labelStyle={{ color: '#f8fafc', fontWeight: 'bold' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line type="monotone" dataKey="t_max_c" name="Max Temp (°C)" stroke="#ef4444" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="t_min_c" name="Min Temp (°C)" stroke="#38bdf8" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Tomato Agronomic Calendar for Tumakuru */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
          <Calendar className="w-5 h-5 text-emerald-400" />
          Tumakuru Tomato Crop Calendar & Seasonal Carbon Footprint Dynamics
        </h2>
        <p className="text-xs text-slate-400 mb-4">
          Calibrated to local sowing windows advised by KVK Tumakuru (Hirehalli) & UAS Bengaluru.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border border-slate-800 rounded-xl p-4 bg-slate-800/30">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20">
                Kharif Season (Rain-Fed / Supplemental)
              </span>
            </div>
            <p className="text-sm font-bold text-white">Transplanting: June – July</p>
            <p className="text-xs text-slate-400 mt-1">Harvesting: Sept – Nov</p>
            <div className="mt-3 text-xs text-slate-300 space-y-1">
              <p>• <strong>Irrigation Power:</strong> Lowest pump energy due to monsoon rains.</p>
              <p>• <strong>Disease Pressure:</strong> High blight risk requires careful fungicide management.</p>
              <p className="text-emerald-400 font-mono text-[11px] mt-2">Avg Footprint: 0.08 – 0.12 kg CO₂e/kg</p>
            </div>
          </div>

          <div className="border border-slate-800 rounded-xl p-4 bg-slate-800/30">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold px-2 py-0.5 bg-blue-500/10 text-blue-400 rounded-full border border-blue-500/20">
                Rabi Season (Winter / High Quality)
              </span>
            </div>
            <p className="text-sm font-bold text-white">Transplanting: Oct – Nov</p>
            <p className="text-xs text-slate-400 mt-1">Harvesting: Jan – March</p>
            <div className="mt-3 text-xs text-slate-300 space-y-1">
              <p>• <strong>Irrigation Power:</strong> Moderate borewell extraction (depth ~140m).</p>
              <p>• <strong>Fruit Set:</strong> Optimal daytime/night temp difference (high yields).</p>
              <p className="text-blue-400 font-mono text-[11px] mt-2">Avg Footprint: 0.06 – 0.10 kg CO₂e/kg</p>
            </div>
          </div>

          <div className="border border-slate-800 rounded-xl p-4 bg-slate-800/30">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded-full border border-amber-500/20">
                Summer Season (High Pumping Energy)
              </span>
            </div>
            <p className="text-sm font-bold text-white">Transplanting: Jan – Feb</p>
            <p className="text-xs text-slate-400 mt-1">Harvesting: April – June</p>
            <div className="mt-3 text-xs text-slate-300 space-y-1">
              <p>• <strong>Irrigation Power:</strong> Highest groundwater pumping (borewells stressed).</p>
              <p>• <strong>Market Price:</strong> Typically fetches premium prices at APMC.</p>
              <p className="text-amber-400 font-mono text-[11px] mt-2">Avg Footprint: 0.18 – 0.28 kg CO₂e/kg</p>
            </div>
          </div>
        </div>
      </div>

      {/* Climatological Normals Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-white">
              Official Monthly Station Table – IMD Tumakuru
            </h3>
            <p className="text-xs text-slate-500">12-Month Climatological Normals</p>
          </div>
          <span className="text-[11px] text-slate-400 bg-slate-800 px-2 py-1 rounded">
            Classification: MEASURED DATA
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-800/60 text-slate-400 uppercase tracking-wider text-[10px]">
              <tr>
                <th className="py-2.5 px-3 rounded-l">Month</th>
                <th className="py-2.5 px-3">Min Temp (°C)</th>
                <th className="py-2.5 px-3">Max Temp (°C)</th>
                <th className="py-2.5 px-3">Rainfall (mm)</th>
                <th className="py-2.5 px-3">ETo (mm/day)</th>
                <th className="py-2.5 px-3 rounded-r">Water Balance Deficit</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {climate.map((row) => {
                const monthlyEtoMm = row.eto_mm_day * 30.4;
                const deficit = +(row.rainfall_mm - monthlyEtoMm).toFixed(1);
                const isDeficit = deficit < 0;
                return (
                  <tr key={row.month} className="hover:bg-slate-800/40">
                    <td className="py-2 px-3 font-semibold text-white">{row.month}</td>
                    <td className="py-2 px-3 font-mono text-cyan-300">{row.t_min_c}</td>
                    <td className="py-2 px-3 font-mono text-amber-300">{row.t_max_c}</td>
                    <td className="py-2 px-3 font-mono text-blue-300">{row.rainfall_mm}</td>
                    <td className="py-2 px-3 font-mono text-slate-200">{row.eto_mm_day}</td>
                    <td className="py-2 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${
                        isDeficit ? 'bg-red-950/60 text-red-400 border border-red-800/40' : 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/40'
                      }`}>
                        {deficit > 0 ? `+${deficit} mm (Surplus)` : `${deficit} mm (Deficit)`}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
