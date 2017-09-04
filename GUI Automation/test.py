'''
Created on 2017. szept. 4.

@author: SzuroveczD
'''
from lxml import etree

source = r'./Config/CoFW_Wathcdog.xml'
INFILE = etree.parse(source)
parameter = INFILE.getroot()
print (parameter.xpath("//Configuration//COFWDIRPATH//text()")[0])
