import main
import os
import re
import webapp2
import jinja2
import random
import string
import hashlib
from google.appengine.ext import db


class User(db.Model):
	username = db.StringProperty(required = True)
	password_hash = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)



class Post(db.Model):
	url = db.StringProperty(required = True)
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	tags = db.StringProperty(required = True)
	category = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

class Comment(db.Model):
	parrent_post = db.ReferenceProperty(Post, required = True)
	nickname = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
