import redis

REDIS_CONN_PARAMS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'encoding': 'utf-8',
}
REDIS_POOL = redis.ConnectionPool(**REDIS_CONN_PARAMS)

def push_queue(value):
    conn = redis.Redis(connection_pool=REDIS_POOL)
    conn.lpush('task_queue',value)