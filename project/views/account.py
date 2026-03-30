
from flask import Blueprint,render_template,request,redirect,session,jsonify
from utils import db
ac = Blueprint( "account",__name__) #蓝图对象

@ac.route("/",methods=['GET'])
def index():
    return render_template('home.html')

@ac.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    phone = request.form['phone']
    password =request.form['password']
    role = request.form['role']
    #连接mysql，并执行查询用户名密码是否正确
    user_dict = db.fetch_one("select * from userinfo where role=%s and phone=%s and password =%s", (role,phone,password))
    print(f'拿到的返回值：{user_dict}')
    if  user_dict:
        #设置浏览器里的cookies的值，会是一长串，这个里面包含以下的信息
        session['user_info'] = {
            "role":user_dict['role'],
            "real_name":user_dict['real_name'],
            "user_id":user_dict['id'],
            "phone": user_dict['phone'],
        }
        return redirect('/order/list')
    return render_template('login.html',error='用户名或密码错误')


@ac.route("/users")
def users():
    pass

@ac.route('/logout', methods=['POST'])
def logout():
    """处理退出登录"""
    session.clear()  # 清除 session
    return jsonify({'success': True, 'redirect': '/login'})