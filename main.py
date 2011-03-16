#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class Shout( db.Model ):
	message = db.StringProperty( required=True )
	when	= db.DateTimeProperty( auto_now_add=True )
	who		= db.StringProperty()

class MainHandler(webapp.RequestHandler):
	def get(self):
		shouts = db.GqlQuery('SELECT * FROM Shout '
							'ORDER BY when ASC')
		values = {'shouts' : shouts }
		self.response.out.write(template.render('main.html',values))

	def post(self):		
		sh = Shout( message = self.request.get('message'),
					who = self.request.get('who'))
		sh.put()
		self.redirect('/')
	
def main():
	application = webapp.WSGIApplication([('.*', MainHandler)],
                                         debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
