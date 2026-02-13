import asyncio
import json
import logging
import random
import math
from app.database.redis import redis_client

logger = logging.getLogger(__name__)

class FragilityEngine:
    def __init__(self):
        self.running = False

    async def calculate_oi_liquidity_ratio(self, symbol="BTCUSDT"):
        # MOCK: Real implementation would fetch OI from exchange API and Orderbook depth
        # For Demo: Random walk with trend
        current_oi = 500000000 + random.uniform(-1000000, 5000000)
        liquidity_2pct = 10000000 + random.uniform(-500000, 500000)
        
        ratio = current_oi / liquidity_2pct
        return ratio

    async def calculate_cvd_divergence(self, symbol="BTCUSDT"):
        # MOCK: Simulate divergence. Postive = Fragile (Price Up, Spot Down)
        # 0 = Neutral, > 0 = Bearish Divergence (Fragile), < 0 = Bullish
        return random.uniform(-500000, 500000)

    async def compute_fragility_score(self):
        """
        Combines multiple metrics into a single 0-100 score.
        """
        while self.running:
            try:
                # 1. Gather Metrics
                oi_liq_ratio = await self.calculate_oi_liquidity_ratio()
                cvd_div = await self.calculate_cvd_divergence()
                
                # 2. Normalize and Weight
                # Rule: High OI/Liq (> 30) is bad. High Divergence is bad.
                
                score_component_1 = min(100, (oi_liq_ratio / 50) * 100) # 50 is extreme ratio
                score_component_2 = min(100, (max(0, cvd_div) / 300000) * 100)
                
                final_score = (score_component_1 * 0.6) + (score_component_2 * 0.4)
                final_score = min(100, max(0, final_score)) + random.uniform(-2, 2) # Noise

                # 3. Determine Market Regime
                regime = "GREEN"
                if final_score > 40: regime = "YELLOW"
                if final_score > 70: regime = "RED"

                # 4. Publish Update
                payload = {
                    "timestamp": asyncio.get_event_loop().time(),
                    "score": round(final_score, 2),
                    "regime": regime,
                    "metrics": {
                        "oi_liquidity_ratio": round(oi_liq_ratio, 2),
                        "cvd_divergence": round(cvd_div, 2)
                    }
                }
                
                await redis_client.set("fragility_index", json.dumps(payload))
                await redis_client.publish("fragility_updates", json.dumps(payload))
                
                logger.info(f"Fragility Updated: {final_score:.2f} [{regime}]")
                
                await asyncio.sleep(2) # Update every 2 seconds

            except Exception as e:
                logger.error(f"Error in Fragility Engine: {e}")
                await asyncio.sleep(5)

    async def start(self):
        self.running = True
        logger.info("Fragility Engine Started")
        await self.compute_fragility_score()

fragility_engine = FragilityEngine()
