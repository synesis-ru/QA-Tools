# -*- coding: utf-8 -*-
from responses import *

GET_HANDLERS = {
                '//auth/exchange_token' : {
                    'index' : 0,
                    'responses' : (
                        (ok_response, ''),
                    #   (ok_response, "JSON2...")
                        )
                    },
                '//auth/guest' : {
                    'index' : 0,
                    'responses' : (
                        (ok_response, ''),
                    #   (ok_response, "JSON2...")
                        )
                    },
                '//auth/token' : {
                    'index' : 0,
                    'responses' : (
                        (ok_response, ''),
                    #   (ok_response, "JSON2...")
                        )
                    },
                '//shop/_batch' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_post_response, 'test_string'), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//auth/crossdomain.xml' : {
                    'index' : 0,
                    'responses' : (
                        (ok_response, ''),
                    #   (ok_response, "JSON2...")
                        )
                    },
                '//user/get': {
                    'index' : 0,
                    'responses' : (
                    #    (token_error, ''),
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                     #   (bad_response, ''),
                        (ok_response, ''), 
                        )
                    },
                '//user/set': {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                     #   (bad_response, ''),
                        (ok_response, ''), 
                        )
                    },
                '//user/get_or_create' : {
                    'index' : 0,
                    'responses' : (
                       # (sleep_timeout, 10),
                    #    (server_error, 500),
                       # (server_error, 404),
                      # (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//user/create' : {
                    'index' : 0,
                    'responses' : (
                       # (sleep_timeout, 10),
                     #   (server_error, 500),
                      #  (server_error, 404),
                      # (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//user/remove' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//session/create' : {
                    'index' : 0,
                    'responses' : (
                      #  (sleep_timeout, 10),
                  #      (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//session/query' : {
                    'index' : 0,
                    'responses' : (
                    #    (sleep_timeout, 10),
                   #     (server_error, 500),
                   #     (server_error, 404),
                      #  (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//session/list/get' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                    #    (server_error, 404),
                     #   (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//session/close' : {
                    'index' : 0,
                    'responses' : (
                      #  (sleep_timeout, 10),
                      #  (server_error, 500),
                     #   (server_error, 404),
                      #  (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//session/get' : {
                    'index' : 0,
                    'responses' : (
                      #  (sleep_timeout, 10),
                     #  (server_error, 500),
                   #     (server_error, 404),
                     #  (bad_response, ''),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//session/update' : {
                    'index' : 0,
                    'responses' : (
                   #    (sleep_timeout, 10),
                        (server_error, 500),
                    #   (server_error, 404),
                     #   (bad_post_response, 'test_string'),
                        (ok_post_response, 'test_string'), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//object/put' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_post_response, 'test_string'), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//game/action' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//game/news' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//notification/add_recipient' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//notification/post' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                     #   (server_error, 404),
                     #   (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//notification/remove_recipient' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//shop/change' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//shop/exchange_rate' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//shop/product_list' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_response, ''), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                '//shop/apply_product' : {
                    'index' : 0,
                    'responses' : (
                     #   (sleep_timeout, 10),
                      #  (server_error, 500),
                      #  (server_error, 404),
                      #  (bad_post_response, 'test_string'),
                        (ok_post_response, 'test_string'), # ,'/user/get?token=1&user_id=100')
                        #   (ok_response, "JSON2...")
                        )
                    },
                
               }