from flask import Flask, request, jsonify
import pandas as pd
import joblib
import tensorflow as tf

app = Flask(__name__)

# Load saved files
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("features.pkl")
ann_model = tf.keras.models.load_model("ann_model.h5")


@app.route("/")
def home():
    return "Employee Attrition API Running Successfully"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    new_df = pd.DataFrame([data])

    # Encode
    new_df = pd.get_dummies(new_df)

    # Match training columns
    new_df = new_df.reindex(
        columns=feature_names,
        fill_value=0
    )

    # Scale
    new_scaled = scaler.transform(new_df)

    prediction = (
        ann_model.predict(new_scaled) > 0.5
    ).astype(int)[0][0]

    if prediction == 1:
        result = "High Attrition Risk"
    else:
        result = "Low Attrition Risk"

    return jsonify({
        "prediction": result
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)