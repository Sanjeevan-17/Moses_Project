import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# Sample training data
data = {
    "crime_type": ["Theft", "Assault", "Burglary", "Homicide", "Drug Possession"] * 20,
    "time": ["Morning", "Afternoon", "Evening", "Night"] * 25,
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] * 20,
    "latitude": [12.97, 13.02, 12.91, 13.05, 12.99] * 20,
    "longitude": [77.59, 77.60, 77.55, 77.61, 77.58] * 20,
    "label": [1, 0, 1, 1, 0] * 20
}

df = pd.DataFrame(data)
df_encoded = pd.get_dummies(df, columns=["crime_type", "time", "day"])
X = df_encoded.drop("label", axis=1)
y = df_encoded["label"]

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
dump(model, "model.pkl")
print("✅ Model saved as model.pkl")
