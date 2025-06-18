import pandas as pd
import numpy as np
import os

os.makedirs("dataset", exist_ok=True)

data = {
    "src_bytes": np.random.randint(0, 5000, 500),
    "dst_bytes": np.random.randint(0, 5000, 500),
    "protocol_type": np.random.choice(["tcp", "udp", "icmp"], 500),
    "service": np.random.choice(["http", "ftp", "ssh", "dns"], 500),
    "flag": np.random.choice(["SF", "S0", "REJ"], 500),
    "label": np.random.choice([0, 1], 500)
}

df = pd.DataFrame(data)

df["protocol_type"] = df["protocol_type"].astype("category").cat.codes
df["service"] = df["service"].astype("category").cat.codes
df["flag"] = df["flag"].astype("category").cat.codes

df.to_csv("dataset/sample_log_dataset.csv", index=False)

print("✅ Dataset created: dataset/sample_log_dataset.csv")
