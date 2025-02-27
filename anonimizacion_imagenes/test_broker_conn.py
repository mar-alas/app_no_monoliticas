import socket
import os

host=os.getenv("BROKER_HOST","localhost")
port = 6650

try:
    with socket.create_connection((host, port), timeout=5):
        print("✅ Pulsar broker is reachable")
except Exception as e:
    print(f"❌ Broker unreachable: {e}")