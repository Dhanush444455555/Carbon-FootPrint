import React from 'react';
import { Leaf, BarChart2, CloudRain, Database, PlusCircle, ChevronRight } from 'lucide-react';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: BarChart2 },
  { id: 'input',     label: 'New Assessment', icon: PlusCircle },
  { id: 'weather',   label: 'Climate Data', icon: CloudRain },
  { id: 'data',      label: 'Datasets', icon: Database },
];

export default function Header({ view, navTo, VIEWS }) {
  return (
    <header className="glass-panel-elevated sticky top-0 z-50 border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <button
            onClick={() => navTo(VIEWS.DASHBOARD)}
            className="flex items-center gap-2.5 hover:opacity-80 transition-opacity"
          >
            <span className="text-2xl">🍅</span>
            <div className="hidden sm:block">
              <p className="text-sm font-bold text-white leading-none tracking-tight">Tomato CarbonTrace</p>
              <p className="text-[10px] text-emerald-400 leading-none mt-0.5">Tumakuru · Karnataka · ISO 14040</p>
            </div>
          </button>

          {/* Nav */}
          <nav className="flex items-center gap-1">
            {NAV_ITEMS.map(({ id, label, icon: Icon }) => {
              const active = view === id || (view === VIEWS.RESULTS && id === 'input');
              return (
                <button
                  key={id}
                  onClick={() => navTo(id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                    active
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden md:inline">{label}</span>
                </button>
              );
            })}
          </nav>

          {/* Badge */}
          <div className="hidden sm:flex items-center gap-2 text-xs text-slate-500 border border-slate-700 rounded-full px-3 py-1">
            <Leaf className="w-3 h-3 text-emerald-400" />
            <span>IPCC 2019 · ISO 14044</span>
          </div>
        </div>
      </div>
    </header>
  );
}
