import pandas as pd
import numpy as np
from joblib import load

MODEL_PATH = "models/energen_sarima_auto_model.joblib"
SCALER_PATH = "models/energen_scaler.joblib"

model = load(MODEL_PATH)
scaler = load(SCALER_PATH)


def predict(load_series, horizon=3):
    """
    Predict energy load using pre-trained SARIMA and MinMaxScaler.

    Args:
        load_series (list or np.array): Historical load values (original scale)
        horizon (int): Number of future steps to forecast

    Returns:
        list: Forecasted load values in original scale
    """

    # Scale input
    load_df = pd.DataFrame(load_series, columns=['load'])
    load_scaled = scaler.transform(load_df)

    # Update model with new data
    model.update(load_scaled)

    # Forecast in scaled space
    forecast_scaled = model.predict(n_periods=horizon)
    # Inverse transform forecast
    forecast = scaler.inverse_transform(forecast_scaled.reshape(-1, 1)).ravel()

    return forecast.tolist()