import main
import os
import webapp2
import logging
import data
import main

# Most handlers inherit from BaseHandler.
# This allows them to check login credentials easily
# as well as draw the page easily with all the dynamic content
# that is shared, like the currents.  
class BaseHandler(webapp2.RequestHandler):

	# A method for writing the HTML to the page. t_values is a dictionary
	# with values that will replace values in the HTML.
	def write_template(self, filename, t_values = {}, escape = True):
		template = None
		if escape:
			template = main.jinja_auto.get_template(filename)
		else:
			template = main.jinja_no_auto.get_template(filename)
		currents = main.get_currents()
		if currents == False:
			self.response.out.write(template.render(t_values))
		else:
			t_values['post1_title'] = currents['post1'][0]
			t_values['post1_content'] = currents['post1'][1]
			t_values['post1_url'] = "/blog" + currents['post1'][2]
			t_values['post2_title'] = currents['post2'][0]
			t_values['post2_content'] = currents['post2'][1]
			t_values['post2_url'] = "/blog" + currents['post2'][2]
			self.response.out.write(template.render(t_values))

	# This function will take a username and password and log the user in
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

	# check_login makes sure the user is logged in when viewing a page.
	# This is often done on restricted pages at the very begining.
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