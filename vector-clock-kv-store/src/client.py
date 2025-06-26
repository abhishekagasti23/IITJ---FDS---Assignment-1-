import requests
import time

# Explicit host port mappings
PORTS = {
    0: 5000,   # Node 0
    1: 5101,   # Node 1 (was 5001)
    2: 5102    # Node 2 (was 5002)
}

NUM_NODES = 3

def put_request(node_id, key, value):
    url = f"http://localhost:{PORTS[node_id]}/put"
    try:
        response = requests.post(url, json={"key": key, "value": value})
        print(f"[PUT] Node {node_id} | {key} = {value} | Response: {response.json()}")
    except Exception as e:
        print(f"Failed PUT on Node {node_id}: {e}")

def get_store(node_id):
    url = f"http://localhost:{PORTS[node_id]}/store"
    try:
        response = requests.get(url)
        data = response.json()
        print(f"\n[GET] Node {node_id} Store:")
        print(f"Store: {data['store']}")
        print(f"Vector Clock: {data['vector_clock']}")
        print(f"Buffer: {data['buffered']}\n")
    except Exception as e:
        print(f"Failed GET on Node {node_id}: {e}")

def scenario_demo():
    print(">>> Causal Consistency Test Demo")

    # Step 1: Node 0 writes x=apple
    put_request(0, "x", "apple")
    time.sleep(1)

    # Step 2: Node 1 reads then writes x=banana
    get_store(1)
    put_request(1, "x", "banana")
    time.sleep(1)

    # Step 3: Final check on all nodes
    for node in range(NUM_NODES):
        get_store(node)

if __name__ == "__main__":
    scenario_demo()
                                                                                                                                                                                                    