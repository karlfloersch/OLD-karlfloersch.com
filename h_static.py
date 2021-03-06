import webapp2
import jinja2
import os
import handlers
import data
import main

# Simple classes for basic HTML pages without any dynamic content.

class MainHandler(handlers.BaseHandler):
	def get(self):
		self.write_template('base.html')

class HomeHandler(handlers.BaseHandler):
	def get(self):
		self.write_template('home.html')

class ProjectsHandler(handlers.BaseHandler):
	def get(self):
		self.write_template('project-page.html')

class ContactHandler(handlers.BaseHandler):
	def get(self):
		self.write_template('contact.html')