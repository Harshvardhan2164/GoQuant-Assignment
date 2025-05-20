# GoQuant-Assignment

Model Documentation — This document explains the models, regression techniques, and performance optimizations used in the project, based directly on the codebase.

Model Selection and Parameters Component Model Type Parameters Used Fee Model Tiered percentage model Static fee rates: 0.10%, 0.07%, 0.05% Slippage Model Linear regression Trained using historical quantity/slippage Market Impact Simplified Almgren-Chriss Uses volatility, quantity, and time horizon

Slippage Model – Linear Regression Location: SlippageModel.cpp

Training Function:

cpp Copy Edit slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX); intercept = (sumY - slope * sumX) / n; This is standard Ordinary Least Squares (OLS) regression for predicting slippage based on quantity:

slippage(Q)=slope⋅Q+intercept Q: Order quantity

slope, intercept: Fitted using past trade data

Rationale:

Lightweight and interpretable

Fast computation for real-time simulation

Easy to retrain with new data

Fee Model – Tiered Structure Location: FeeModel.cpp
Code Logic:

switch (tier) { case FeeTier::Tier1: return amountUSD * 0.001; case FeeTier::Tier2: return amountUSD * 0.0007; case FeeTier::Tier3: return amountUSD * 0.0005; default: return amountUSD * 0.001; } Formula:

fee=amountUSD×tier_rate Where:

Tier 1 = 0.10%

Tier 2 = 0.07%

Tier 3 = 0.05%

This structure mimics real-world centralized exchange fees and allows easy modification for future rule-based logic.

Market Impact Model – Simplified Almgren-Chriss Location: MarketImpactModel.cpp
Formula Used:

return volatility * std::sqrt(quantity / timeHorizon); Mathematical Form:

slippage(Q)=slope⋅Q+intercept​

​

Where:

𝜎 σ: Market volatility (passed as parameter)

𝑄 Q: Order quantity

𝑇 T: Time horizon over which execution occurs

This simplified form of the Almgren-Chriss model estimates the temporary market impact of executing a trade. It reflects that larger and quicker trades result in higher impact.

Performance Optimization Approaches Your project is structured for low-latency real-time performance using several key strategies:
Memory Management Stack allocation in hot paths

Avoidance of unnecessary heap allocations

Use of std::vector with reserved capacity for model data

Network Communication Asynchronous WebSocket handling via ixwebsocket

Lightweight JSON parsing with nlohmann::json

Data Structure Selection std::vector chosen for efficient linear access

Minimal use of complex containers

Thread Management Background WebSocket thread

Processing loop decoupled from UI thread

Model Efficiency Slippage: Single multiply-add operation per prediction

Fees: Constant-time conditional lookup

Market Impact: One square root operation

Latency Benchmarking Goals Metric Target Latency Description Data processing latency < 5 ms From tick receipt to model output UI update latency < 10 ms ImGui + OpenGL redraw cycle Simulation loop latency < 15 ms Fee + Slippage + Impact combined