import websockets
import ujson
import asyncio
import time
from datetime import datetime

class OrderBookWebSocket:
    def __init__(self, url, symbol, callback):
        self.url = url
        self.symbol = symbol
        self.callback = callback
        self.latencies = []

    async def listen(self):
        async with websockets.connect(self.url) as ws:
            print(f"Connected to {self.url}")
            while True:
                start = time.perf_counter();
                raw_msg = await ws.recv();
                data = ujson.loads(raw_msg);
                
                if data.get("symbol") == self.symbol:
                    latency = time.perf_counter() - start
                    self.latencies.append(latency)
                    await self.callback(data, latency)
                    
    def run(self):
        asyncio.get_event_loop().run_until_complete(self.listen())