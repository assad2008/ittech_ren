#/usr/bin/python
#coding=utf-8

import sys
import markdown2
from common import *
import re


#print get_achrives('/data0/mdblog/mdblogpath/')
lists = get_achrives('/data0/pyweb/mdblog/mdblogpath/')
for i in lists:
	for ii in lists.get(i):
		print ii
			
'''
strs = 'dfghttpserver(rklehtoyu934u0ep)544334'

x = re.findall(r'\w+httpserver(\(\w+?\))\w+',strs)
print x
print x.group(0)

sys.exit()
'''
'''
lists = get_md_file('/home/pyweb/mdblog/mdblogpath/')
print lists
sys.exit()
filepath = '/home/pyweb/mdblog/mdblogpath/increment-brain-cell.md'
html = markdown2.markdown_path(filepath,extras = ['metadata'])

print html.metadata

fd = open(filepath,'r')
text = fd.read()
fd.close()
'''