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

	def check_login(self):
		user_cookie = self.request.cookies.get('user', '0')
		if not "|" in user_cookie:
			return False
		c = user_cookie.split('|')
		if len(c) < 2:
			return False
		user_id = c[0]
		user_hash = c[1]
		if not user_id.isdigit():
			return False
		user = data.User.get_by_id(int(user_id))
		if user is None:
			return False
		correct_hash = user.password_hash.split('|')[0]
		correct_cookie = "%s|%s" % (user_id, correct_hash)

		if not correct_cookie == user_cookie:
			return False
		return True