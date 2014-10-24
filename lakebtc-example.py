#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import lakebtc
 
access_key="Your Email"
private_key="Your Private_key"
 
l = lakebtc.Lakebtc(access_key,private_key)

#Public API

#Ticker
result = l.get_ticker()
print result

#Oder Book
result = l.get_bcorderbook()
print result

result = l.get_bcorderbook_cny()
print result

#Trade Histroy
result = l.get_bctrades(1408089363)
print result

#Private API(private_key is required)

#getAccountInfo
#result = l.get_account_info()
#print result

#buyOrder
#result = l.buy(500,0.1,"USD")
#print result

#sellOrder
#result = l.sell(300,0.1,"USD")
#print result

#getOrders
#result = l.get_orders()
#print result

#cancelOrder (need order id)
#result = l.cancel(3296)
#print result
 
#getTrades
#result = l.get_trades(1403078138)
#print result
