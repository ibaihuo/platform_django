#!/usr/bin/env python
#-*- coding:utf-8 -*-

# This is for debug and print the SQL query sentence.
from django.db import connection

class DebugMiddleWare(object):
    def process_request(self,request):
        pass

    def process_response(self,request,response):
        for query in connection.queries:
            print('-----------------SQL--------------')
            print('QUERY:' + query['sql'])
            print
            print('TIME:' + query['time'])
            print('----------------------------------')

#             if request.session['validate_code']:
#                 print '===========The session is',request.session['validate_code']
        print ('\n\n')
        return response
