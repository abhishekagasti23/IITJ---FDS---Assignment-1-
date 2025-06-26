import requests
import time

for i in range(20):
    try:
        res = requests.post("http://localhost:5000/request_charge")
        print(f"{i+1}: {res.text.strip()}")
    except Exception as e:
        print(f"Request {i+1} failed: {e}")
    time.sleep(0.5)
