import streamlit as st
from threading import Thread
from models.slippage_model import SlippageModel
from models.market_impact import estimate_market_impact
from models.maker_taker_model import MakerTakerModel
from utils.websocket_client import OrderBookWebSocket
from utils.fee_model import calculate_fee
from utils.latency_tracker import average_latency
import numpy as np
import asyncio

st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Trade Parameters")
exchange = st.sidebar.selectbox("Exchange", ["OKX"])
symbol = st.sidebar.text_input("Spot Asset", "BTC-USDT-SWAP")
quantity = st.sidebar.slider("Quantity (USD)", 10, 1000, 100)
volatility = st.sidebar.slider("Volatility (0.01 - 1%)", 0.001, 0.05, 0.01)
fee_tier = st.sidebar.selectbox("Fee Tier", [0.0005, 0.001, 0.0015], index=1)

# Output Panel
st.title("Real-Time Trade Simulation")
output_placeholder = st.empty()

# Models
slippage_model = SlippageModel()
maker_taker_model = MakerTakerModel()
latencies = []

# Callback for new tick
def process_tick(data, latency):
    bids = data.get("bids", [])
    asks = data.get("asks", [])
    mid_price = (float(bids[0][0]) + float(asks[0][0])) / 2
    liquidity = sum([float(level[1]) for level in bids[:5]])  # depth liquidity
    order_size = quantity / mid_price

    slippage = slippage_model.predict([volatility, order_size, liquidity])
    fee = calculate_fee(quantity, fee_tier)
    impact = estimate_market_impact(order_size, volatility, liquidity)
    net_cost = slippage * quantity + fee + impact
    maker_taker = maker_taker_model.predict_proba([volatility, liquidity])

    latencies.append(latency)
    avg_latency = average_latency(latencies[-100:])

    output_placeholder.markdown(f"""
    **Mid Price:** ${mid_price:.2f}  
    **Estimated Slippage:** ${slippage*quantity:.4f}  
    **Estimated Fee:** ${fee:.4f}  
    **Market Impact:** ${impact:.4f}  
    **Net Cost:** ${net_cost:.4f}  
    **Maker Probability:** {maker_taker[0]:.2%}  
    **Taker Probability:** {maker_taker[1]:.2%}  
    **Latency (avg/tick):** {avg_latency:.6f} sec
    """)
    
# Start WebSocket
def start_ws():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws = OrderBookWebSocket(
        url="wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP",
        symbol=symbol,
        callback=process_tick
    )
    
    loop.run_until_complete(ws.listen())

if 'ws_started' not in st.session_state:
    thread = Thread(target=start_ws)
    thread.daemon = True
    thread.start()
    st.session_state.ws_started = True