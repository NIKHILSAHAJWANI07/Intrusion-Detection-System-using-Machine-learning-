import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def load_kdd_data():
    # Column names from the KDD documentation
    cols = ["duration", "protocol_type", "service", "flag", "src_bytes",
            "dst_bytes", "land", "wrong_fragment", "urgent", "hot", 
            "num_failed_logins", "logged_in", "num_compromised", "root_shell",
            "su_attempted", "num_root", "num_file_creations", "num_shells",
            "num_access_files", "num_outbound_cmds", "is_host_login",
            "is_guest_login", "count", "srv_count", "serror_rate",
            "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
            "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
            "dst_host_srv_count", "dst_host_same_srv_rate",
            "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
            "dst_host_srv_serror_rate", "dst_host_rerror_rate",
            "dst_host_srv_rerror_rate", "label"]
    
    df = pd.read_csv("dataset/kddcup.data_10_percent.csv", names=cols)
    
    # Convert attack labels to binary (1=attack, 0=normal)
    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal.' else 1)
    
    # Select key features (you can expand this later)
    features = ["duration", "protocol_type", "service", "flag", 
                "src_bytes", "dst_bytes", "logged_in", "count"]
    
    return df[features + ['label']]

def load_sample_data():
    df = pd.read_csv("dataset/sample_log_dataset.csv")
    # Ensure consistent binary labels
    df['label'] = df['label'].astype(int)
    return df

# Load and combine datasets
try:
    print("Loading KDD dataset...")
    df = load_kdd_data()
except FileNotFoundError:
    print("KDD dataset not found, using sample data")
    df = load_sample_data()

# Data Analysis
print("\n=== Data Summary ===")
print(df.describe())
print("\n=== Label Distribution ===")
print(df['label'].value_counts(normalize=True))

# Preprocessing
protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
service_map = {service: i for i, service in enumerate(df['service'].unique())}
flag_map = {flag: i for i, flag in enumerate(df['flag'].unique())}

df['protocol_type'] = df['protocol_type'].map(protocol_map).fillna(3)
df['service'] = df['service'].map(service_map).fillna(len(service_map))
df['flag'] = df['flag'].map(flag_map).fillna(len(flag_map))

# Feature Engineering
df['bytes_ratio'] = df['src_bytes'] / (df['dst_bytes'] + 1)  # +1 to avoid division by zero
df['packet_size_diff'] = abs(df['src_bytes'] - df['dst_bytes'])

# Train/test split
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(
    n_estimators=300,           # Increased from 200
    max_depth=12,               # Reduced from 15 to prevent overfitting
    min_samples_split=5,        # New parameter
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Save model with feature names
model.feature_names_in_ = X.columns.tolist()
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print("\n=== Model Evaluation ===")
print(f"Model trained on {len(df)} samples")
print(f"Attack samples: {y.sum()}, Normal samples: {len(y)-y.sum()}")
print(f"Train Accuracy: {train_score:.4f}")
print(f"Test Accuracy: {test_score:.4f}")

# Feature Importance
try:
    importances = model.feature_importances_
    feature_names = X.columns
    print("\n=== Top 10 Features ===")
    for feat, imp in sorted(zip(feature_names, importances), 
                          key=lambda x: x[1], reverse=True)[:10]:
        print(f"{feat}: {imp:.4f}")
except Exception as e:
    print(f"\nFeature importance error: {str(e)}")