from dbutils.pooled_db import PooledDB #进程池
import pymysql
from pymysql.cursors import DictCursor

POOL = PooledDB(
    creator=pymysql, #使用连接数据库的模块
    maxconnections=10, #连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,#初始化时，连接池中至少创建的空闲的连接，0表示不创建
    maxcached=3, #连接池中最多空闲的连接，0和None表示不限制
    blocking=True,#连接池中如果没有可用连接后，是否阻塞等待。True：等待，False：不等待然后报错
    setsession=[], #开始会话前执行的命令列表，如：["set datestyle to ...","set time zone"]
    ping = 0,
    host='localhost', port=3306, user='root', password='123456', db='v5', charset='utf8'
)
#获取sql匹配成功的第一条数据
def fetch_one(sql,params):
    conn = POOL.connection()
    # cursor=DictCursor 返回值才会是字典的格式
    cursor = conn.cursor(cursor=DictCursor)
    cursor.execute(sql, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close() # 将此连接交还给连接池
    return result

#获取sql匹配成功的所有数据
def fetch_all(sql,params):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=DictCursor)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def insert(sql,params):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=DictCursor)
    cursor.execute(sql, params) #操作 增删改查
    conn.commit() #确认操作
    cursor.close()
    conn.close()
    return cursor.lastrowid #返回新生成数据的id