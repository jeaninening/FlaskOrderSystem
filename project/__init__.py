from flask import Flask, session, request, redirect,url_for
from .views import account
from .views import order

app = Flask(__name__)

def auth():
    # 1. 放行静态文件（不需要验证）
    if request.path.startswith('/static'):
        return None  # 放行，继续处理请求

    # 2. 放行登录页面（不需要验证）
    if request.path == '/login':
        # 如果已经登录，跳转到列表页
        if session.get('user_info'):
            return redirect('/order/list')
        return None  # 未登录，放行显示登录页

    # 3. 其他页面需要验证登录
    user_info = session.get('user_info')
    if not user_info:
        # 未登录，重定向到登录页
        return redirect('/login')

    # 已登录，放行
    return None

def get_real_name():
    #在页面渲染时调用
    user_info = session.get('user_info')
    if user_info:
        return user_info
    else:
        return ''


#这个地方不可以是动态的
#不然每次刷新，你储存的cookies就无法获取
SECRET_KEY ='your-fixed-secret-key-here-keep-it-safe'

app.template_global()(get_real_name)  # 全局注册


def create_app():
    app.secret_key = SECRET_KEY
    app.register_blueprint(account.ac)
    app.register_blueprint(order.od)
    app.before_request(auth)


    return app