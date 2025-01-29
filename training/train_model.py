import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMClassifier
import joblib

#Loading cleaned dataset
file_path = "data/cleaned_creditcard.csv"
df = pd.read_csv(file_path)


# Split into features (X) and target (y)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train LightGBM model
model = LGBMClassifier(n_estimators=200, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump(model, "models/model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("✅ LightGBM Model Trained and Saved!")
