from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import joblib

app = Flask(__name__)

# Load the model and scaler
model = tf.keras.models.load_model('stress_detection_model.keras')
scaler = joblib.load('scaler.joblib')

features = ['MEAN_RR', 'RMSSD', 'pNN25', 'pNN50', 'LF', 'HF', 'LF_HF']

def predict_stress(data):
    scaled_data = scaler.transform(data.reshape(1, -1))
    prediction = model.predict(scaled_data)
    return np.argmax(prediction, axis=1)[0]

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_data = np.array([float(data[feature]) for feature in features])
    prediction = predict_stress(input_data)
    
    stress_levels = ["No Stress", "Low Stress", "High Stress"]
    result = stress_levels[prediction]
    
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
