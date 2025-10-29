from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

app = Flask(__name__)

# Load model
try:
    model = load("model.pkl")
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Failed to load model:", e)
    model = None

@app.route('/')
def home():
    return "✅ Flask backend is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📥 Incoming request data:", data)

        if not data:
            return jsonify({"error": "Missing JSON data"}), 400

        # Validate keys
        required_keys = ['latitude', 'longitude', 'crime_type', 'time', 'day']
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing field: {key}"}), 400

        input_data = {
            'latitude': [data['latitude']],
            'longitude': [data['longitude']]
        }

        # One-hot encode crime_type
        for ct in ['Assault', 'Burglary', 'Drug Possession', 'Homicide', 'Theft']:
            input_data[f'crime_type_{ct}'] = [1 if data['crime_type'] == ct else 0]

        # One-hot encode time
        for tm in ['Afternoon', 'Evening', 'Morning', 'Night']:
            input_data[f'time_{tm}'] = [1 if data['time'] == tm else 0]

        # One-hot encode day (based on model training)
        for dy in ['Friday', 'Monday', 'Thursday', 'Tuesday', 'Wednesday']:
            input_data[f'day_{dy}'] = [1 if data['day'] == dy else 0]

        df = pd.DataFrame(input_data)
        print("📊 Model Input DataFrame:\n", df)

        # Prediction
        pred = model.predict(df)[0]
        prob = round(model.predict_proba(df)[0][pred] * 100, 2)

        print(f"✅ Prediction: {pred}, Probability: {prob}%")
        return jsonify({"prediction": int(pred), "probability": prob})

    except Exception as e:
        print("❌ Error during prediction:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
