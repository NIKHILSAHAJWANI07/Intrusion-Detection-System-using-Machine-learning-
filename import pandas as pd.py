import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample training data
df = pd.read_csv("dataset/sample_log_dataset.csv")  # Use real data if available
X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to model.pkl")
