from flask import Flask
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading

app = Flask(__name__)
current_load = Gauge('current_load', 'Current load on the substation')

@app.route('/charge', methods=['POST'])
def charge():
    current_load.inc()
    threading.Timer(5.0, current_load.dec).start()  # Simulate 5-second charge
    return 'Charging started\n'

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
