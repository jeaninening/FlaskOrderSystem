import redis
import sys

import json
from utils import db
from utils.db import fetch_one
from concurrent.futures import ThreadPoolExecutor
import time
REDIS_CONN_PARAMS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'encoding': 'utf-8',
}
REDIS_POOL = redis.ConnectionPool(**REDIS_CONN_PARAMS)


def pop_queue():
    conn = redis.Redis(connection_pool=REDIS_POOL)
    data = conn.brpop('task_queue', timeout=5)
    print(data)

    if not data:
        return None
    return data[1].decode('utf-8')


def db_queue_init():
    """
    1.去数据库获取待执行的订单ID
    2.去redis中获取待执行的订单ID
    3.找到数据库中 且 redis队列中没有所有订单ID-> 重新放到redis的队列中
    :return:
    """
    # 1.去数据库获取待执行的订单ID
    db_list = db.fetch_all("select id from `order` where status = 1", [])
    db_id_list = {item['id'] for item in db_list}
    print("db_id_list:", db_id_list)

    # 2.redis中获取队列所有的ID
    conn = redis.Redis(connection_pool=REDIS_POOL)
    total_count = conn.llen('task_queue')
    print('total_count', total_count)
    cache_list = conn.lrange('task_queue', 0, total_count)
    cache_int_list = {int(item.decode('utf-8')) for item in cache_list}
    print(f"cache_list:{cache_int_list}")

    # 找到数据库中 且 redis队列中没有所有订单ID-> 重新放到redis的队列中
    need_push = db_id_list - cache_int_list
    if need_push:
        print(f"need_push:{need_push}", *need_push)
        conn.lpush('task_queue', *need_push)
        # *need_push 相当于将字典里每一个元素往队列放


def get_order_obj(order_id):
    res = db.fetch_one('select * from `order` where id = %s', [order_id])
    return res


def update_order(status, order_id):
    db.insert("update `order` set status = %s where id = %s", [status, order_id])
def task(info_dict):
    time.sleep(3)

def run():
    # 1.初始化数据库未在队列中的订单
    db_queue_init()
    while True:
        # 2.去队列中获取订单
        order_id = pop_queue()
        if not order_id:
            continue
        # # 3.订单是否存在
        # order_dict = get_order_obj(order_id)
        # if not order_dict:
        #     continue
        #
        # # 4.更新订单状态
        # update_order(2,order_id)
        #
        # # 5.执行订单
        # print('执行任务', order_dict)
        # thread_pool = ThreadPoolExecutor(max_workers=150)
        # for item in range(order_dict['count']):
        #     thread_pool.submit(task, order_dict)
        #
        # thread_pool.shutdown() #等订单都执行完成了再执行下面
        #
        # # 6.执行完成
        # update_order(3,order_id)


if __name__ == '__main__':
    run()
