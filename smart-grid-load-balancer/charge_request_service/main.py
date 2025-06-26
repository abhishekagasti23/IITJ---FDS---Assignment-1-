from flask import Flask, request
import requests

app = Flask(__name__)
LOAD_BALANCER_URL = 'http://load_balancer:5002'

@app.route('/request_charge', methods=['POST'])
def request_charge():
    res = requests.post(f'{LOAD_BALANCER_URL}/dispatch')
    return res.text, res.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                            