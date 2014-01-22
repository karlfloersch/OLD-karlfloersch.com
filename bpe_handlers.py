import main
import os
import webapp2
import logging
import handlers
import data
from google.appengine.ext import db
from google.appengine.api import memcache

def top_posts(update = False):
	key = 'top'
	posts = memcache.get(key)
	if posts is None or update:
		logging.error("DB QUERY")
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
		posts = list(posts)
		memcache.set(key, posts)
	return posts

class BlogHandler(handlers.BaseHandler):
	def get(self):
		posts = top_posts()
		self.write_template('blog-home.html',{'posts':posts})
		



class EditPostHandler(handlers.BaseHandler):

	def get(self, url = "/"):
		if not self.check_login():
			self.redirect('/')
			return
		if url == '/':
			self.write_template('make-post.html')
			return
		else:
			posts = top_posts()
			for post in posts:
				if post.url == url:
					title = post.title
					content = post.content
					self.write_template('make-post.html', {'title_input': title, 'content_input': content})
					return
		self.redirect('/blog/newpost')

	def post(self, url = "/"):
		if not self.check_login():
			self.redirect('/')
			return
		
		title = self.request.get('title')
		url = str('/' + title.replace(' ', '_'))
		content = self.request.get('content')
		if title.strip() == "" or content.strip() == "":	
			self.write_new_post(title,content, "title and content please!")
			return
		posts = top_posts()
		for post in posts:
			if post.title == title:
				post.content = content
				post.put()
				top_posts(True)
				self.redirect("/")
				return


		a = data.Post(url = url, title = title, content = content)
		a.put()
		top_posts(True)
		self.redirect("/blog")

