from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load
import pandas as pd

app = Flask(__name__)
CORS(app)

model = load("model.pkl")

@app.route('/')
def home():
    return "✅ Flask backend is running!"

@app.route('/predict', methods=['POST'])
def predict():

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()

    input_data = {
        'latitude':[data['latitude']],
        'longitude':[data['longitude']]
    }

    for ct in ['Assault','Burglary','Drug Possession','Homicide','Theft']:
        input_data[f'crime_type_{ct}'] = [1 if data['crime_type']==ct else 0]

    for tm in ['Afternoon','Evening','Morning','Night']:
        input_data[f'time_{tm}'] = [1 if data['time']==tm else 0]

    for dy in ['Friday','Monday','Thursday','Tuesday','Wednesday']:
        input_data[f'day_{dy}'] = [1 if data['day']==dy else 0]

    df = pd.DataFrame(input_data)

    expected_columns = [
        'latitude','longitude',
        'crime_type_Assault','crime_type_Burglary','crime_type_Drug Possession',
        'crime_type_Homicide','crime_type_Theft',
        'time_Afternoon','time_Evening','time_Morning','time_Night',
        'day_Friday','day_Monday','day_Thursday','day_Tuesday','day_Wednesday'
    ]

    df = df[expected_columns]

    pred = model.predict(df)[0]
    prob = round(model.predict_proba(df)[0][pred]*100,2)

    return jsonify({"prediction":int(pred),"probability":prob})

if __name__ == '__main__':
    app.run(debug=True)
