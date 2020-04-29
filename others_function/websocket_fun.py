import websocket
import json
import threading
import _thread
import time


# ws = websocket.create_connection("ws://47.111.170.187:49912/ws/QYfe1e24ebf74edd36")  # 创建连接
# print('连接成功')
# '''data为json格式'''
# data = {}
# ws.send(json.dumps(data))  # json转化为字符串，必须转化
# print(ws.recv())  # 服务器响应数据
# wss.close()  # 关闭连接

url = "ws://47.111.170.187:49912/ws/QYfe1e24ebf74edd36"    # 接口地址

def on_message(ws, message):
    print('服务端发送信息:"', message)
    if message:
        print(ws.send('我收到信息了'))

def on_error(ws, error):
    print('服务端发送错误信息:"', error)

def on_close(ws):
    print("close websocket connection !")

def on_open(ws):
    def run(*args):
        content = {"ID": "YG204843178690469800", "type": "punchClock",
             "data": {"clockTime": "1587907101000", "equipmentSerialNumber": "QYfe1e24ebf74edd36", "clockType": 3,
                      "picture": "https://sg.4000750222.com/sgimages/test/2019/12/24/2c90ef856f30d86f016f377306650178.jpg",
                      "userId": "YG308515899550978048", "accessType": 0}, "equipmentSerialNumber": "QYfe1e24ebf74edd36",
             "msgId": "C204843178698858496"}
        content = {}
        print('打开websocket时调用进行发送数据')
        ws.send(json.dumps(content))
        # ws.close()
    _thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    print(time.strftime('%H:%M:%S'))
    # _thread.start_new_thread(ws.run_forever, (None, None, 60, 5,))
    # ws.send(json.dumps({'haha': 'hh'}))
    ws.run_forever(ping_interval=30, ping_timeout=5)
