#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import time
import re
import hmac
import hashlib
import base64
import httplib
import json
 
class Lakebtc():
    def __init__(self,access_key=None,private_key=None):
        self.access_key=access_key
        self.private_key=private_key
        self.conn=httplib.HTTPSConnection("www.lakebtc.com")

    #TimeStamp
    def _get_tonce(self):
        return int(time.time()*1000000)

    #Public API
    def get_ticker(self):
        return self._public_get('ticker')

    def get_bcorderbook(self):
        return self._public_get('bcorderbook')

    def get_bcorderbook_cny(self):
        return self._public_get('bcorderbook_cny')

    def get_bctrades(self,timestamp={}):
        return self._public_get(("bctrades?since="+str(timestamp)) if timestamp else "bctrades")

    #Private API (private_key is required).
    def get_account_info(self,post_data={}):
        post_data['method']='getAccountInfo'
        post_data['params']=[]
        return self._private_post(post_data)

    def get_orders(self,post_data={}):
        post_data['method']='getOrders'
        post_data['params']=[]
        return self._private_post(post_data)

    def buy(self,price,amount,currency,post_data={}):
        post_data['method']='buyOrder'
        post_data['params']=["{0:.4f}".format(round(price,4)),"{0:.4f}".format(round(amount,4)),currency]
        return self._private_post(post_data)

    def sell(self,price,amount,currency,post_data={}):
        post_data['method']='sellOrder'
        post_data['params']=["{0:.4f}".format(round(price,4)),"{0:.4f}".format(round(amount,4)),currency]
        return self._private_post(post_data)

    def cancel(self,order_id,post_data={}):
        post_data['method']='cancelOrder'
        post_data['params']=[order_id]
        return self._private_post(post_data)

    def get_trades(self,timestamp,post_data={}):
        post_data['method']='getTrades'
        post_data['params']=[timestamp]
        return self._private_post(post_data)

    #HTTP GET
    def _public_get(self,params):
        self.conn.request("GET",'/api_v1/' + params)
        response = self.conn.getresponse()
        if response.status == 200:
            resp_dict = json.loads(response.read())
            return resp_dict
        else:
            print "Http Code:",response.status
            print "reason:",response.reason

    #HTTP POST
    def _private_post(self,post_data):
        tonce=self._get_tonce()
        post_data['tonce']=tonce
        post_data['accesskey']=self.access_key
        post_data['requestmethod']='post'
        post_data['id']=1

        pd_hash=self._prepare_data(post_data)

        #base64 encoded
        auth_string='Basic '+base64.b64encode(self.access_key+':'+pd_hash)
        headers={'Authorization':auth_string,'Json-Rpc-Tonce':tonce}

        self.conn.request("POST",'/api_v1',json.dumps(post_data),headers)
        response = self.conn.getresponse()

        if response.status == 200:
            resp_dict = json.loads(response.read())
            return resp_dict
        else:
            print "Http Code:",response.status
            print "reason:",response.reason

        return None

    #Format params
    def _prepare_data(self,h):
        qstr=""
        ary=['tonce','accesskey','requestmethod','id','method','params']
        for a in ary:
            if h[a]:
                if a == 'params':
                    param_string=re.sub("[\[\] ]","",str(h[a]))
                    param_string=re.sub("'",'',param_string)
                    param_string=re.sub("True",'1',param_string)
                    param_string=re.sub("False",'',param_string)
                    qstr+=a+'='+param_string+'&'
                else:
                    qstr+=a+'='+str(h[a])+'&'
            else:
                qstr+=a+'=&'
        qstr=qstr.strip('&')

        result = hmac.new(self.private_key, qstr, hashlib.sha1).hexdigest()
        return result
