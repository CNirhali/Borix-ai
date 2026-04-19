import time
import requests

try:
    print("Wait 15s...")
    time.sleep(15)
    print("Sending WhatsApp...")
    requests.post("http://localhost:8000/api/webhooks/whatsapp", data={"Body": "I want 2 cold coffees and a sandwich please", "From": "+1234567890"})
    
    print("Wait 8s...")
    time.sleep(8)
    print("Sending Telegram...")
    requests.post("http://localhost:8000/api/webhooks/telegram", json={"message": {"text": "Can I get 1 misal pav?", "chat": {"id": 123}}})
except Exception as e:
    print(f"Error: {e}")
