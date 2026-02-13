const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/api/v1/dashboard/ws';

export interface FragilityData {
    timestamp: number;
    score: number;
    regime: 'GREEN' | 'YELLOW' | 'RED';
    metrics: {
        oi_liquidity_ratio: number;
        cvd_divergence: number;
    };
    message?: string;
}

export const fetchFragility = async (): Promise<FragilityData> => {
    try {
        const res = await fetch(`${API_URL}/api/v1/dashboard/fragility`, { cache: 'no-store' });
        if (!res.ok) throw new Error('Failed to fetch data');
        return res.json();
    } catch (error) {
        console.error(error);
        return {
            timestamp: Date.now(),
            score: 0,
            regime: 'GREEN',
            metrics: { oi_liquidity_ratio: 0, cvd_divergence: 0 },
            message: "Offline"
        };
    }
};

export const getWebSocketUrl = () => WS_URL;
