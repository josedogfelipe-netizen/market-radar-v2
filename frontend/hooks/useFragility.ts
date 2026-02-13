"use client";

import { useEffect, useState } from 'react';
import { FragilityData, getWebSocketUrl, fetchFragility } from '@/lib/api';

export const useFragility = () => {
    const [data, setData] = useState<FragilityData | null>(null);
    const [status, setStatus] = useState<string>('Connecting...');

    useEffect(() => {
        // Initial Fetch
        fetchFragility().then(initialData => {
            setData(initialData);
            setStatus('Connected');
        });

        // WebSocket Setup
        const wsUrl = getWebSocketUrl();
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            console.log('Connected to WS');
            setStatus('Live');
        };

        ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                if (message.score !== undefined) {
                    setData(message);
                }
            } catch (e) {
                console.error("WS Parse Error", e);
            }
        };

        ws.onclose = () => {
            console.log('WS Disconnected');
            setStatus('Disconnected (Reconnecting...)');
            // Reconnection logic could go here
        };

        return () => {
            ws.close();
        };
    }, []);

    return { data, status };
};
