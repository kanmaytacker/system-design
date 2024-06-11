from kazoo.client import KazooClient
import time

# Initialize Zookeeper client
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

def create_node(path, value):
    if zk.exists(path):
        print(f"Node {path} already exists")
    else:
        zk.create(path, value.encode('utf-8'))
        print(f"Node {path} created with value: {value}")

def get_node_value(path):
    if zk.exists(path):
        value, _ = zk.get(path)
        print(f"Value of node {path}: {value.decode('utf-8')}")
    else:
        print(f"Node {path} does not exist")

def update_node_value(path, value):
    if zk.exists(path):
        zk.set(path, value.encode('utf-8'))
        print(f"Node {path} updated with value: {value}")
    else:
        print(f"Node {path} does not exist")

def delete_node(path):
    if zk.exists(path):
        zk.delete(path)
        print(f"Node {path} deleted")
    else:
        print(f"Node {path} does not exist")

def list_children(path):
    if zk.exists(path):
        children = zk.get_children(path)
        print(f"Children of node {path}: {children}")
    else:
        print(f"Node {path} does not exist")

if __name__ == "__main__":
    root_path = "/demo"
    child_path = "/demo/child"
    initial_value = "hello"
    updated_value = "world"

    # Create root node
    create_node(root_path, initial_value)

    # Create child node
    create_node(child_path, initial_value)

    # Get node values
    get_node_value(root_path)
    get_node_value(child_path)

    # Update node values
    update_node_value(root_path, updated_value)
    update_node_value(child_path, updated_value)

    # List children of root node
    list_children(root_path)

    # Delete child node
    delete_node(child_path)

    # Delete root node
    delete_node(root_path)

    # Stop the Zookeeper client
    zk.stop()
