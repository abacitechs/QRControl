import redis
from flask import Flask

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"  # Update with your Redis connection details

redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])
