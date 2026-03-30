import redis

REDIS_CONN_PARAMS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'encoding': 'utf-8',
}
REDIS_POOL = redis.ConnectionPool(**REDIS_CONN_PARAMS)

#方式一：一次全部取出
"""
conn = redis.Redis(connection_pool=REDIS_POOL)
total_count = conn.llen('task_queue')
res = conn.lrange('task_queue', 0, total_count)
print(res)

"""
#方式二：逐个获取

"""
conn = redis.Redis(connection_pool=REDIS_CONN_PARAMS)
total_count = conn.llen('task_queue')
for index in range(total_count):
    ele = conn.lindex('task_queue', index)
    print(ele)
"""

#方式三：一次取一部分 为什么这么做，redis中没有为列表提供一次只取一部分的功能，像hscan_iter

"""
conn = redis.Redis(connection_pool=REDIS_POOL)
total_count = conn.llen('task_queue')
has_fetch_count = 0
while has_fetch_count < total_count:
    ele_list = conn.lrange('task_queue', 0, has_fetch_count+3)
    has_fetch_count += len(ele_list)
    print(ele_list)
"""


