import React from 'react';

export const Alert = ({ title, children, variant = 'default' }: { title: string, children: React.ReactNode, variant?: 'default' | 'destructive' }) => {
    const bg = variant === 'destructive' ? 'bg-red-900/50 border-red-900' : 'bg-slate-800 border-slate-700';
    const text = variant === 'destructive' ? 'text-red-200' : 'text-slate-200';

    return (
        <div className={`p-4 rounded-lg border ${bg} ${text} mb-4`}>
            <h5 className="font-bold mb-1">{title}</h5>
            <div className="text-sm opacity-90">{children}</div>
        </div>
    );
};
