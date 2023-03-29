
from wsgiref.simple_server import  make_server
import json

from colored_logs.logger import Logger, LogType

PACKAGE_NAME = "httpserver"
log = Logger(ID=PACKAGE_NAME)

PACKAGE_NAME = 'game5001'
connStr = '''
{
    "code":0,
    "msg":"success 成功"
}
'''

heartbeatStr = '''
{
    "code":0,
    "msg":"success 成功"
}
'''
heartbeatErrStr = '''
{
    "code":-1,
    "msg":"Failed 无效"
}
'''
infoGetStr = '''
{
    "code":0,
    "msg":"GET 成功"
}
'''

infoPostStr = '''
{
    "code":0,
    "msg":"POST 成功"
}
'''
errStr = '''
{
    "code":-1,
    "msg":"not support"
}
'''

def RunServer(env, start_response):
    # 添加回复内容的HTTP头部信息，支持多个
    headers = {"Content-Type":'application/json', 'Custom-head1':'frank server'}

    # env包含当前环境信息与请求信息
    current_url = env["PATH_INFO"]
    current_content_type = env["CONTENT_TYPE"]
    current_content_length = env["CONTENT_LENGTH"]
    current_request_method = env["REQUEST_METHOD"]
    current_remote_address = env["REMOTE_ADDR"]
    current_encode_type = env["PYTHONIOENCODING"]
    # 获取body json数据，并转换为python对象
    current_req_body = env["wsgi.input"].read(int(env["CONTENT_LENGTH"]))
    current_req_json = json.loads(current_req_body)

    #打印客户端请求信息
    log.success("request ip:",current_remote_address)
    log.success("request method:", current_request_method)
    log.success("request url:",current_url)
    log.success("request content-type:",current_content_type)
    log.success("request body:", current_req_json)

    # 127.0.0.1:8888/connect or 192.168.63.230
    if current_url == "/connect":
        start_response("200 ok", list(headers.items()))
        return [connStr.encode("utf-8"),]
    elif current_url == "/spin":   # 127.0.0.1:8888/spin
        # 主要修改这里的代码，从客户端获取json数据后，如何处理？ 并返回一个结果给客户端
        bet = current_req_json["bet"]
        userid = current_req_json["userid"]
        log.success("userid {0} bet {1}".format(userid, bet))
        result = {"total_win":18.6, "tuan_matrix":[[1,2,3,4,5],[3,3,4,5,6],[3,3,4,5,6]]}
        infoStr = json.dumps(result)
        start_response("200 ok", list(headers.items()))
        return [infoStr.encode("utf-8"), ]
    else:
        start_response("404 not found", list(headers.items()))
        return [errStr.encode("utf-8"),]

if __name__ =="__main__":
    httpd = make_server('', 8888, RunServer)
    host,port = httpd.socket.getsockname()
    log.success("start running",host,"port",port)
    httpd.serve_forever()