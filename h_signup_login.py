import main
import os
import webapp2
import logging
import handlers
import data

# LoginHandler displays the login screen and posted with
# login credentials, will check to see if they are valid.
class LoginHandler(handlers.BaseHandler):
	def get(self):
		self.write_login()

	# Get input and check if that user exists
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		if self.login_user(username, password):
			self.redirect('/')
		else:
			self.write_login(username, "Invalid Login.")

	# Draw the login screen. Very simple with user and pass
	def write_login(self, username = "", error = ""):
		t_values = {
			'username': username,
			'error': error
		}
		self.write_template("login.html", t_values)


# SignupHandler allows for people to sign up.
# However, this is not activated normally and only
# opens up when I want to make a new admin or something.
class SignupHandler(handlers.BaseHandler):
	# If we need a new admin, draw the signup forum
	# Otherwise, just return the person back to home.
	def get(self):
		needNewAdmin = False;
		if needNewAdmin:
			self.write_form()
		else:
			self.redirect('/')

	# Assuming we need an admin, this will take the info
	# and check it for errors, then add a hashed version
	# to the database.
	def post(self):
		needNewAdmin = False;
		if not needNewAdmin:
			self.redirect('/')

		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		info_pack = self.check_info(username, password, verify, email)

		#if info was valid
		if info_pack[0]:
			self.add_user(username, password, email)
			self.redirect('/')
		else: #else info was not valid
			self.write_form(info_pack[1])

	# This creates a user with that user and password
	# then adds it to the database
	def add_user(self, username, password, email):
		password_hash = main.make_pw_hash(username, password)

		a = None
		if email != "":
			a = data.User(username = username, password_hash = password_hash, email = email)
		else:
			a = data.User(username = username, password_hash = password_hash)
		a.put()
		self.login_user(username,password)

	# This just validates the user's input
	def check_info(self, username, password, verify, email):
		have_error = False

		t_values = {
			'username': username,
			'email': email,
			'error_username': "",
			'error_password': "",
			'error_verify': "",
			'error_email': ""
		}
		user = data.User.all().filter("username =", username).get()
        #("SELECT * FROM User WHERE username = \'%s\'" % username).get()

		if not main.valid_username(username):
			t_values['error_username'] = "That's not a valid username."
			have_error = True
		elif user is not None:
			t_values['error_username'] = "That user already exists."
			have_error = True

		if not main.valid_password(password):
			t_values['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password != verify:
			t_values['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not main.valid_email(email):
			t_values['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			return (False, t_values)
		return (True, t_values)

	# A method for writing the form easily
	def write_form(self, t_values = {'username': '',
		'email': '',
		'error_username': '',
		'error_password': '',
		'error_verify': '',
		'error_email': ''}):
		
		self.write_template("signup-form.html", t_values)


