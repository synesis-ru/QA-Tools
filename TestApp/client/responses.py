# -*- coding: utf-8 -*-
import sys, os
import urlparse
import json
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from server.core import requests
from server import config
    
def sleep_timeout(req, sec ):
    print 'SLEEP TIMEOUT'
    time.sleep(sec)
    request = req.path
    data = requests.do_get_request_encoded(request)
    req.send_response(200)
    req.end_headers()
    print "SLEEP TIMEOUT RESPONSE: -----  %s" % data
    req.wfile.write(data)
 
def server_error(req, code):
    print 'SERVER ERROR %d' %code
    req.send_error(code)

def ok_response(req, params):
    print 'GET HTTPLIB REQUEST'
    request = req.path
    data = requests.do_get_request_encoded(request)
    print '\nRequest = %s       \n\nReaponse = %s' % (request,data)
    req.send_response(200)
    req.end_headers()
    req.wfile.write(data)
    
def ok_post_response(req, params):
    print 'POST HTTPLIB REQUEST'
    request = req.path
    len = int(req.headers['Content-length'])
    data_in = req.rfile.read(len)
    print "POST %d bytes IN : %s\n" % (len, data_in)
    data = requests.do_post_request_encoded(request, data_in)
    print '\nRequest = %s       \n\nReaponse = %s' % (request,data)
    req.send_response(200)
    req.end_headers()
    req.wfile.write(data)
    
    
def bad_post_response(req, params):
    print 'POST RESPONSE'
    request = req.path
    data = requests.do_post_request_encoded(request, params)
    print 'Request = %s       Reaponse = %s' % (request,data)
    req.send_response(200)
    req.end_headers()
    req.wfile.write(data)
    
    
def bad_response(req, params):
    print 'BAD RESPONSE'
    request = req.path
    garbage = 'sdgfsdihgdf/f&?\rtgwegtyher'
    data = requests.do_get_request_encoded(request) + garbage
    print 'Request = %s       Reaponse = %s' % (request,data)
    req.send_response(200)
    req.end_headers()
    req.wfile.write(data)
    
    
def close_socket(req, params):
   # BaseHTTPServer.BaseHTTPRequestHandler.
    req.send_response(200)
    req.end_headers()
    req.wfile.write('')
   

def parse_request(req):
    request = req.path
    delim = request.find('?')
    if delim == -1:
        game_req = 0
        print "REQUEST %s doesn't contain <?>" % request
        return (game_req, request, request)
    else:
        game_req = 1
        req_func, arg = request.split('?')
  #  print '  req_func = ' + req_func + '             arg = ' + arg
  #  print "request = %s" % request
        r_enc = urlparse.parse_qsl(arg)
        arg_dict = dict(r_enc)
 #   print arg_dict.items()
        return (game_req, req_func, arg_dict)
    
def token_error(req, params):
    resp = {"class":"AuthResult","message":"invalid format","object":"null","result":104}
    response_json = json.dumps(resp)
    req.send_response(200)
    req.end_headers()
    print "TOKEN ERROR RESPONSE: --- %s" %response_json
    req.wfile.write(response_json)

def ok_get_urllib2_response(req):
    print 'GET URLLIB2 REQUEST'
    request = req.path
    data = requests.do_get_request_urllib2(request)
    print '\nRequest = %s       \n\nReaponse = %s' % (request,data)
    req.send_response(200)
    req.end_headers()
    req.wfile.write(data)
    
    
def ok_post_urllib2_response(req, params):
    print 'POST URLLIB2 REQUEST'
    request = req.path
    len = int(req.headers['Content-length'])
    data_in = req.rfile.read(len)
    print "POST %d bytes IN : %s\n" % (len, data_in)
    data = requests.do_post_request_urllib2(request, data_in)
    print '\nRequest = %s       \n\nReaponse = %s' % (request, data)
    req.send_response(200)
    req.end_headers()
    req.wfile.write(data)
      
    
    
    
    
    
    
    
    
    
    
    
