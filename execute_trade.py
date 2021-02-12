# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
import os
import requests
import xml.etree.cElementTree as ET
from cred_file import acct_num, oauth_hdr, trade_endpoint
import lxml.etree as etree


def buy_stock(symbol, limit_price):
    limit_price = str(limit_price)
    fixml = ET.Element('FIXML', xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2")
    order = ET.SubElement(fixml, "Order",
                          TmInForce="0",
                          Typ="2",
                          Side="1",
                          Px=limit_price,
                          Acct=acct_num)
    inst = ET.SubElement(order, "Instrmt",
                         SecTyp="CS",
                         Sym=symbol)
    ordqty = ET.SubElement(order, "OrdQty",
                           Qty="1")

    tree = ET.ElementTree(fixml)

    tree.write("test_xml.xml")

    target_url = trade_endpoint + acct_num + '/orders.xml'
    print(target_url)
    print(oauth_hdr)
    print(tree)
    XML_STRING = open('test_xml.xml').read()
    print(XML_STRING)
    print('\n\n')
    # with open('test_xml.xml') as xml:
    print('sending')
    r = requests.post(url=target_url, auth=oauth_hdr, data=XML_STRING)
    print(r)
    print(r.content)

    return

def sell_stock(symbol, limit_price):
    limit_price = str(limit_price)
    fixml = ET.Element('FIXML', xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2")
    order = ET.SubElement(fixml, "Order",
                          TmInForce="0",
                          Typ="2",
                          Side="2",
                          Px=limit_price,
                          Acct=acct_num)
    inst = ET.SubElement(order, "Instrmt",
                         SecTyp="CS",
                         Sym=symbol)
    ordqty = ET.SubElement(order, "OrdQty",
                           Qty="1")

    tree = ET.ElementTree(fixml)

    tree.write("test_xml.xml")

    target_url = trade_endpoint + acct_num + '/orders.xml'
    print(target_url)
    print(oauth_hdr)
    print(tree)
    XML_STRING = open('test_xml.xml').read()
    print(XML_STRING)
    print('\n\n')
    # with open('test_xml.xml') as xml:
    print('sending')
    r = requests.post(url=target_url, auth=oauth_hdr, data=XML_STRING)
    print(r)
    print(r.content)

    return

if __name__=="__main__":
    buy_stock('F', 11.30)