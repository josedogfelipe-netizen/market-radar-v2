import clickhouse_connect
import os

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))

class ClickHouseClient:
    def __init__(self):
        self.client = None
    
    def connect(self):
        try:
            self.client = clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT)
            self.init_schema()
        except Exception as e:
            print(f"Failed to connect to ClickHouse: {e}")

    def ping(self):
        if not self.client:
            self.connect()
        try:
            return self.client.command('SELECT 1') == 1
        except Exception:
            return False
            
    def init_schema(self):
        if not self.client:
            return
        
        # Create Ticks Table
        self.client.command('''
        CREATE TABLE IF NOT EXISTS market_ticks (
            timestamp DateTime64(3),
            symbol String,
            price Float64,
            volume Float64,
            source String
        ) ENGINE = MergeTree()
        ORDER BY (symbol, timestamp)
        ''')

        # Create Fragility Metrics Table
        self.client.command('''
        CREATE TABLE IF NOT EXISTS fragility_metrics (
            timestamp DateTime64(3),
            sfi_score Float64,
            oi_liquidity_ratio Float64,
            cvd_divergence Float64,
            funding_stress Float64
        ) ENGINE = MergeTree()
        ORDER BY timestamp
        ''')

ch_client = ClickHouseClient()
