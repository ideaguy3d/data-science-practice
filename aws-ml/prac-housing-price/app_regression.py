from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("housing_model.joblib")

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    # Expect: {"instances": [[feature_vector], ...]}
    instances = np.array(data.get("instances", []), dtype=float)
    preds = model.predict(instances).tolist()
    return jsonify(predictions=preds)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
