import telnetlib
from flask import Flask
from moomoo import *
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    return app.send_static_file("index.html")

@app.route("/login")
def login():
    # 获取前端传来的 code 参数
    code = request.args.get('code')

    # 创建一个 Telnet 对象
    tn = telnetlib.Telnet()

    # 连接到指定的主机和端口
    tn.open('127.0.0.1', 22222)

    # 发送指令
    command = f"input_phone_verify_code -code={code}\n"
    tn.write(command.encode('ascii'))

    # 读取返回的信息
    output = tn.read_all().decode('ascii')

    # 关闭连接
    tn.close()

    return output

@app.route("/test")
def test():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
    quote = quote_ctx.get_market_snapshot('HK.00700')  # 获取港股 HK.00700 的快照数据
    print(quote)
    quote_ctx.close() # 关闭对象，防止连接条数用尽


    trd_ctx = OpenSecTradeContext(host='127.0.0.1', port=11111)  # 创建交易对象
    result = trd_ctx.place_order(price=500.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE)
    print(result)  # 模拟交易，下单（如果是真实环境交易，在此之前需要先解锁交易密码）

    trd_ctx.close()  # 关闭对象，防止连接条数用尽
    return "quote: " + quote + "\nresult: " + str(result)