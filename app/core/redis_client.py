import argparse
import json

import redis

redis_client = redis.Redis(host='localhost', port=6379, db=5)
redis_pubsub = redis_client.pubsub()