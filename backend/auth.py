from flask import session
from event.event import LoginEvent, VerifyEvent, SetEnvEvent, GetStatusEvent
from event.eventbus import event_bus
from flask_socketio import emit

def on_login(event: LoginEvent):
    success = login()
    emit('login_response', {'success': success})

def on_verify(event: VerifyEvent):
    success = verify()
    emit('verify_response', {'success': success})

def on_set_env(event: SetEnvEvent):
    set_env(event.env)

def on_get_status(event: GetStatusEvent):
    status = get_status()
    emit('status_response', {'status': status})

event_bus.subscribe(LoginEvent, on_login)
event_bus.subscribe(VerifyEvent, on_verify)
event_bus.subscribe(SetEnvEvent, on_set_env)
event_bus.subscribe(GetStatusEvent, on_get_status)

def login():
    # 这里执行实际的登录操作,例如验证用户名和密码
    # 如果登录成功,设置会话变量
    session['logged_in'] = True
    return True

def verify():
    # 这里执行实际的验证操作,例如检查用户的权限
    # 返回验证结果
    return session.get('logged_in', False)

def set_env(env):
    # 设置环境(模拟环境或正式环境)
    session['env'] = env

def get_status():
    logged_in = session.get('logged_in', False)
    env = session.get('env', 'sim')
    if not logged_in:
        return 'Not Logged In'
    else:
        return f'Logged In ({env})'