########################################################################
##                    DATABASE MODELS
##
########################################################################

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Schedule( db.Model ):
	since = db.DateTimeProperty( auto_now=True )
	start_value = db.FloatProperty( default=0.0 )
	
class Person( db.Model ):
	user = db.UserProperty( required=True )
	schedule = db.ReferenceProperty( Schedule,
	                                 collection_name='partners' )
		
class Project( db.Model ):
	name = db.StringProperty( required=True )
	owner = db.ReferenceProperty( Person,
	                              collection_name='project_portfolio')
		
class Expense( db.Model ):
	name        = db.StringProperty( required=True )
	value       = db.FloatProperty( required=True, default=0.0 )
	description = db.StringProperty()
	when        = db.DateTimeProperty()
	belongs     = db.ReferenceProperty( Schedule,
	                                    collection_name='expenditures' )