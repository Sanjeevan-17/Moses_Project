from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

app = Flask(__name__)
model = load("model.pkl")

@app.route('/')
def home():
    return "✅ Flask backend is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📥 Incoming data:", data)

        input_data = {'latitude': [data['latitude']], 'longitude': [data['longitude']]}

        for ct in ['Assault', 'Burglary', 'Drug Possession', 'Homicide', 'Theft']:
            input_data[f'crime_type_{ct}'] = [1 if data['crime_type'] == ct else 0]

        for tm in ['Afternoon', 'Evening', 'Morning', 'Night']:
            input_data[f'time_{tm}'] = [1 if data['time'] == tm else 0]

        for dy in ['Friday', 'Monday', 'Thursday', 'Tuesday', 'Wednesday']:
            input_data[f'day_{dy}'] = [1 if data['day'] == dy else 0]

        df = pd.DataFrame(input_data)
        print("📊 Model Input:\n", df)

        pred = model.predict(df)[0]
        prob = round(model.predict_proba(df)[0][pred] * 100, 2)

        return jsonify({"prediction": int(pred), "probability": prob})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
