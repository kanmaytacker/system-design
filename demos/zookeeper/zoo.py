from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
import time

# Initialize Zookeeper client
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

def create_ephemeral_node(path, value):
    zk.create(path, value.encode('utf-8'), ephemeral=True)
    print(f"Ephemeral node {path} created with value: {value}")

def monitor_children(path):
    @zk.ChildrenWatch(path)
    def watch_children(children):
        print(f"Children of node {path} are now: {children}")

def node_died(path):
    @zk.DataWatch(path)
    def watch_node(data, stat):
        if stat is None:
            print(f"Node {path} died")
        else:
            print(f"Node {path} is alive with data: {data.decode('utf-8') if data else 'None'}")

def heartbeat_demo(path):
    def heartbeat():
        while True:
            if zk.exists(path):
                zk.set(path, b'heartbeat')
                print(f"Sent heartbeat to {path}")
            time.sleep(5)

    import threading
    heartbeat_thread = threading.Thread(target=heartbeat)
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

if __name__ == "__main__":
    root_path = "/demo"
    ephemeral_path = "/demo/ephemeral"
    initial_value = "hello"
    updated_value = "world"

    # Create root node
    zk.ensure_path(root_path)
    zk.set(root_path, initial_value.encode('utf-8'))
    print(f"Node {root_path} created with value: {initial_value}")

    # Monitor children of root node
    monitor_children(root_path)

    # Create an ephemeral node
    create_ephemeral_node(ephemeral_path, initial_value)

    # Monitor if ephemeral node dies
    node_died(ephemeral_path)

    # Heartbeat demo
    heartbeat_demo(root_path)

    # Create a child node to trigger the children watcher
    child_path = "/demo/child"
    zk.create(child_path, initial_value.encode('utf-8'))
    print(f"Child node {child_path} created with value: {initial_value}")

    # Wait to see the effects
    time.sleep(20)

    # Clean up
    zk.delete(child_path)
    zk.delete(ephemeral_path)
    zk.delete(root_path)

    # Stop the Zookeeper client
    zk.stop()
