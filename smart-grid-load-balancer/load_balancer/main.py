from flask import Flask
import requests
import re

app = Flask(__name__)
SUBSTATIONS = ['substation1:5001', 'substation2:5001']

def get_load(substation):
    try:
        response = requests.get(f'http://{substation}/metrics')
        match = re.search(r'current_load\s+(\d+)', response.text)
        return int(match.group(1)) if match else float('inf')
    except:
        return float('inf')

@app.route('/dispatch', methods=['POST'])
def dispatch():
    loads = {sub: get_load(sub) for sub in SUBSTATIONS}
    best = min(loads, key=loads.get)
    res = requests.post(f'http://{best}/charge')
    return f'Routed to {best}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
