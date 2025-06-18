import random
import time
import os

# Feature options
protocols = ["tcp", "udp", "icmp"]
services = ["http", "ftp", "ssh", "dns"]
flags = ["SF", "S0", "REJ"]

# Make sure log directory exists
os.makedirs("logs", exist_ok=True)
log_path = "logs/access.log"

print("🚀 Log generator started... Writing to logs/access.log")

while True:
    # Core features
    src_bytes = random.randint(50, 5000)
    dst_bytes = random.randint(20, 3000)
    proto = random.choice(protocols)
    service = random.choice(services)
    flag = random.choice(flags)

    # Additional features needed for trained model
    duration = random.randint(0, 60)           # Random duration in seconds
    count = random.randint(1, 511)             # Number of connections to same host
    logged_in = random.choice([0, 1])          # Simulate login status

    # Construct log line: match model's feature order
    line = f"{src_bytes} {dst_bytes} {proto} {service} {flag} {duration} {count} {logged_in}\n"

    # Write log entry
    with open(log_path, "a") as f:
        f.write(line)

    print(f"📝 Written: {line.strip()}")
    time.sleep(2)

