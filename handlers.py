import main
import os
import webapp2
import logging
import data

class BaseHandler(webapp2.RequestHandler):
	def write_template(self, filename, t_values = {}, escape = True):
		template = None
		if escape:
			template = main.jinja_auto.get_template(filename)
		else:
			template = main.jinja_no_auto.get_template(filename)

		self.response.out.write(template.render(t_values))

	def login_user(self, username, password):
		has_error = False
		user = data.User.all().filter("username =", username).get()
		
		if user is None:
			has_error = True
		elif not main.valid_pw(username, password, user.password_hash):
			has_error = True

		if has_error:
			return False

		pw_hash = user.password_hash.split('|')[0]

		user_cookie = "%s|%s" % (str(user.key().id()), pw_hash)
		self.response.headers.add_header('Set-Cookie', 'user=%s; Path=/' % str(user_cookie))
		return True