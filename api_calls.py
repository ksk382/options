# -*- coding: utf-8 -*-
import requests
import pandas as pd
import datetime as dt
from cred_file import oauth_hdr, stock_endpoint, option_endpoint, balance_endpoint, trade_endpoint, acct_num
import os
import xml.etree.ElementTree as ET
import json

def get_stock_df(ticker):
    target_url = stock_endpoint + ticker
    r = requests.get(url=target_url, auth=oauth_hdr)
    #print(json.dumps(d, indent = 4, sort_keys=True))
    d = r.json()['response']['quotes']['quote']
    df = pd.DataFrame([d])
    # pass a rate limiter
    try:
        e = int(r.headers['X-RateLimit-Remaining'])
    except:
        e = 1
    return df, e

def get_option_df(ticker):
    now = dt.datetime.now()
    year = str(now.year)
    #month = str(now.month)
    q = f'&query=xyear-eq%3A{year}' #%20AND%20xmonth-eq%3A{month}'
    target_url = option_endpoint + ticker + q
    r = requests.get(url=target_url, auth=oauth_hdr)
    #print(json.dumps(d, indent = 4, sort_keys=True))
    d = r.json()['response']['quotes']['quote']
    df = pd.DataFrame(d)
    # pass a rate limiter
    try:
        e = int(r.headers['X-RateLimit-Remaining'])
    except:
        e = 1
    return df, e

def get_balance():
    target_url = balance_endpoint
    r = requests.get(url=target_url, auth=oauth_hdr)
    try:
        d = r.json()['response']['accountbalance']['accountvalue']
    except Exception as e:
        print (str(e))
        print (r)
    d = float(d)
    return d


def buy_stock(symbol, qty, limit_price):
    buy_sell = '1'
    r = limit_order(symbol, qty, limit_price, buy_sell)
    return r

def sell_stock(symbol, qty, limit_price):
    buy_sell = '2'
    r = limit_order(symbol, qty, limit_price, buy_sell)
    return r

def limit_order(symbol, qty, limit_price, buy_sell):
    limit_price = str(limit_price)
    fixml = ET.Element('FIXML', xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2")
    order = ET.SubElement(fixml, "Order",
                          TmInForce="0",
                          Typ="2",
                          Side=buy_sell,
                          Px=limit_price,
                          Acct=acct_num)
    inst = ET.SubElement(order, "Instrmt",
                         SecTyp="CS",
                         Sym=symbol)
    ordqty = ET.SubElement(order, "OrdQty",
                           Qty=qty)

    xml_dir = '../transaction_xml/'
    if not os.path.exists(xml_dir):
        os.mkdir(xml_dir)
    tree = ET.ElementTree(fixml)

    now = dt.datetime.now()
    now_str = dt.datetime.strftime(now, "%Y-%m-%d_%H.%M")
    out_name = xml_dir + symbol + now_str + '.xml'
    tree.write(out_name)

    target_url = trade_endpoint + acct_num + '/orders.xml'
    XML_STRING = open(out_name).read()
    r = requests.post(url=target_url, auth=oauth_hdr, data=XML_STRING)
    out_name = xml_dir + symbol + now_str +  '_response.txt'
    with open(out_name, 'wb') as f:
        f.write(r.content)

    return (r.content)

def get_holdings():
    target_url = trade_endpoint + acct_num + '/holdings.json'
    r = requests.get(url=target_url, auth=oauth_hdr)
    d = r.json()['response']['accountholdings']
    return d

def get_oders():
    target_url = trade_endpoint + acct_num + '/orders.json'
    r = requests.get(url=target_url, auth=oauth_hdr)
    d = r.json()['response']
    e = d['orderstatus']['order']
    print(json.dumps(e, indent = 4, sort_keys=True))
    for i in e:
        root = ET.parse(i['fixmlmessage']).getroot()
    value = root.get('FIXML')
    print(value)
    return d

if __name__ == "__main__":
    r = get_oders()
