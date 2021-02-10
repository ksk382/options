# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
import os
import xml.etree.cElementTree as ET


fixml = ET.Element('FIXML')
ET.SubElement(fixml,"xmlns").text = "http://www.fixprotocol.org/FIXML-5-0-SP2"
order = ET.SubElement(fixml, "Order")
ET.SubElement(order, "TmInForce").text = "0"
ET.SubElement(order, "Typ").text = "2"
ET.SubElement(order, "Side").text = "1"
ET.SubElement(order, "Px").text = "0"
ET.SubElement(order, "Acct").text = "0"
ET.SubElement(order, "Instrmt").text = "0"
ET.SubElement(order, "SecTyp").text = "0"
ET.SubElement(order, "Sym").text = "F"

tree = ET.ElementTree(fixml)
tree.write("test_xml.xml")


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