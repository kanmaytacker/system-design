import redis
from localstack_client.session import Session
import time

# Initialize a session using LocalStack
session = Session()

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def redis_set_key_with_ttl(key, value, ttl):
    redis_client.set(key, value, ex=ttl)
    print(f"Set key '{key}' with TTL {ttl} seconds in Redis")

def redis_get_key(key):
    value = redis_client.get(key)
    if value:
        print(f"Retrieved from Redis: {value.decode('utf-8')}")
    else:
        print(f"Key '{key}' not found in Redis")

def redis_list_operations(list_name, values):
    for value in values:
        redis_client.lpush(list_name, value)
    print(f"Added values {values} to list '{list_name}'")
    
    length = redis_client.llen(list_name)
    elements = redis_client.lrange(list_name, 0, -1)
    print(f"List '{list_name}' has {length} elements: {elements}")

def redis_set_operations(set_name, values):
    for value in values:
        redis_client.sadd(set_name, value)
    print(f"Added values {values} to set '{set_name}'")
    
    members = redis_client.smembers(set_name)
    print(f"Set '{set_name}' has members: {members}")

def redis_hash_operations(hash_name, key_value_pairs):
    for key, value in key_value_pairs.items():
        redis_client.hset(hash_name, key, value)
    print(f"Added key-value pairs {key_value_pairs} to hash '{hash_name}'")
    
    keys = redis_client.hkeys(hash_name)
    all_pairs = redis_client.hgetall(hash_name)
    print(f"Hash '{hash_name}' has keys: {keys} and pairs: {all_pairs}")

def redis_transactions():
    with redis_client.pipeline() as pipe:
        try:
            pipe.multi()
            pipe.set('trans_key1', 'value1')
            pipe.set('trans_key2', 'value2')
            responses = pipe.execute()
            print(f"Transaction responses: {responses}")
        except redis.exceptions.RedisError as e:
            print(f"Transaction failed: {e}")

def redis_lru_eviction_demo():
    # Set keys until memory limit is reached to trigger LRU eviction
    for i in range(1000):
        redis_client.set(f'key{i}', f'value{i}')
        print(f"Set key{i}")
        if i % 100 == 0:
            time.sleep(0.1)  # Brief pause to avoid overwhelming the server

    # Retrieve some keys to verify LRU eviction
    for i in range(1000):
        value = redis_client.get(f'key{i}')
        if value:
            print(f"Retrieved key{i}: {value.decode('utf-8')}")
        else:
            print(f"Key key{i} was evicted")

if __name__ == "__main__":
    # Set and get key with TTL
    redis_set_key_with_ttl('tempkey', 'This is a temporary key', 5)
    redis_get_key('tempkey')
    
    print(),

    # Wait to ensure TTL expiration
    time.sleep(6)
    redis_get_key('tempkey')

    print(),
    # List operations
    redis_list_operations('mylist', ['value1', 'value2', 'value3'])

    print(),
    # Set operations
    redis_set_operations('myset', ['value1', 'value2', 'value3'])

    print(),
    # Hash operations
    redis_hash_operations('myhash', {'key1': 'value1', 'key2': 'value2'})

    print(),
    # Transaction operations
    redis_transactions()
    
    print(),
    redis_lru_eviction_demo()

