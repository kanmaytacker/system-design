import json
import sys
import uuid

from typing import Union, List

from redis import Redis
from redis.cluster import ClusterNode, RedisCluster

import seaborn as sns

sns.set_style("white")

from matplotlib import pyplot as plt

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6379
PORT_PREFIX = 700

MAX_MEMORY_OFFSET = (2 * 1024 * 1024) + 1024 * 512
EVICTION_POLICY = "allkeys-random"

# Ranges
INITIAL_RANGE = 5000
INITIAL_READ_RANGE = 1000
FLOOD_RANGE = 10000


def create_cluster() -> RedisCluster:
    nodes = list(
        map(
            lambda index: ClusterNode(
                host=DEFAULT_HOST,
                port=f"{PORT_PREFIX}{index}",
            ),
            range(0, 5),
        )
    )
    cluster = RedisCluster(startup_nodes=nodes)
    return with_configs(cluster)


def create_standalone() -> Redis:
    instance = Redis(host=DEFAULT_HOST, port=DEFAULT_PORT)
    return with_configs(instance)


def with_configs(instance: Union[Redis, RedisCluster]) -> Union[Redis, RedisCluster]:
    # Offset current memory by max memory offset
    instance.config_set("maxmemory", MAX_MEMORY_OFFSET)
    instance.config_set("maxmemory-policy", EVICTION_POLICY)
    if EVICTION_POLICY == "allkeys-lru":
        instance.config_set("maxmemory-samples", 5)

    assert instance.config_get("maxmemory-policy") == {
        "maxmemory-policy": EVICTION_POLICY
    }
    return instance


def handle_cluster(cluster: RedisCluster):

    # Check that the cluster is empty. Else, flush it.
    cluster.flushall()
    print(f"Cluster has {cluster.dbsize()} keys")

    print(
        f"Redis cluster is running on ports {list(map(lambda node: node.port, cluster.get_nodes()))}"
    )
    print_info(cluster)

    store_constants(cluster)

    # Fetch the node that holds the constant-1 key
    node = cluster.get_node_from_key("constant-1")
    print(f"Constant 1 is stored in node {node.name} on port {node.port}")

    # Fetch the node that holds the constant-2 key
    node = cluster.get_node_from_key("constant-2")

    print(f"Constant 2 is stored in node {node.name} on port {node.port}")

    store_loop(cluster)

    # Fetch the node that holds the loop-0 key
    node = cluster.get_node_from_key("loop-0")
    print(f"Loop 0 is stored in node {node.name} on port {node.port}")

    read_data(cluster)


def handle_standalone(redis: Redis):

    redis.flushall()
    print(f"Node has {redis.dbsize()} keys")

    print(f"Redis is running on port {redis.connection_pool.connection_kwargs['port']}")
    print_info(redis)

    store_constants(redis)
    store_loop(redis, end=INITIAL_RANGE)

    read_data(redis, end=INITIAL_READ_RANGE)

    store_loop(redis, end=FLOOD_RANGE, start=INITIAL_RANGE)

    read_data(redis, end=INITIAL_READ_RANGE)

    evicted = read_data(redis, end=FLOOD_RANGE)
    print(f"Total evicted keys: {len(evicted)}")

    # Plot the distribution of evicted keys
    sns.displot(evicted, bins=200, kde=True)

    plt.xticks(range(0, FLOOD_RANGE, 1000))
    plt.title("Distribution of evicted keys over ranges")
    plt.xlabel("Range")
    plt.ylabel("Number of evicted keys")
    plt.show()


def print_info(node: Union[Redis, RedisCluster]):
    print(f"Used memory: {node.info()['used_memory_human']}")
    print(f"Max memory: {node.info()['maxmemory_human']}")
    print(
        "Eviction policy: ",
        node.config_get("maxmemory-policy")["maxmemory-policy"],
    )


def store_constants(node: Union[Redis, RedisCluster]):

    node.set("constant-1", "value-1")
    node.set("constant-2", "value-2")

    print(f"Stored constants: {node.keys()}")
    print(f"Constant 1: {node.get('constant-1')}")
    assert node.get("constant-1") == b"value-1"

    print(f"Constant 2: {node.get('constant-2')}")
    assert node.get("constant-2") == b"value-2"


def store_loop(node: Union[Redis, RedisCluster], end: int, start: int = 0):

    for i in range(start, end):
        try:
            node.set(loop_key(i), str(uuid.uuid4()))
        except Exception as e:
            # Check if the error is due to eviction
            if "OOM" in str(e):
                print(f"Last key: {loop_key(i)}")
            break

    print(f"Node has {node.dbsize()} keys")
    print(f"Memory used: {node.info()['used_memory_human']}")


def read_data(node: Union[Redis, RedisCluster], end: int, start: int = 0) -> List[int]:

    evicted = []
    for i in range(start, end):
        if node.get(loop_key(i)):
            continue

        evicted.append(i)

    print(f"Total evicted keys: {len(evicted)}")
    print(f"Evicted keys: {evicted[:5]}")

    return evicted


def loop_key(i: int) -> str:
    return f"loop-{i}"


if __name__ == "__main__":

    # Check args for mode (standalone or cluster)
    mode = sys.argv[1] if len(sys.argv) > 1 else "standalone"

    if mode == "cluster":
        handle_cluster(create_cluster())
    elif mode == "standalone":
        handle_standalone(create_standalone())
