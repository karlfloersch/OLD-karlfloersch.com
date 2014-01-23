import webapp2
import jinja2
import os
import handlers


class MainHandler(handlers.BaseHandler):
    def get(self):
        self.write_template('base.html')


class HomeHandler(handlers.BaseHandler):
    def get(self):
        self.write_template('home.html')

class ProjectsHandler(handlers.BaseHandler):
    def get(self):
        self.write_template('project-page.html')