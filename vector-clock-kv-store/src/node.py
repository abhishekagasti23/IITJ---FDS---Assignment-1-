import os
import json
import time
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- Config ---
NODE_ID = int(os.environ.get("NODE_ID", 0))
NUM_NODES = int(os.environ.get("NUM_NODES", 3))

# --- Data ---
vector_clock = [0] * NUM_NODES
store = {}
buffer = []

peer_ports = [5000 + i for i in range(NUM_NODES)]
peer_urls = [f"http://node{i}:5000/replicate" for i in range(NUM_NODES) if i != NODE_ID]

# --- Causal Check ---
def is_causally_ready(msg_clock):
    for i in range(NUM_NODES):
        if i == msg_clock["sender"]:
            if msg_clock["clock"][i] != vector_clock[i] + 1:
                return False
        else:
            if msg_clock["clock"][i] > vector_clock[i]:
                return False
    return True

def apply_message(msg):
    key = msg["key"]
    value = msg["value"]
    clock = msg["clock"]
    store[key] = value
    for i in range(NUM_NODES):
        vector_clock[i] = max(vector_clock[i], clock[i])

@app.route("/put", methods=["POST"])
def put():
    data = request.get_json()
    key = data["key"]
    value = data["value"]
    vector_clock[NODE_ID] += 1
    store[key] = value

    message = {
        "key": key,
        "value": value,
        "sender": NODE_ID,
        "clock": vector_clock.copy()
    }

    for url in peer_urls:
        try:
            requests.post(url, json=message)
        except Exception as e:
            print(f"Replication to {url} failed: {e}")

    return jsonify({"status": "stored", "vector_clock": vector_clock}), 200

@app.route("/replicate", methods=["POST"])
def replicate():
    msg = request.get_json()
    if is_causally_ready(msg):
        apply_message(msg)
        flush_buffer()
        return jsonify({"status": "applied"}), 200
    else:
        buffer.append(msg)
        return jsonify({"status": "buffered"}), 202

def flush_buffer():
    ready = [msg for msg in buffer if is_causally_ready(msg)]
    for msg in ready:
        apply_message(msg)
        buffer.remove(msg)

@app.route("/store", methods=["GET"])
def get_store():
    return jsonify({
        "store": store,
        "vector_clock": vector_clock,
        "buffered": buffer
    })

@app.route("/")
def health():
    return f"Node {NODE_ID} is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
