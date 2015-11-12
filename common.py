#/usr/bin/python
#coding=utf-8

import os,sys
import time,datetime
import markdown2
import redis
import json

blogfilepath = '/data0/pyprojects/ittech/wwwroot/mdblogpath/'
markdownext = ['wiki-tables','tables','codehilite','smart_strong','nl2br','toc','footnotes','wikilinks','metadata','fenced-code-blocks','code-color','fenced-code']

def get_total_articl(filepath):
	r = redis.StrictRedis(host = 'localhost', port = 6000, db = 0)
	blogtotal = r.get('blogpostsnum')
	if blogtotal > 0:
		return blogtotal
	blogtotal = 0
	for root, dirs, files in os.walk(filepath):
		if root == None:
			continue
		if root == blogfilepath + 'topic':
			continue
		for name in files:
			blogtotal += 1
	r.set('blogpostsnum',blogtotal,360)
	return blogtotal
		
def get_pages(total,curpage):
	from pypages import Paginator
	per_page = 10
	total = int(total)
	objects = range(1,int(total / per_page) + 2)
	page = Paginator(total, per_page, curpage)
	page.objects = objects
	return page

def get_page_lists(curpage):
	postsnum = get_total_articl('/data0/pyprojects/ittech/wwwroot/mdblogpath/')
	pagelist = get_pages(postsnum,int(curpage))
	return pagelist
	
def get_unixtimestamp(dates):
	ndate = dates.split('-')
	dateC = datetime.datetime(int(ndate[0]),int(ndate[1]),int(ndate[2]),00,00,00)
	timestamp = time.mktime(dateC.timetuple())
	return timestamp
	
def get_md_file(filepath):
	mdfile = list()
	for root, dirs, files in os.walk(filepath):
		if root == None:
			continue
		if root == blogfilepath + 'topic':
			continue
		for name in files:
			filename = os.path.join(root, name)
			filedata = dict()
			filedata['filename'] = name.split('.')[0]
			filedata['createtime'] = time.ctime(os.path.getctime(filename))
			filedata['createtimes'] = get_unixtimestamp(markdown2.markdown_path(filename,extras = ['metadata']).metadata.get('Date'))
			filedata['filepath'] = filename
			mdfile.append(filedata)

	def createtime(s):
		return s['createtimes']

	mdfile = sorted(mdfile,key = createtime,reverse = True)	
	return mdfile

def get_md_achrivers(filepath):
	mdfile = get_md_file(filepath)
	achives = dict()
	for nd in mdfile:
		html = markdown2.markdown_path(nd.get('filepath'),extras = ['metadata'])
		usertime = time.strftime('%Y-%m',time.localtime(int(time.mktime(time.strptime(html.metadata['Date'],'%Y-%m-%d')))))
		if achives.has_key(usertime):
			achives[usertime].append((nd.get('filename'),html.metadata['Title'],html.metadata['Date']))
		else:
			achives[usertime] = list()
			achives[usertime].append((nd.get('filename'),html.metadata['Title'],html.metadata['Date']))	
	return 	achives

def get_blog_lists(path):
	bloglist = list()
	try:
		r = redis.StrictRedis(host = 'localhost', port = 6000, db = 0)
		bloglist = r.get('bloglists')
		if bloglist != None:
			return json.loads(bloglist)
		else:
			bloglist = list()
	except:
		bloglist = list()
	files = get_md_file(path)
	for i in files:
		html = markdown2.markdown_path(i.get('filepath'),extras = ['metadata'])
		html.metadata['filename'] = i.get('filename')
		html.metadata['createtime'] = time.strftime('%Y-%m-%d',time.localtime(int(time.mktime(time.strptime(i.get('createtime'),'%a %b %d %H:%M:%S %Y')))))
		bloglist.append(html.metadata)
	r.set('bloglists',json.dumps(bloglist),360)
	return bloglist
	
def get_achrives(path):
	r = redis.StrictRedis(host = 'localhost', port = 6000, db = 0)
	achrivers = r.get("blog_achrives")
	if achrivers is not None:
		return json.loads(achrivers)
	achrivers = get_md_achrivers('/data0/pyprojects/ittech/wwwroot/mdblogpath/')
	achrivers = json.dumps(achrivers)
	r.set("blog_achrives",achrivers,3600 * 6)
	return json.loads(achrivers)
	
def get_md(mdpath = None):
	path = mdpath or '/data0/pymd/01.0.md'
	html = markdown2.markdown_path(path,extras = markdownext)
	html.metadata['createtime'] = time.ctime(os.path.getctime(path))
	return html
	
def makerss(bloglists):
	xml = ''
	xml += '<?xml version="1.0" encoding="utf-8" ?>' + "\n"
	xml += '<rss version="2.0">' + "\n"
	xml += '<channel>' + "\n"
	xml += '<title>IT笔记</title>' + "\n"
	xml += '<link>http://blog.itmark.net/</link>' + "\n"
	xml += '<description>Latest 20 threads of all Posts</description>' + "\n"
	xml += '<copyright>Copyright(C) IT笔记</copyright>' + "\n"
	xml += '<generator>IT笔记 by River King.</generator>' + "\n"
	xml += '<lastBuildDate>' + datetime.datetime.now().strftime("%Y-%m-%d %X") + '</lastBuildDate>' + "\n"
	xml += '<ttl>3600</ttl>' + "\n"
	for l in bloglists:
		xml += '<item>' + "\n"
		xml += '<title>' + l.get('Title').encode('utf-8') + '</title>' + "\n"
		xml += '<link>http://blog.itmark.net/posts/' + l.get('filename').encode('utf-8') + '.html</link>' + "\n"
		xml += '<description><![CDATA[' + l.get('Summary').encode('utf-8') + ']]></description>' + "\n"
		xml += '<author>River King</author>' + "\n"
		xml += '<pubDate>' + l.get('createtime').encode('utf-8') + '</pubDate>' + "\n"
		xml += '</item>' + "\n"
	xml += '</channel>' + "\n"
	xml += '</rss>'
	return xml