import time
import pickle
import os
import sys
import pandas as pd  # <- added

# Set up correct path for model.pkl
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "model.pkl")

# Load trained model
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Consistent mappings (must match training)
protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
service_map = {"http": 0, "ftp": 1, "ssh": 2, "dns": 3}
flag_map = {"SF": 0, "S0": 1, "REJ": 2}

# Parse one log line into feature vector
def parse_log_line(line, protocol_map, service_map, flag_map):
    try:
        parts = line.strip().split()
        if len(parts) != 5:
            return None

        src_bytes = int(parts[0])
        dst_bytes = int(parts[1])
        proto = protocol_map.get(parts[2], 3)
        service = service_map.get(parts[3], len(service_map))
        flag = flag_map.get(parts[4], len(flag_map))

        bytes_ratio = src_bytes / (dst_bytes + 1)
        packet_size_diff = abs(src_bytes - dst_bytes)

        return [src_bytes, dst_bytes, proto, service, flag, bytes_ratio, packet_size_diff]
    except Exception as e:
        print(f"Error parsing line: {line.strip()} | {e}")
        return None

# Main monitoring function
def monitor_logs(log_path="logs/access.log"):
    print("Monitoring logs with model features:", model.feature_names_in_)
    with open(log_path, "r") as f:
        f.seek(0, 2)  # Move to end of file

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            data = parse_log_line(line, protocol_map, service_map, flag_map)
            if data:
                try:
                    # Convert list to DataFrame with correct column names to avoid warning
                    df = pd.DataFrame([data], columns=model.feature_names_in_)
                    pred = model.predict(df)[0]
                    label = "[ATTACK]" if pred == 1 else "[NORMAL]"
                    print(f"{label} | Log: {line.strip()}")
                except Exception as e:
                    print(f"Prediction error: {e}")

# Run
if __name__ == "__main__":
    monitor_logs()
