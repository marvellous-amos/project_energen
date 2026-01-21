import json
import pandas as pd
import joblib

from sklearn.preprocessing import MinMaxScaler
from pmdarima import auto_arima
from joblib import dump
from project_energen.config import DATA_DIR, MODEL_DIR, TRAIN_START, TEST_START, SEASONAL_PERIOD

def main():
    # Load data
    energy_df = pd.read_csv(DATA_DIR/'energy.csv')
    energy_df['timestamp'] = pd.to_datetime(energy_df['timestamp'], dayfirst=True, errors='raise')
    energy_df = energy_df.set_index('timestamp')


    # Create training and testing datasets
    #two-month period from september 1 to October 31
    train_start_dt = TRAIN_START
    test_start_dt = TEST_START

    result = energy_df.loc[train_start_dt:, ["load"]].copy()

    result["train"] = result["load"].where(result.index < test_start_dt)
    result["test"]  = result["load"].where(result.index >= test_start_dt)

    result = result.drop(columns="load")

    train = energy_df.loc[
        (energy_df.index >= train_start_dt) &
        (energy_df.index < test_start_dt),
        "load"
    ]

    test = energy_df.loc[
        energy_df.index >= test_start_dt,
        "load"
    ]


    scaler = MinMaxScaler()

    train_scaled = scaler.fit_transform(
        train.values.reshape(-1, 1)
    ).flatten()

    test_scaled = scaler.transform(
        test.values.reshape(-1, 1)
    ).flatten()

    ## Implementing ARIMA

    HORIZON = 3
    print("Forecasting horizon:", HORIZON, "hours")

    model = auto_arima(
        train_scaled,
        seasonal=True,
        m=SEASONAL_PERIOD,
        stepwise=True,
        trace=True,
        suppress_warnings=True,
        error_action="ignore",
    )

    config = {
        "order": model.order,
        "seasonal_order": model.seasonal_order,
        "m": SEASONAL_PERIOD,
        "scaler": "MinMaxScaler",
        "train_Start": str(train.index.min()),
        "train_end": str(train.index.max()),
    }

    dump(scaler, f'{MODEL_DIR}/energen_scaler.joblib')
    dump(model, f'{MODEL_DIR}/energen_sarima_auto_model.joblib')
    with open(f"{MODEL_DIR}/energen_sarima_auto_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)



if __name__ == "__main__":
    main()
