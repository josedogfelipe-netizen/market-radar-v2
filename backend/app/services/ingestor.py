import asyncio
import json
import logging
import websockets
from app.database.redis import redis_client
from app.database.clickhouse import ch_client
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BINANCE_WS_URL = "wss://fstream.binance.com/ws/btcusdt@aggTrade/ethusdt@aggTrade/solusdt@aggTrade"

async def process_trade(trade_data):
    """
    Process raw trade data from Binance and store/publish it.
    """
    try:
        symbol = trade_data['s']
        price = float(trade_data['p'])
        quantity = float(trade_data['q'])
        timestamp = datetime.fromtimestamp(trade_data['T'] / 1000)
        is_buyer_maker = trade_data['m']
        
        # 1. Update Real-time State in Redis (e.g., last price)
        await redis_client.set(f"price:{symbol}", price)
        
        # 2. Publish to internal channel for Fragility Engine
        await redis_client.publish(f"trades:{symbol}", json.dumps({
            "s": symbol, "p": price, "q": quantity, "t": trade_data['T'], "m": is_buyer_maker
        }))
        
        # 3. Store in ClickHouse (Batching would be better in prod, simplistic here)
        # Note: In a real high-load app, use a buffer.
        # ch_client.client.insert('market_ticks', [[timestamp, symbol, price, quantity, 'binance']])
        
    except Exception as e:
        logger.error(f"Error processing trade: {e}")

async def binance_ingestor():
    """
    Connects to Binance WebSocket and ingests data.
    """
    while True:
        try:
            async with websockets.connect(BINANCE_WS_URL) as websocket:
                logger.info("Connected to Binance WebSocket")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if 'e' in data and data['e'] == 'aggTrade':
                        await process_trade(data)
        except Exception as e:
            logger.error(f"Binance connection lost: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)

async def start_ingestors():
    """
    Starts all data collectors.
    """
    await asyncio.gather(
        binance_ingestor(),
        # Add other collectors here (Bybit, On-chain mock, etc.)
    )

if __name__ == "__main__":
    # For standalone testing
    asyncio.run(start_ingestors())
