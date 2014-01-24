import main
import os
import webapp2
import logging
import handlers
import data
from google.appengine.ext import db
from google.appengine.api import memcache
from HTMLParser import HTMLParser

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
		for post in posts:
			post.title = '<a href="/blog'+ post.url +'">'+post.title+'</a>'
			post.content = strip_tags(post.content)
		self.write_template('blog-home.html',{'posts':posts}, False)


# THIS IS FOR STRIPPING HTML FOR DISPLAY ON BLOG HOME 	#
class MLStripper(HTMLParser):							#
	def __init__(self):									#
		self.reset()									#
		self.fed = []									#
	def handle_data(self, d):							#
		self.fed.append(d)								#
	def get_data(self):									#
		return ''.join(self.fed)						#
def strip_tags(html):									#
	s = MLStripper()									#
	s.feed(html)										#
	return s.get_data()									#
# THIS IS FOR STRIPPING HTML FOR DISPLAY ON BLOG HOME 	#


class ViewPostHandler(handlers.BaseHandler):
	def get(self, url = "/"):
		if url == '/':
			self.redirect("/blog")
			return
		posts = top_posts()

		for post in posts:
			# self.response.write(post.url+ " " + url + "<br>")
			if post.url == url:
				t_values = {'title_input':post.title,'content_input':post.content}
				self.write_template('blog-post.html',t_values,False)
				return
		# self.error(404)
		self.response.write("404 ERROR: Page not found.")


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
				self.redirect("/blog" + url)
				return


		a = data.Post(url = url, title = title, content = content)
		a.put()
		top_posts(True)
		self.redirect("/blog" + url)




class DeletePostHandler(handlers.BaseHandler):
	def get(self, url = "/"):
		if not self.check_login():
			self.redirect('/')
			return

		posts = top_posts()
		for post in posts:
			if post.url == url:
				post.delete
				top_posts(True)
				self.response.write("Post successfully deleted")
				return













