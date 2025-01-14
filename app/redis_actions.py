import os
import redis

# Get Redis configuration from environment variables
redis_host = os.getenv('REDISHOST', 'localhost')
redis_port = int(os.getenv('REDISPORT', 6379))

# Initialize Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

print(f"Connected to Redis at {redis_host}:{redis_port}")

def sync_to_redis(key, value):
    """
    Sync a key-value pair to Redis.
    """
    try:
        redis_client.set(key, value)
        print(f"Synced {key} to Redis.")
    except Exception as e:
        print(f"Error syncing {key} to Redis: {e}")

def get_from_redis(key):
    """
    Retrieve a value from Redis by key.
    """
    try:
        value = redis_client.get(key)
        print(f"Retrieved {key} from Redis: {value}")
        return value
    except Exception as e:
        print(f"Error retrieving {key} from Redis: {e}")
        return None

# Example usage:
# sync_to_redis('example_key', 'example_value')
# retrieved_value = get_from_redis('example_key')
