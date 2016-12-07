# from db import db
# from orator import Model, Schema
# import logging
from crud_base import CrudBaseModel

class Client(CrudBaseModel):
	__table__ = 'clients'
	__primary_key__ = 'client_id'
	__incrementing__  = False
	__fillable__ = [ 'client_id', 'client_name', 'client_secret', 'client_active' ]

	srcRawQry = ""
	srcQryBind = []
	
	## Override parent method for spesific search query
	@classmethod
	def setSrcRawQry(self, strSearch):
		self.srcRawQry = "client_id LIKE %s"
		self.srcQryBind = [ "%"+strSearch+"%" ]