from http.server import  HTTPServer,BaseHTTPRequestHandler
import json
json_data=[]
from http import HTTPStatus

class requestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK)

        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path.endswith('/api/temperature'):
            self.send_response(HTTPStatus.OK)
            output = ''
            output += '<html><body>'
            output += '<h1>ValueList</h1><p>'

            print('jsondata:',json_data)
            print(len(json_data))
            if (len(json_data)>0):

                for data in json_data:
                    output += 'data'
                    output += '</p></br>'
                output += '</body></html>'
            self.wfile.write(output.encode())




    def do_POST(self):
        if self.path.endswith('api/temperature'):

            content_len = (int(self.headers['Content-Length']))
            data= self.rfile.read(content_len)
            post_data = json.loads(data)
            data=json.dumps(post_data[len(post_data)-1], indent=4)
            print('Postdata:',data)
            json_data.append(data)
            self._set_headers()


def main():
    PORT = 9000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()