"use client";

import { useFragility } from '@/hooks/useFragility';
import { RadarGauge } from '@/components/radar/RadarGauge';

export default function Home() {
    const { data, status } = useFragility();

    return (
        <main className="flex min-h-screen flex-col items-center p-8 bg-slate-950 text-white">
            {/* Header */}
            <div className="w-full flex justify-between items-center mb-12 border-b border-slate-800 pb-4">
                <h1 className="text-2xl font-mono font-bold tracking-tighter">
                    RADAR <span className="text-red-500">v2.0</span>
                </h1>
                <div className="flex items-center gap-2 text-sm font-mono">
                    <div className={`w-2 h-2 rounded-full ${status === 'Live' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
                    <span className="text-slate-400">{status}</span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 w-full max-w-7xl">

                {/* Main Gauge */}
                <div className="lg:col-span-1">
                    <RadarGauge
                        score={data?.score || 0}
                        regime={data?.regime || 'Loading...'}
                    />
                </div>

                {/* Metrics Panel */}
                <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-6 bg-slate-900 rounded-xl border border-slate-800">
                        <h3 className="text-slate-400 font-mono text-xs uppercase mb-2">OI / Liquidity Ratio</h3>
                        <div className="text-3xl font-bold font-mono">
                            {data?.metrics.oi_liquidity_ratio?.toFixed(2) || '---'}
                        </div>
                        <p className="text-xs text-slate-500 mt-2">
                    High ratio (>2.5) indicates leverage overload relative to order book depth.
                        </p>
                    </div>

                    <div className="p-6 bg-slate-900 rounded-xl border border-slate-800">
                        <h3 className="text-slate-400 font-mono text-xs uppercase mb-2">CVD Divergence</h3>
                        <div className="text-3xl font-bold font-mono">
                            {data?.metrics.cvd_divergence?.toFixed(0) || '---'}
                        </div>
                        <p className="text-xs text-slate-500 mt-2">
                            Positive = Fragile (Perp buying into Spot selling).
                        </p>
                    </div>

                    <div className="col-span-1 md:col-span-2 p-6 bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-center">
                        <p className="text-slate-600 font-mono text-sm">[ Real-time Chart Placeholder ]</p>
                    </div>
                </div>
            </div>
        </main>
    )
}
