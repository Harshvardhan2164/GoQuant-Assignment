# GoQuant-Assignment

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Component Details](#component-details)
5. [Technology Stack](#technology-stack)
6. [Setup and Installation](#setup-and-installation)
7. [Usage](#usage)
8. [Limitations and Future Work](#limitations-and-future-work)
9. [References](#references)

---

## Project Overview

This project implements a **real-time trade cost estimator and orderbook analyzer** for cryptocurrency futures trading on the OKX exchange. It connects to OKX's Level 2 orderbook WebSocket feed for the BTC-USDT-SWAP instrument and processes streaming data to estimate various components of trade cost:

* Slippage (linear or quantile regression-based)
* Trading Fees (tier-based)
* Market Impact (Almgren-Chriss model)
* Maker/Taker Proportions (logistic regression)
* Internal system latency measurement

The system provides actionable insights for traders aiming to optimize execution costs in a highly dynamic market environment.

---

## Features

* **WebSocket Client:** Connects securely to OKX's L2 orderbook WebSocket endpoint (`wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP`) with SSL/TLS support.
* **Real-time Orderbook Processing:** Parses incoming JSON orderbook snapshots, extracts bid/ask prices and volumes at multiple levels.
* **Slippage Estimation:** Computes expected slippage using linear or quantile regression models based on historical data and live orderbook states.
* **Fee Calculation:** Calculates trading fees based on user-selected fee tiers (maker/taker rates).
* **Market Impact Estimation:** Implements Almgren-Chriss framework to estimate market impact costs given trade size and market conditions.
* **Net Cost Calculation:** Aggregates slippage, fees, and market impact for total estimated trade cost.
* **Maker/Taker Proportion Estimation:** Uses logistic regression models to estimate the likelihood that a trade is maker or taker based on orderbook features.
* **Latency Measurement:** Measures internal processing latency with timestamping on each data tick to monitor system performance.

---

## Architecture

```
+-----------------------------------------------------+
|                   Frontend (Web UI)                 |
|    - Displays real-time trade cost estimates        |
|    - Provides input parameters for simulation       |
+-----------------------------^-----------------------+
                              |
                       WebSocket Stream (JSON)
                              |
+-----------------------------v-----------------------+
|                Backend Trade Estimator               |
|  - WebSocket Client (Boost Beast with SSL)           |
|  - JSON Orderbook Parser (Boost.JSON)                |
|  - Statistical Models: Linear Regression, Logistic   |
|    Regression, Almgren-Chriss Model                   |
|  - Trade Cost Calculation Module                      |
|  - Latency Measurement                                |
+-----------------------------------------------------+
```

---

## Component Details

### 1. Slippage Estimation

Uses linear or quantile regression trained on historical orderbook snapshots to estimate expected price slippage for a given trade size.
Training Function:

slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX); intercept = (sumY - slope * sumX) / n; This is standard Ordinary Least Squares (OLS) regression for predicting slippage based on quantity:

slippage(Q)=slope⋅Q+intercept 
Q: Order quantity

slope, intercept: Fitted using past trade data

Rationale:
* Lightweight and interpretable
* Fast computation for real-time simulation
* Easy to retrain with new data


### 2. Fee Calculation

Computes fees based on pre-configured fee tiers (maker and taker rates). The fee tiers can be user-selected or fetched from exchange parameters.
Code Logic:

switch (tier) { case FeeTier::Tier1: return amountUSD * 0.001; case FeeTier::Tier2: return amountUSD * 0.0007; case FeeTier::Tier3: return amountUSD * 0.0005; default: return amountUSD * 0.001; } Formula:

fee=amountUSD×tier_rate Where:

Tier 1 = 0.10%

Tier 2 = 0.07%

Tier 3 = 0.05%

This structure mimics real-world centralized exchange fees and allows easy modification for future rule-based logic.

### 3. Market Impact Estimation

Implements Almgren-Chriss market impact model considering trade size, volatility, and liquidity metrics derived from the orderbook.
Formula Used:

return volatility * std::sqrt(quantity / timeHorizon); Mathematical Form:

slippage(Q)=slope⋅Q+intercept​


Where:

𝜎: Market volatility (passed as parameter)

𝑄: Order quantity

𝑇: Time horizon over which execution occurs

This simplified form of the Almgren-Chriss model estimates the temporary market impact of executing a trade. It reflects that larger and quicker trades result in higher impact.

### 4. Net Cost Calculation

Aggregates all cost components (slippage + fees + market impact) for a final estimated cost figure.

### 5. Maker/Taker Proportion Calculation

Estimates the probability of a trade being maker or taker using logistic regression on features such as orderbook imbalance, spread, and recent trade activity.

### 6. Internal Latency Measurement

Records timestamps for each received tick and processing step to measure latency and ensure real-time performance.
Latency Benchmarking Goals Metric Target Latency Description Data processing latency < 5 ms From tick receipt to model output UI update latency < 10 ms ImGui + OpenGL redraw cycle Simulation loop latency < 15 ms Fee + Slippage + Impact combined

### 7. WebSocket Real-Time Data Streaming

Secure WebSocket client implementation connects to OKX’s L2 orderbook endpoint, receiving snapshots of bids and asks continuously and updating estimations accordingly.

---

## Technology Stack

* **C++17/20**: Core implementation language.
* **Boost Libraries**: Beast (WebSocket), ASIO (Networking), JSON (parsing), Regex, etc.
* **OpenSSL**: For TLS/SSL support on secure WebSocket connections.
* **Statistical Models**: Custom regression and logistic regression implemented or linked from C++ libraries.
* **Build Tools**: `g++`, `make` or CMake for build automation.

---

## Setup and Installation (C++)

1. **Prerequisites**:

   * Boost 1.75+ with Beast and JSON modules
   * OpenSSL development libraries
   * Modern C++ compiler (g++ 9+, clang 10+)
   * CMake 

2. **Build**:
    ```bash
   mkdir build
   cd build
   ```

   ```bash
   cmake ..
   make
   ```

3. **Run**:

   ```bash
   ./GoQuant
   ```

---

---

## Setup and Installation (Frontend)

1. **Prerequisites**:

   * Nodejs (LTS version)

2. **Run**:
    ```bash
   cd ui
   npm install
   ```

   ```bash
   npm run dev
   ```

---

---

## Check WebSocket Response

  ```bash
  g++ websocket2.cpp -o websocket2 -lboost_system -lssl -lcrypto -lpthread -lboost_json
  ./websocket2
  ```


---

## Usage

* Run the program, which connects to OKX's WebSocket endpoint and prints incoming orderbook snapshots.
* The program calculates slippage, fees, market impact, and net cost per tick in real-time.
* Modify input parameters or regression models inside the source code as needed.
* Integrate with a frontend via WebSocket or REST API to expose real-time analytics.

---

## Limitations and Future Work

* **Model Calibration:** Current regression models require offline training on historical data to improve accuracy.
* **Instrument Support:** Currently supports only BTC-USDT-SWAP; extend to other symbols and exchanges.
* **Error Handling:** Improve robustness against network disconnects and malformed data.
* **Frontend Integration:** Develop a dedicated frontend dashboard for live visualization and user interaction.
* **Latency Optimization:** Profile and optimize for ultra-low latency trading scenarios.

---

## References

* Almgren, R., & Chriss, N. (2000). Optimal execution of portfolio transactions.
* C++ Libraries — Beast, JSON, ASIO
* OKX API Documentation (WebSocket & REST)

---
