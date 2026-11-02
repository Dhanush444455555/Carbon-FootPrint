import React from 'react';
import {
  LayoutDashboard, PlusCircle, BarChart2, CloudRain, Database,
  Leaf, Zap, TrendingUp, FileText, Brain, MapPin, FlaskConical,
  ChevronRight, Menu, X, Target
} from 'lucide-react';

const NAV_SECTIONS = [
  {
    label: 'Dashboard',
    items: [
      { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
      { id: 'results',   label: 'Emissions by Stage', icon: BarChart2 },
      { id: 'input',     label: 'KPI Tracker', icon: Target },
    ],
  },
  {
    label: 'Data Sources',
    items: [
      { id: 'records', label: 'Farmer Logbook', icon: FileText },
      { id: 'input',   label: 'Farm Activity Input', icon: Leaf },
      { id: 'weather', label: 'Weather & Climate', icon: CloudRain },
      { id: 'data',    label: 'Soil & Logistics', icon: MapPin },
      { id: 'data',    label: 'Market & Mandi', icon: TrendingUp },
    ],
  },
  {
    label: 'Analysis',
    items: [
      { id: 'input',      label: 'LCA Calculator', icon: FlaskConical },
      { id: 'results',    label: 'ML Predictions', icon: Brain },
      { id: 'dashboard',  label: 'Benchmarks', icon: Zap },
    ],
  },
  {
    label: 'Reporting',
    items: [
      { id: 'results',    label: 'Reports & Export', icon: FileText },
      { id: 'data_intel', label: 'Data Intelligence', icon: Database },
    ],
  },
];

export default function Sidebar({ view, navTo, VIEWS, sidebarOpen, setSidebarOpen }) {
  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-20 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar panel */}
      <aside
        className={`
          fixed md:relative z-30 h-full flex flex-col
          bg-slate-900 border-r border-slate-800
          transition-all duration-300 ease-in-out
          ${sidebarOpen ? 'w-60' : 'w-0 md:w-14'}
          overflow-hidden
        `}
      >
        {/* Brand header */}
        <div className="flex items-center gap-3 px-4 py-4 border-b border-slate-800 min-w-[240px]">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-green-600 flex items-center justify-center text-sm shrink-0">
            🍅
          </div>
          {sidebarOpen && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-white leading-tight truncate">Tomato CarbonTrace</p>
              <p className="text-[10px] text-emerald-400 leading-tight truncate">Tumakuru · Karnataka</p>
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="ml-auto text-slate-500 hover:text-slate-300 transition-colors shrink-0 hidden md:block"
          >
            {sidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-3 min-w-[240px]">
          {NAV_SECTIONS.map((section) => (
            <div key={section.label} className="mb-4">
              {sidebarOpen && (
                <p className="px-4 pb-1 text-[10px] font-semibold uppercase tracking-widest text-slate-500">
                  {section.label}
                </p>
              )}
              {section.items.map((item, idx) => {
                const isActive = view === item.id;
                const Icon = item.icon;
                return (
                  <button
                    key={`${section.label}-${idx}`}
                    onClick={() => navTo(item.id)}
                    title={!sidebarOpen ? item.label : undefined}
                    className={`
                      w-full flex items-center gap-3 px-4 py-2 text-sm transition-all group
                      ${isActive
                        ? 'bg-emerald-500/15 text-emerald-400 border-r-2 border-emerald-500'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                      }
                    `}
                  >
                    <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-emerald-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
                    {sidebarOpen && (
                      <span className="truncate">{item.label}</span>
                    )}
                    {sidebarOpen && isActive && (
                      <ChevronRight className="w-3 h-3 ml-auto shrink-0 text-emerald-500" />
                    )}
                  </button>
                );
              })}
            </div>
          ))}
        </nav>

        {/* Standards badge at bottom */}
        <div className="border-t border-slate-800 p-3 min-w-[240px]">
          {sidebarOpen ? (
            <div className="flex flex-col gap-1.5">
              <div className="flex items-center gap-2 px-2 py-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
                <Leaf className="w-3 h-3 text-emerald-400 shrink-0" />
                <span className="text-[10px] text-emerald-400 font-medium">IPCC 2019 • ISO 14040/44</span>
              </div>
              <p className="text-[9px] text-slate-600 text-center">Tumakuru District Carbon Intelligence Platform</p>
            </div>
          ) : (
            <div className="flex justify-center">
              <Leaf className="w-4 h-4 text-emerald-500" />
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
