import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump

# Create dataset
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

dump(model, "model.pkl")
print("✅ Model trained and saved as model.pkl")
