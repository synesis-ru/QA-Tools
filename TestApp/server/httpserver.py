# -*- coding: utf-8 -*-
import BaseHTTPServer
import SocketServer
import random
import sys

#PORT = 8000
#random.shuffle(USERS)
USERS = []
elementIndex = 0

class Simple(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(req):
        global elementIndex
        req.send_response(200)
        req.end_headers()
        if elementIndex >= (len(USERS)-1):
            req.wfile.write("EMPTY")
            elementIndex = 0
          #  return
        else:
            idx = USERS[elementIndex]
            elementIndex += 1
        print "index = %d element = %d" % (elementIndex-1, idx)
      #  USERS.remove(idx)
        req.wfile.write(idx)

def main():   
    while len(sys.argv) != 4:
        print """
                 1-st argument is PORT;
                 2-nd argument is low index;
                 3-rd argument is high index;
                """
        sys.exit(-1)
    global USERS
    if sys.argv[1].isdigit() and sys.argv[2].isdigit() and sys.argv[3].isdigit():
        PORT = int(sys.argv[1])
        low_index = int(sys.argv[2])
        top_index = int(sys.argv[3])
        USERS = range(low_index, top_index+1)
        random.shuffle(USERS)
        httpd = BaseHTTPServer.HTTPServer(("", PORT), Simple)
        print "serving at port", PORT
        httpd.serve_forever()
    else:
        print """
                All arguments should be digit!
                1-st argument is PORT;
                2-nd argument is low index;
                3-rd argument is high index;
              """
        sys.exit(-1)

if __name__ == '__main__':
    main()
