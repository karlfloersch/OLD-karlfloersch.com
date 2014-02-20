import main
import os
import webapp2
import logging
import handlers
import data
from google.appengine.ext import db

# This class checks if the user is signed in, and then
# if he is sends the edit post page filled with the post's
# content.  It will then accept changes and update immediately
class EditPostHandler(handlers.BaseHandler):

	# Checks login, if true draws the edit post page with the
	# input from the post being edited, or not if it's a new post.
	def get(self, url = "/"):
		if not self.check_login():
			self.redirect('/')
			return
		if url == '/':
			self.write_template('make-post.html')
			return
		else:
			posts = main.top_posts()
			for post in posts:
				if post.url == url:
					title = post.title
					content = post.content
					tags = post.tags
					category = post.category
					self.write_template('make-post.html', {'title_input': title, 'content_input': content, 'tags_input': tags, 'category_input': category})
					return
		self.redirect('/blog/newpost')

	# Checks the post's content to be complete and if it is
	# it saves the post to the database.
	def post(self, url = "/"):
		if not self.check_login():
			self.redirect('/')
			return

		title = self.request.get('title')
		url = str('/' + title.replace(' ', '_'))
		content = self.request.get('content')
		tags = self.request.get('tags')
		category = self.request.get('category')

		if title.strip() == "" or content.strip() == "" or tags.strip() == "" or category.strip() == "":	
			self.write_template('make-post.html',{'title_input': title, 'content_input': content, 'tags_input': tags, 'category_input': category, 'error': "fill out all forms!"})
			return
		posts = main.top_posts()
		for post in posts:
			if post.title == title:
				post.content = content
				post.tags = tags
				post.category = category
				post.put()
				main.top_posts(True)
				self.redirect("/blog" + url)
				return

		a = data.Post(url = url, title = title, content = content, tags = tags, category = category)
		a.put()
		main.top_posts(True)
		self.redirect("/blog" + url)



# This class is supposed to delete the post
# from the database but currently doesn't work.
class DeletePostHandler(handlers.BaseHandler):
	def get(self, url = "/"):
		if not self.check_login():
			self.redirect('/')
			return
		posts = main.top_posts()
		for post in posts:
			if post.url == url:
				post.delete
				main.top_posts(True)
				self.response.write("Post successfully deleted")
				return













