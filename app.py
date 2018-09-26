
import os
port = int(os.environ.get("PORT", 5000))
from urllib.parse import urlparse
from urllib.parse import parse_qs
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '0.0.0.0'
PORT_NUMBER = port

mydata={'sensorValue':'none','time':'none'}
class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }
        if "?" in self.path:
            data=dict(parse_qsl(self.path.split("?")[1], True))
            for key,value in dict(parse_qsl(self.path.split("?")[1], True)).items():
                print (key + " = " + value)
            print ('data',data)
            print ('mydata', mydata)
            myTime=time.asctime()
            mydata['time']=myTime
            mydata['sensorValue']=data['sensorValue']

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Title goes here.</title></head>
        <body><p>This is a test.</p>
        <p>You accessed path: {}</p>
        <p>Sensor value: {}</p>
        </body></html>
        '''.format(path,mydata['sensorValue'])
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
