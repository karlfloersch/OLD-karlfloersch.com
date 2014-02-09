#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import handlers
import random
import string
import hashlib
import re
import data
import h_static
import h_signup_login
import h_edit_posts
import h_blog_view
import logging
from google.appengine.ext import db
from google.appengine.api import memcache
from HTMLParser import HTMLParser


###
# USE FOR MAPPING PAGE TO HANDLER
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
    ('/', h_static.HomeHandler),
    ('/blog/?', h_blog_view.BlogHandler),
    ('/projects/?', h_static.ProjectsHandler),
    ('/contact/?', h_static.ContactHandler),
    ('/signup', h_signup_login.SignupHandler),
    ('/9z4b3ty6x9lxva0u3u19', h_signup_login.LoginHandler),
    ('/blog/newpost', h_edit_posts.EditPostHandler),
    ('/blog/_edit' + PAGE_RE, h_edit_posts.EditPostHandler),
    ('/blog/_delete' + PAGE_RE, h_edit_posts.DeletePostHandler),
    ('/blog' + PAGE_RE, h_blog_view.ViewPostHandler)
], debug=True)
#-	-	-	-	-	-	-	-	-#


###
#FOR USE WITH RENDERING STUFF SON
jinja_auto = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
jinja_no_auto = jinja2.Environment(autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
#-	-	-	-	-	-	-	-	-#


###
#RETURNS A LIST OF ALL THE POSTS ORDERED DECENDING#
def top_posts(update = False):
    key = 'top'
    posts = memcache.get(key)
    if posts is None or update:
        logging.error("DB QUERY")
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        posts = list(posts)
        memcache.set(key, posts)
    return posts
#-  -   -   -   -   -   -   -   -   -   -   -#



###
#FOR USE WITH GETTING THE CURRENTS SECTION INFO#
def get_currents():
    posts = top_posts()
    if len(posts) < 2:
        return False
    post1 = [posts[0].title, strip_tags(posts[0].content[:300]), posts[0].url]
    post2 = [posts[1].title, strip_tags(posts[1].content[:300]), posts[1].url]
    return {'post1': post1, 'post2': post2}
#-  -   -   -   -   -   -   -   -   -   -   -#


####
#FOR USE WITH USER DATABASE PASSWORD MAKING#
def make_salt():
    ans = ""
    for i in range(0,5):
        ans += random.choice(string.letters)
    return ans

def make_pw_hash(name, pw, salt = None):
    if salt is None:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)
#-	-	-	-	-	-	-	-	-	-	-	-#


####
#FOR USE WITH CHECKING IF INPUT WAS VALID FOR USERS#
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
#-	-	-	-	-	-	-	-	-	-	-	-	-#

# THIS IS FOR STRIPPING HTML FOR DISPLAY ON BLOG HOME   #
class MLStripper(HTMLParser):                           #
    def __init__(self):                                 #
        self.reset()                                    #
        self.fed = []                                   #
    def handle_data(self, d):                           #
        self.fed.append(d)                              #
    def get_data(self):                                 #
        return ''.join(self.fed)                        #
def strip_tags(html):                                   #
    s = MLStripper()                                    #
    s.feed(html)                                        #
    return s.get_data()                                 #
# THIS IS FOR STRIPPING HTML FOR DISPLAY ON BLOG HOME   #  
