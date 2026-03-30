from flask import Blueprint, session, redirect, render_template, request,jsonify
from utils import db
from utils import cache

od = Blueprint("order", __name__)  # 蓝图对象

status_dict = {
    1: ['待执行', 'text-bg-secondary'],
    2: ['正在执行', 'text-bg-warning'],
    3: ['完成', 'text-bg-success'],
    4: ['失败', 'text-bg-danger']
}

@od.route("/order/list")
def order_list():
    user_info = session.get('user_info')
    role = user_info['role']
    real_name = user_info['real_name']
    if role == 2:
        # data_list= db.fetch_all("select * from order",[])
        data_list = db.fetch_all("select * from `order` left join userinfo on `order`.user_id = userinfo.id",
                                 [])  # 联表查询

    else:
        # data_list = db.fetch_all("select * from `order` where user_id=%s",[user_info['id']])
        data_list = db.fetch_all(
            "select * from `order` left join userinfo on `order`.user_id = userinfo.id where `order`.user_id = %s",
            [user_info['user_id']]
        )

    # print(data_list)
    return render_template('order_list.html',
                           data_list=data_list,
                           status_dict=status_dict,
                           real_name=real_name)


@od.route("/order/create", methods=["GET", "POST"])
def order_create():
    if request.method == "GET":
        return render_template('order_create.html')

    url = request.form.get("url")
    count = request.form.get("count")
    # 写入数据
    user_info = session.get('user_info')
    # print(user_info, '====user_info')
    params = [url, count, user_info['user_id']]
    order_id = db.insert('insert into `order`(url,count,user_id,status) values (%s,%s,%s,1)', params)
    # 写入reids队列
    print(order_id)
    cache.push_queue(order_id)
    return redirect("/order/list")


@od.route("/order/update/<int:id>", methods=["GET", "POST"])
def order_update(id):
    if request.method == "GET":
        order_dict = db.fetch_one("select * from `order` where id = %s", [id])
        print(order_dict, '====order_dict')
        if order_dict:
            return render_template('order_create.html',
                                   url=order_dict.get('url'),
                                   count=order_dict.get('count')
                                   )
        else:
            return '未找到对应的订单'

    url = request.form.get("url")
    count = request.form.get("count")
    # 写入数据，更新数据库
    params = [url, count, id]
    order_id = db.insert('UPDATE `order` SET url=%s, count=%s WHERE id=%s', params)
    return redirect("/order/list")


@od.route("/order/delete", methods=["POST"])
def order_delete():
    data = request.get_json()

    id = data.get('id')

    if not id:
        return jsonify({"status":False,"msg":"缺少订单ID"}), 400
    db.insert( "DELETE FROM `order` WHERE id=%s", [id])
    return jsonify({'success': True, 'redirect': '/order/list'})