def estimate_market_impact(order_size, volatility, liquidity, alpha=0.1):
    impact = alpha * order_size * volatility / liquidity
    return impact