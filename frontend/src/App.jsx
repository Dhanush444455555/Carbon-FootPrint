import React, { useState } from 'react';
import { AppContext } from './context/AppContext';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import FarmInputForm from './components/FarmInputForm';
import ResultsPanel from './components/ResultsPanel';
import WeatherPanel from './components/WeatherPanel';
import DataPanel from './components/DataPanel';
import FarmRecordsLogbook from './components/FarmRecordsLogbook';
import { MapPin, ShieldCheck, ChevronRight, Bell, Moon, Sun } from 'lucide-react';

export const VIEWS = {
  DASHBOARD: 'dashboard',
  INPUT: 'input',
  RESULTS: 'results',
  WEATHER: 'weather',
  DATA: 'data',
  DATA_INTEL: 'data_intel',
  RECORDS: 'records',
};

export default function App() {
  const [view, setView] = useState(VIEWS.DASHBOARD);
  const [lcaResult, setLcaResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const navTo = (v) => setView(v);

  const getBreadcrumbTitle = () => {
    switch (view) {
      case VIEWS.DASHBOARD: return 'Overview';
      case VIEWS.INPUT: return 'LCA Farm Assessment';
      case VIEWS.RESULTS: return 'Carbon Footprint Results';
      case VIEWS.WEATHER: return 'Weather & Climate Normals';
      case VIEWS.DATA: return 'Datasets & Taluk Inventory';
      case VIEWS.DATA_INTEL: return 'Tumakuru Data Intelligence';
      case VIEWS.RECORDS: return 'Tumakuru Farmer Logbook';
      default: return 'Overview';
    }
  };

  return (
    <AppContext.Provider value={{ lcaResult, setLcaResult, isLoading, setIsLoading, navTo, VIEWS }}>
      <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
        {/* Left Sidebar Navigation */}
        <Sidebar
          view={view}
          navTo={navTo}
          VIEWS={VIEWS}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
        />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {/* Top Bar (Carbonlytics style) */}
          <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur flex items-center justify-between px-6 shrink-0 z-10">
            {/* Breadcrumb & Geographic Tag */}
            <div className="flex items-center gap-3 min-w-0">
              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <span>Dashboard</span>
                <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="font-semibold text-white truncate">{getBreadcrumbTitle()}</span>
              </div>
              <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/40 text-[11px] text-emerald-400">
                <MapPin className="w-3 h-3" />
                <span>Tumakuru District, Karnataka</span>
              </div>
            </div>

            {/* Right Tools & Badges */}
            <div className="flex items-center gap-3">
              <span className="hidden lg:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-300">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>IPCC 2019 Refinement · ISO 14044</span>
              </span>

              {/* Status pill */}
              <div className="hidden md:flex items-center gap-2 pl-3 border-l border-slate-800">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-xs text-slate-400">Online</span>
              </div>

              {/* User Avatar */}
              <div className="flex items-center gap-2 pl-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-600 to-green-500 flex items-center justify-center text-xs font-bold text-white shadow-sm">
                  TM
                </div>
                <div className="hidden xl:block text-left">
                  <p className="text-xs font-semibold text-white leading-tight">Tumakuru Agronomist</p>
                  <p className="text-[10px] text-slate-400 leading-tight">KDA / ICAR Verified</p>
                </div>
              </div>
            </div>
          </header>

          {/* View Container */}
          <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
              {view === VIEWS.DASHBOARD && <Dashboard />}
              {view === VIEWS.INPUT && <FarmInputForm />}
              {view === VIEWS.RESULTS && <ResultsPanel />}
              {view === VIEWS.WEATHER && <WeatherPanel />}
              {view === VIEWS.DATA && <DataPanel />}
              {view === VIEWS.DATA_INTEL && <DataPanel />}
              {view === VIEWS.RECORDS && <FarmRecordsLogbook />}
            </div>
          </main>
        </div>
      </div>
    </AppContext.Provider>
  );
}
