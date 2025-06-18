import time
import random

attacks = [
    "100 200 tcp http SF",       # Normal
    "9999 0 udp dns REJ",        # DDoS
    "50 5000 tcp ssh S0",        # Port scan
    "0 0 icmp - -"               # Ping flood
]

print("Simulating attacks... Press Ctrl+C to stop")
try:
    while True:
        with open("logs/access.log", "a") as f:
            line = random.choice(attacks)
            f.write(line + "\n")
            print(f"Added: {line}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation stopped")