import main
import os
import webapp2
import logging
import handlers
import data
from google.appengine.ext import db

# Draws the Blog section which is just a list of the most recent
# posts.  It currently just displays all the posts.
class BlogHandler(handlers.BaseHandler):
	def get(self):
		posts = main.top_posts()
		for post in posts:
			post.title = '<a href="/blog'+ post.url +'">'+post.title+'</a>'
			post.content = main.strip_tags(post.content)
		self.write_template('blog-home.html',{'posts':posts}, False)

# This just fills the page with the post's content.
class ViewPostHandler(handlers.BaseHandler):
	def get(self, url = "/"):
		if url == '/':
			self.redirect("/blog")
			return
		posts = main.top_posts()

		for post in posts:
			if post.url == url:
				t_values = {'title_input':post.title,'content_input':post.content, 'date_input': post.created.date()}
				self.write_template('blog-post.html',t_values,False)
				return
		self.response.write("404 ERROR: Page not found.")