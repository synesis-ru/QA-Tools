#!/usr/bin/python 
# -*- coding: utf-8 -*-
import BaseHTTPServer
import SocketServer
import sys
#import cgi
import requestlist
import responses

PORT = 8092
HOST_NAME = ''
 
class TestServer(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(req):
        print '-----------------------------------'
        print 'GET REQUEST'
        print req.path
        print req.command
        game_req, req_func, arg_dict = responses.parse_request(req)
        if game_req:
            print req_func
            if not requestlist.GET_HANDLERS.has_key(req_func):
                print 'request %s not founded' % req_func
                return
            print arg_dict.items()
            count_functions = len(requestlist.GET_HANDLERS[req_func]['responses'])
      #  print '++++ Count of functions = ' + str(count_functions)
            idx = requestlist.GET_HANDLERS[req_func]['index']
      #  print 'idx = ' + str(idx)
            if idx >= count_functions:
                idx = 0
                requestlist.GET_HANDLERS[req_func]['index'] = 0
            requestlist.GET_HANDLERS[req_func]['index'] += 1
            func_tuple = requestlist.GET_HANDLERS[req_func]['responses'][idx] #idx
            func_tuple[0](req, func_tuple[1])
        else:
            responses.ok_get_urllib2_response(req)
            
        
        

    def do_POST(req):
        print '\n-----------------------------------\n'
        print 'POST REQUEST'
        print req.path
        # Parse the form data posted
        game_req, req_func, arg_dict = responses.parse_request(req)
        if game_req:
            print 'GAME_REQ=%d' % game_req
            print req_func
            if not requestlist.GET_HANDLERS.has_key(req_func):
                print 'request %s not founded' % req_func
                return
            print arg_dict.items()
            count_functions = len(requestlist.GET_HANDLERS[req_func]['responses'])
      #  print '++++ Count of functions = ' + str(count_functions)
            idx = requestlist.GET_HANDLERS[req_func]['index']
      #  print 'idx = ' + str(idx)
            if idx >= count_functions:
                idx = 0
                requestlist.GET_HANDLERS[req_func]['index'] = 0
            requestlist.GET_HANDLERS[req_func]['index'] += 1
            func_tuple = requestlist.GET_HANDLERS[req_func]['responses'][idx] #idx
            func_tuple[0](req, func_tuple[1])
        else:
          responses.ok_post_urllib2_response(req, '')  



def main():   
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from server import config
    from server.core import requests
    global requests
    
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT), TestServer)
    print 'testserver started at %d PORT' % PORT
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
            

if __name__ == '__main__':
    main()
