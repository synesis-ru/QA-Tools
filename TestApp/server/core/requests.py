# -*- coding: utf-8 -*-
import urllib2
import httplib
import simplejson as json
import logging
import exceptions
from server import config
import traceback

def do_get_request(request):
    decoded = {'result' : 'UNDEFINED'}
    data = None
    try:
        conn = None
        conn = httplib.HTTPConnection(config.SERVER)
       # logging.debug("DO GET REQUEST ")
        conn.request('GET', request)
        resp = conn.getresponse()
        status = resp.status
        print "status = " + str(status)
        if status == 200:
            data = resp.read()
            print "DATA = " + str(data)
            conn.close()
            decoded = json.loads(data)
            if decoded[u'result'] == 0:
                return decoded
            else:
                raise exceptions.RequestFailedError(decoded)
                return {}
        else:
            logging.warning("Bad response --- status  = %d" % status)
            if conn:
                conn.close()
    except exceptions.RequestFailedError, e:
        raise exceptions.RequestFailedError(decoded)
        if conn:
            conn.close()
            return {}
    except Exception, e:
        if conn:
            conn.close()
        logging.warn('%s\n--- GET request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
        raise exceptions.RequestFailedError(status)
        return {}
        

def do_post_request(request, data_in):
    decoded = {'result' : 'UNDEFINED'}
    data = None
    try:
        conn = None
        conn = httplib.HTTPConnection(config.SERVER)
        conn.request(method='POST', url=request, body=data_in )
        resp = conn.getresponse()
        status = resp.status
        print "status = " + str(status)
        data = resp.read()
        print "DATA = " + str(data)
        conn.close()
        decoded = json.loads(data)
    except Exception, e:
        if conn:
            conn.close()
            logging.warn('---HTTP ERROR POST conn = %s \n%s ' % (conn, e))
            if data:
                logging.warn("     Response was %s "% data)
        logging.warn('%s\n--- POST request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
    if decoded[u'result'] == 0:
        return decoded
    else:
        raise exceptions.RequestFailedError(decoded)
        return {}
    
    
def do_get_request_encoded(request):
    data = None
    try:
        conn = None
        conn = httplib.HTTPConnection(config.SERVER)
    #    print "!!!!!!!!!!!!!Request = %s" %request
        conn.request('GET', request)
        resp = conn.getresponse()
        status = resp.status
        print "status = " + str(status)
        if status == 200:
            data = resp.read()
            return data
        else:
            logging.warning("Bad response --- status  = %d" % status)
            if conn:
                conn.close()
    except exceptions.RequestFailedError, e:
        print 'RequestFailedError --- do_get_request_encoded'
      #  raise exceptions.RequestFailedError(data)
        if conn:
            conn.close()
            return {}
    except Exception, e:
        print 'Exception --- do_get_request_encoded'
        if conn:
            conn.close()
      #  logging.warn('%s\n--- GET request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
        print('%s\n--- GET request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
      #  raise exceptions.RequestFailedError(conn)
        return {}


def do_post_request_encoded(request, data_in):
    data = None
    try:
        conn = None
        conn = httplib.HTTPConnection(config.SERVER)
        conn.request(method='POST', url=request, body=data_in )
        resp = conn.getresponse()
        status = resp.status
        print "status = " + str(status)
        if status == 200:
            data = resp.read()
            return data
        else:
            logging.warning("Bad response --- status  = %d" % status)
            if conn:
                conn.close()
    except Exception, e:
        if conn:
            conn.close()
            logging.warn('---HTTP ERROR POST conn = %s \n%s ' % (conn, e))
            if data:
                logging.warn("     Response was %s "% data)
                logging.warn('%s\n--- POST request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
        return {}
    

def do_get_request_urllib2(request):
    data = None
    try:
        resp = None
        resp = urllib2.urlopen(config.SERVER1 + request)
        data = resp.read()
        resp.close()
    except urllib2.HTTPError, e:
        logging.warn('HTTP error %d' % e.code)
        if resp:
            resp.close()
    except urllib2.URLError, e:
        logging.warn("Network error: %s" % e.reason.args[1])
        if resp:
            resp.close()
    except Exception, e:
        logging.warn("do_get_request_urllib2 ---- Exception")
        if resp:
            resp.close()
            if data:
                logging.warn('%s\n--- POST request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
    return data       


def do_post_request_urllib2(request, data_in):
    data = None
    try:
        resp = None
        resp = urllib2.urlopen(config.SERVER1 + request, data_in)
        data = resp.read()
        resp.close()
    except urllib2.HTTPError, e:
        logging.warn('HTTP error %s' % e)
        if resp:
            resp.close()
    except urllib2.URLError, e:
        logging.warn("Network error: %s" % e)
        if resp:
            resp.close()
    except Exception, e:
        logging.warn("do_get_request_urllib2 ---- Exception")
        if resp:
            resp.close()
            if data:
                logging.warn('%s\n--- POST request failed %s\n--- REASON: %s\n--- DATA: %s' % (traceback.format_exc(), request, e, data))
    return data        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    