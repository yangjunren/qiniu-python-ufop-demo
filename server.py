import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, urllib.request, json, base64
from urllib.parse import urlparse, parse_qsl

# HTTPGetMaxSize 最大处理的文件长度
_httpGetmaxSize = 2 * 1024 * 1024


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _err_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _err_400_response(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # get请求，用于health检测
    def do_GET(self):
        logging.info("POST request,\nPath: {0}\nHeaders:\n{1}\n".format(str(self.path), str(self.headers)))
        if self.path == "/health":
            self._set_response()
            self.wfile.write("health is {}".format("OK").encode("utf-8"))
        else:
            self._err_response()
            self.wfile.write("request url 404！".encode("utf-8"))

    # post请求，用于处理handler请求，并返回处理结果
    def do_POST(self):
        ret = urlparse(self.path)
        if ret.path == "/handler":
            ret_query = dict(parse_qsl(ret.query))
            if len(ret_query) == 2 and ret_query["url"] != "":
                try:
                    url = ret_query["url"]
                    f = urllib.request.urlopen(url)
                    body = f.read()
                    print(type(body))
                    data = base64.b64encode(body).decode("utf-8")
                    self._set_response()
                    self.wfile.write("POST request success！\n\n{0}".format(data).encode("utf-8"))
                except Exception as err:
                    logging.info(err)
                logging.info(
                    "POST request,\nPath: {0}\nHeaders:\n{1}\n\nBody:\n{2}\n".format(str(self.path), str(self.headers),
                                                                                     data))
            elif len(ret_query) < 2:
                try:
                    content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
                    data = self.rfile.read(content_length).decode("utf-8")  # <--- Gets the data itself
                    if json.loads(data)['data']:
                        self._set_response()
                        self.wfile.write("POST request success!\n\n{0}".format(data).encode("utf-8"))
                    else:
                        self._err_400_response()
                        self.wfile.write("request error！".encode("utf-8"))
                except Exception as err:
                    self._err_400_response()
                    logging.info(err)
                logging.info(
                    "POST request,\nPath: {0}\nHeaders:\n{1}\n\nBody:\n{2}\n".format(str(self.path), str(self.headers),
                                                                                     data))
            else:
                self._err_400_response()
                self.wfile.write("request error！".encode("utf-8"))
        else:
            self._err_400_response()
            self.wfile.write("request error！".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=S, port=9200):
    logging.basicConfig(level=logging.INFO)
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()