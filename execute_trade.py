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

print (acct_num)
fixml = ET.Element('FIXML', xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2")
order = ET.SubElement(fixml, "Order",
                    TmInForce="0",
                    Typ="2",
                    Side="1",
                    Px="11.75",
                    Acct=acct_num)
inst = ET.SubElement(order, "Instrmt",
                    SecTyp="0",
                    Sym="F")
ordqty = ET.SubElement(order, "OrdQty",
                    Qty="1")

tree = ET.ElementTree(fixml)


tree.write("test_xml.xml")

target_url = trade_endpoint + acct_num + '/orders.xml'
print (target_url)
print (oauth_hdr)
print (tree)
XML_STRING = open('test_xml.xml').read()
print (XML_STRING)
print ('\n\n')
#with open('test_xml.xml') as xml:
print ('sending')
r = requests.post(url=target_url, auth=oauth_hdr, data=XML_STRING)
print(r)
print(r.content)
r = requests.get(url=target_url, auth=oauth_hdr)
print (r)
xml = ET.fromstring(r.content)
x = etree.parse(r.content)
for table in xml.iter():
    for child in table:
        print (child.tag, child.text)

'''
root = ET.Element("root")
doc = ET.SubElement(root, "doc")
ET.SubElement(doc, "field1", name="blah").text = "some value1"
ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

tree = ET.ElementTree(root)
print (tree)

tree.write("test_xml.xml")'''

'''
xml = """my xml"""
headers = {'Content-Type': 'application/xml'}
requests.post('http://www.my-website.net/xml', data=xml, headers=headers)
'''


'''
<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
  <Order TmInForce="0" Typ="2" Side="1" Px="13" Acct="12345678">
    <Instrmt SecTyp="CS" Sym="F"/>
    <OrdQty Qty="1"/>
  </Order>
</FIXML>
'''