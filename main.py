#!/usr/bin/env python

from google.appengine.api import users

from google.appengine.api import memcache

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from models import Person
from models import Schedule
from models import Expense

#import os

#ROOT_PATH = os.path.dirname(__file__)

#TEMPLATE_DIRS = (
  #ROOT_PATH + "/templates",
#)

## Well ... i've heard about django 1.2 ... but still can't use it!
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#from google.appengine.dist import use_library
#use_library('django', '1.2')
	
PERSON_EXPIRE_TIME = 360

########################################################################
##                     
##        HANDLERS: Home Handlers ... used to set schedules
##
########################################################################
class MainHandler(webapp.RequestHandler):
	def get(self):
		c_per = memcache.get('current_person')
		if not c_per:
			c_user = users.get_current_user()
		
			if not c_user:
				self.redirect(users.create_login_url(self.request.uri))
				return
		
			c_per = Person.gql("WHERE user = :1",c_user).get()
			if not c_per:
				c_per = Person( user = c_user )
			
			memcache.add('current_person',c_per,PERSON_EXPIRE_TIME)
			
		if not c_per.schedule:
			self.response.out.write(template.render('noscheds.html',{}))
		else:
			self.response.out.write(template.render('home.html',{}))
			
	def post(self):
		c_per = memcache.get('current_person')
		
		if not c_per:
			return # ERROR! Invalid attempt to post schedules
		if not c_per.schedule:
			return # ERROR! Person don't have an schedule ... probably an invalid attempt
		
		## TODO: Do a nice data validation?? could be JScript too ...
		exp = Expense( belongs = c_per,
	                 name = self.request.get('name'), 
	                 value = self.request.get('cost'),
	                 when = self.request.get('date'),
	                 description = self.request.get('desc') )
		exp.put()		
		memcache.set('current_person',c_per,PERSON_EXPIRE_TIME)
		
		self.redirect('/')

class ScheduleHandler(webapp.RequestHandler):
	def post(self, action):
		if action == 'create':
			c_per = memcache.get('current_person')
			
			if not c_per:
				return	# ERROR! Invalid attempt to post schedules
			if c_per.schedule:
				return # ERROR! Person already has an schedule ... probably an invalid attempt
			
			sched = Schedule()
			sched.put()
			c_per.schedule = sched
			c_per.put()
			
			memcache.set('current_person',c_per,PERSON_EXPIRE_TIME)
		
		self.redirect('/')
		
########################################################################
##                     
##                 Main Function and Boilerplates
##
########################################################################

def main():
	application = webapp.WSGIApplication([(r'/', MainHandler),
	                                      (r'/schedule/(.*)',ScheduleHandler)],
                                         debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
