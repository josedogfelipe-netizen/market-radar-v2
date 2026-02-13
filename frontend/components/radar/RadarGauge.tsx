"use client";

import React from 'react';

interface RadarGaugeProps {
    score: number;
    regime: string;
}

export const RadarGauge: React.FC<RadarGaugeProps> = ({ score, regime }) => {
    // Determine color based on score/regime
    let colorClass = "text-green-500";
    let progressColor = "bg-green-500";

    if (score > 40) {
        colorClass = "text-yellow-500";
        progressColor = "bg-yellow-500";
    }
    if (score > 70) {
        colorClass = "text-red-500";
        progressColor = "bg-red-500";
    }

    // Rotation calculation for a semi-circle gauge (not perfect but simple visual)
    const rotation = (score / 100) * 180;

    return (
        <div className="relative flex flex-col items-center justify-center p-6 bg-slate-900 rounded-xl border border-slate-800">
            <h2 className="text-xl font-mono mb-4 text-slate-400">STRUCTURAL FRAGILITY INDEX</h2>

            <div className="relative w-64 h-32 overflow-hidden mb-4">
                <div className="absolute top-0 left-0 w-full h-full bg-slate-800 rounded-t-full"></div>
                <div
                    className={`absolute top-0 left-0 w-full h-full ${progressColor} origin-bottom transition-all duration-1000 ease-out rounded-t-full opacity-75 blur-sm`}
                    style={{ transform: `rotate(${rotation - 180}deg)` }}
                ></div>
                <div
                    className={`absolute top-0 left-0 w-full h-full ${progressColor} origin-bottom transition-all duration-1000 ease-out rounded-t-full`}
                    style={{ transform: `rotate(${rotation - 180}deg)` }}
                ></div>
                <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-48 h-24 bg-slate-900 rounded-t-full flex items-end justify-center pb-2">
                    <span className={`text-5xl font-bold font-mono ${colorClass}`}>
                        {Math.round(score)}
                    </span>
                </div>
            </div>

            <div className={`mt-2 px-4 py-1 rounded-full text-xs font-bold border ${colorClass} border-opacity-30 bg-opacity-10 bg-white uppercase tracking-widest`}>
                REGIME: {regime}
            </div>

            <div className="mt-6 w-full grid grid-cols-2 gap-4 text-sm">
                <div className="flex justify-between border-b border-slate-800 pb-1">
                    <span className="text-slate-500">Normal</span>
                    <span className="text-green-500">0-40</span>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-1">
                    <span className="text-slate-500">Caution</span>
                    <span className="text-yellow-500">40-70</span>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-1">
                    <span className="text-slate-500">DANGER</span>
                    <span className="text-red-500">70-100</span>
                </div>
            </div>
        </div>
    );
};
