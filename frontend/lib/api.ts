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

// In Cloud/Docker, we use the Next.js proxy at /api/...
const API_URL = ''; // Relative path uses the proxy

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

export const getWebSocketUrl = () => {
    if (typeof window !== 'undefined') {
        // Dynamic WS URL based on current page location
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

        // In Codespaces, we need to handle the port forwarding URL structure if possible,
        // OR rely on the User forwarding port 8000.
        // BUT, a cleaner trick for Codespaces usually involves specific handling.
        // For simplicity now: Try to guess the backend URL or fallback to localhost.

        // Attempt to replace port 3000 with 8000 in the hostname if it contains 3000
        const host = window.location.host;
        if (host.includes('-3000')) {
            return `${protocol}//${host.replace('-3000', '-8000')}/api/v1/dashboard/ws`;
        }

        return `${protocol}//${window.location.hostname}:8000/api/v1/dashboard/ws`;
    }
    return 'ws://localhost:8000/api/v1/dashboard/ws';
};
