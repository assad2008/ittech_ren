#/usr/bin/python
#coding=utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.template
from tornado.options import define, options
import os,time,sys
from common import get_blog_lists,get_md,makerss,get_page_lists,get_achrives

mdpath = '/data0/pyprojects/ittech/wwwroot/mdblogpath/'
temppath = '/data0/pyprojects/ittech/wwwroot/theme'

loader = tornado.template.Loader(temppath)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
			(r"/page/([0-9]+\.html)", IndexPagesHandler),
			(r"/posts/([a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)",PostsHandler),
			(r"/topic/([a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)",TopicHandler),
			(r"/archives\.html",ArchivesHandler),
			(r"/feed", FeedHandler),
			(r"/google5a130ed8653a53b0\.html",GooHandler),
			(r"/(.+)",NotFoundHandler)
		]
		tornado.web.Application.__init__(self, handlers)


class BaseHandler(tornado.web.RequestHandler):
	def http404(self):
		self.set_status(404)
		self.write(loader.load("Light/404.htm").generate(htmlstring = []))
	

class FaviconHandler(BaseHandler):
	def get(self):
		self.set_status(404)
		return
		
class GooHandler(BaseHandler):
	def get(self):
		self.write(loader.load("google5a130ed8653a53b0.html").generate(htmlstring = []))
		return
		
class NotFoundHandler(BaseHandler):
	def get(self,args):
		self.http404()
		return
		
class IndexHandler(BaseHandler):
	def get(self,args = ''):
		if args == '':
			bloglists = get_blog_lists(mdpath)
			pages = get_page_lists(1)
			self.write(loader.load("Light/index.htm").generate(htmlstring = bloglists[0:9],pages = pages))
		else:
			self.http404()
			return

class IndexPagesHandler(BaseHandler):
	def get(self,args = ''):
		if args is not None:
			try:
				(pageid,ext) = args.split('.')
				if ext != 'html':
					self.http404()
					return
			except:
				pageid = 1
			curpage = int(pageid)
			if curpage == 1:
				self.redirect('/')
			bloglists = get_blog_lists(mdpath)
			pages = get_page_lists(curpage)
			start = (curpage - 1) * 10 - 1
			end = curpage * 10 -1
			self.write(loader.load("Light/index.htm").generate(htmlstring = bloglists[start:end],pages = pages))
		else:
			self.http404()
			return
			
class PostsHandler(BaseHandler):
	def get(self,args):
		try:
			(requestmdpath,ext) = args.split('.')
			if ext != 'html':
				self.http404()
				return
		except:
			requestmdpath = 'hello_world.md'
		mdfile = mdpath + requestmdpath + '.md'
		if os.path.exists(mdfile) is False:
			self.http404()
			return
		htmls = get_md(mdfile)
		self.write(loader.load("Light/posts.htm").generate(htmlstring = htmls))

class TopicHandler(BaseHandler):
	def get(self,args):
		try:
			(requestmdpath,ext) = args.split('.')
			if ext != 'html':
				self.http404()
				return
		except:
			requestmdpath = 'about.md'
		mdfile = mdpath + 'topic/' + requestmdpath + '.md'
		if os.path.exists(mdfile) is False:
			self.http404()
			return
		htmls = get_md(mdfile)
		self.write(loader.load("Light/topic.htm").generate(htmlstring = htmls))		

class ArchivesHandler(BaseHandler):
	def get(self):
		bloglists = get_achrives(mdpath)
		self.write(loader.load("Light/archives.htm").generate(htmlstring = bloglists))

class FeedHandler(BaseHandler):
	def get(self,args = ''):
		if args == '':
			bloglists = get_blog_lists(mdpath)
			self.write(makerss(bloglists[:20]))
		else:
			self.http404()
			return
		
host,port = ('0.0.0.0',8899)
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application(),xheaders = True)
	http_server.bind(port, host)
	http_server.start(num_processes = 0) 
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()