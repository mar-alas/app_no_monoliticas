import pulsar
import os

# Define your broker URL
broker_host=os.getenv("BROKER_HOST","localhost")
broker_url = f"pulsar://{broker_host}:6650"  # Modify if needed

try:
    # Attempt to create a Pulsar client
    client = pulsar.Client(broker_url)
    
    # Try creating a producer on a test topic (this verifies the connection)
    producer = client.create_producer("persistent://public/default/test-topic")

    print("✅ Pulsar connection successful!")

    # Cleanup: Close producer and client
    producer.close()
    client.close()

except Exception as e:
    print(f"❌ Failed to connect to Pulsar: {e}")
