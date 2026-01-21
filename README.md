# Energy Load Forecasting System (Local)

## Project Overview

This project implements a **classical time-series forecasting system** for predicting future electrical energy load using historical consumption data. It demonstrates an end-to-end workflow for **offline energy demand forecasting**, covering data preprocessing, exploratory analysis, model training, evaluation, and local forecasting.

Although the system can be run inside a Docker container, it is **not deployed to a cloud platform** and does not rely on managed services. Docker is used strictly for **environment reproducibility and local execution**.

---

## The Problem

Accurate electricity demand forecasting is fundamental to modern power systems. Utilities and grid operators rely on forecasts to ensure:

- Power grid stability and reliability
- Capacity planning and load balancing
- Reduced operational and generation costs
- Prevention of outages and energy waste

Poor forecasts can result in:

- Overproduction and wasted energy
- Grid instability during peak demand
- Increased operational and maintenance costs

---

## Objective

The objective of this project is to **forecast future electricity load** by learning temporal and seasonal patterns from historical observations.

The model answers the question:

> **“Given historical hourly electricity load data, what will the load be over the next forecast horizon?”**

---

## Dataset

- **Type:** Univariate time series
- **Granularity:** Hourly
- **Primary Variable:**
  - `load` — electricity demand
- **Time Index:**
  - `timestamp`

The dataset spans multiple years, allowing the model to capture:

- Daily seasonality
- Weekly consumption patterns
- Long-term trends

---

## Intended Use Case

This system is suitable for:

- Offline demand forecasting
- Batch-based scenario analysis
- Research and experimentation
- Learning classical time-series modeling

It is **not intended** for:

- Real-time prediction services
- Streaming ingestion pipelines
- Automated production deployment

---

## Model Choice: SARIMA (Seasonal ARIMA)

The project uses a **Seasonal ARIMA (SARIMA)** model, which is well-suited for energy load data with strong periodic behavior.

### Why SARIMA?

- Explicit modeling of seasonality (`m = 24` for hourly data)
- Strong statistical foundation
- High interpretability
- Widely used in energy forecasting

---

## Feature Engineering

This is a **pure univariate forecasting model**:

- No exogenous variables (e.g., weather, holidays)
- Forecasts depend only on historical load values
- Stationarity handled via differencing
- Seasonality handled explicitly by the SARIMA formulation

---

## Training Workflow

1. Load raw energy data
2. Parse and validate timestamps
3. Set timestamp as the time-series index
4. Split data into:
   - Training set
   - Temporal test set (future hold-out)
5. Fit SARIMA model on training data
6. Generate forecasts on the test period
7. Evaluate forecast accuracy
8. Persist trained model locally

---

## Project Structure

project_energen/
│
├── src/
│ └── project_energen/
│ ├── train.py # Model training and evaluation
│ ├── forecast.py # Forecasting logic
│ ├── api.py # Local inference API
│ ├── config.py # Centralized configuration
│ └── init.py
│
├── data/
│ └── energy.csv # Historical energy data
│
├── models/
│ └── # Trained SARIMA model
│
├── Dockerfile
├── requirements.txt
└── README.md

---

## Configuration

All configuration values are centralized in `config.py` to ensure clarity and reproducibility.

Key parameters include:

- `TRAIN_START` — training period start date
- `TEST_START` — evaluation period start date
- `SEASONAL_PERIOD = 24` — daily seasonality for hourly data
- `DATA_DIR` — data directory path
- `MODEL_DIR` — model persistence path

---

## Getting Started

### Prerequisites

- Python 3.11+
- pip or poetry
- pandas
- statsmodels
- matplotlib

### Clone the Repository

```bash
git clone <your-repo-url>
cd project_energen
```

**Install Dependencies**

```bash
pip install -r requirements.txt
```

**Train the Model**

```bash
python src/project_energen/train.py
```

**Output:**

- Trained SARIMA model saved to the models/ directory
- Forecast evaluation metrics printed to the console

## Running with Docker (Local)

Docker is provided to ensure consistent runtime environments across machines.

### Build the Docker Image

```bash
docker build -t energen-api .
```

### Run the Container

```bash
docker run -p 5000:5000 energen-api
```

This starts the local forecasting API at:

```arduino
http://localhost:5000
```

## API Usage (Local)

### Health Check

```bash
GET /health
```

### Forecast Endpoint

```bash
POST /predict
Content-Type: application/json
```

Example request:

```json
{
  "load": [2900, 2950, 3000, 3050],
  "horizon": 3
}
```

Example response:

```json
{
  "forecast": [3144.07, 3349.29, 3655.13],
  "horizon": 3,
  "model": "Auto-SARIMA (seasonal)"
}
```

## Forecasting with Newly Observed Loads (Rolling Updates)

### Concept

As new load observations become available:

1. Append them to the historical time series
2. Re-train the SARIMA model on the extended dataset
3. Generate updated forecasts

This mirrors real-world operational forecasting, where models are refreshed periodically as new data arrives.

### Important Note

SARIMA models do not support incremental learning.

Each update requires full re-training with the expanded dataset. This approach is appropriate for:

- Hourly or daily batch forecasting
- Offline workflows
- Research and analysis settings

## Model Evaluation

Evaluation is performed using a temporal hold-out test set to avoid data leakage.

Metrics used include:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

In addition to numerical metrics, visual inspection is used to assess:

- Seasonal pattern capture
- Bias or systematic error
- Under- or over-forecasting behavior

## Visualization

The project includes multiple visual diagnostics:

- Load distribution histograms
- Time-series plots
- Forecast vs. actual overlays

These visualizations are essential for:

- Model validation
- Debugging time-series behavior
- Communicating results to stakeholders

## Reproducibility

Reproducibility is a core design goal:

- Fixed training and test split dates
- Deterministic model configuration
- Explicit seasonal period definition
- Version-pinned dependencies

This ensures:

- Consistent results across runs
- Reliable model comparison
- Transparent experimentation

## Limitations

- No API or deployment layer
- Model retraining required for updates

## Future Improvements

Potential extensions include:

- Automated data ingestion from public energy APIs
- Batch or REST-based forecasting services

## Tech Stack

- pandas / numpy — data manipulation

- statsmodels — SARIMA modeling

- matplotlib — visualization

- Flask — local inference API

- Docker — environment reproducibility

- Python — core language

## Development Notes

Best practices applied throughout the project:

- Time-aware train/test splitting

- Explicit seasonality modeling

- Robust timestamp validation

- Modular, readable code structure

- Centralized configuration management

- Local reproducibility

## Deployment Status

🚫 Not deployed

This project is intentionally scoped for:

Docker is used only for local execution and reproducibility, not for production hosting.

## Summary

This project demonstrates a classical, statistically grounded approach to energy load forecasting using SARIMA. It prioritizes interpretability, correctness, and real-world time-series considerations over deployment complexity, making it well-suited for research, learning, and offline analytical workflows.
