from flask import Flask, request, jsonify
from waitress import serve
from src.project_energen.predict import predict

app = Flask("energy-forecast-api")


@app.route("/predict", methods=["POST"])
def forecast():
    try:
        payload = request.get_json()

        if payload is None:
            return jsonify({"error": "Invalid or empty JSON payload"}), 400

        if "load" not in payload:
            return jsonify({"error": "Missing required field: load"}), 400

        load_history = payload["load"]
        horizon = payload.get("horizon", 3)

        if not isinstance(load_history, list) or len(load_history) < 2:
            return jsonify({"error": "load must be a list with at least 2 values"}), 400

        predictions = predict(load_history, horizon)

        return jsonify({
            "forecast": predictions,
            "horizon": horizon,
            "model": "Auto-SARIMA (seasonal)",
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "energy-load-forecasting",
        "version": "1.0.0"
    })


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Energy Load Forecasting API",
        "endpoints": {
            "POST /predict": "Generate load forecast",
            "GET /health": "Health check"
        },
        "example_request": {
            "load": [2900, 2950, 3000, 3050],
            "horizon": 3
        }
    })


if __name__ == "__main__":
    print("Starting Energy Forecast API on port 5000...")
    serve(app, host="0.0.0.0", port=5000)
