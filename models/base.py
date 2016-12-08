from db import db
from orator import Model, Schema
import logging, hashlib

db.connection().enable_query_log()

Model.set_connection_resolver(db)
schema = Schema(db)

class CrudBase(Model):

	srcRawQry = ""
	srcQryBind = []

	@classmethod
	def setSrcRawQry(self, strSearch):
		self.srcRawQry = "%s = %s"
		self.srcQryBind = [ strSearch, strSearch ]

	@classmethod
	def getList(self, recPerPage=25, search=None, filter={}):
		me = self
		table = me.__table__
		# Filter
		if len(filter):
			for k, v in filter.iteritems():
				if schema.has_column(table, k) and (v != None and v != ''):
					me = me.where(k, v)
		# Search
		if search != None and search != '':
			self.setSrcRawQry(search)
			me = me.where(
				me.where_raw(self.srcRawQry, self.srcQryBind)
			)
		paged = me.paginate(recPerPage,0)
		result = {
			"total": paged.total,
			"per_page": paged.per_page,
			"current_page": paged.current_page,
			"last_page": paged.last_page,
			"prev_page": paged.previous_page,
			"next_page": paged.next_page,
			"data": paged.to_dict()
		}
		return result

	@classmethod
	def getById(self, id):
		return self.find(id)

	@classmethod
	def addNew(self, data):
		me = self()
		cols = schema.get_column_listing(me.__table__)
		for v in me.__fillable__:
			setattr(me, v, data[v])
		me.save()
		savedId = getattr(me,me.__primary_key__)
		return me.getById(savedId)

	@classmethod
	def doUpdate(self, id, data):
		me = self.find(id)
		for v in schema.get_column_listing(self.__table__):
			try:
				setattr(me, v, data[v])
			except Exception as e:
				pass
		me.save()
		savedId = getattr(me,self.__primary_key__)
		return self.getById(savedId)


class AuthenticableBase(Model):

	__attemptWith = 'email'

	@classmethod
	def setAttemptWith(self, strType):
		self.__attemptWith = strType

	@classmethod
	def validate(self, dcData):
		authSubject = None
		if self.__attemptWith=='email':
			hashed = self.hashPassword(dcData['password'])
			authSubject = self.where('email', dcData['email']).where('password', hashed).first()
		elif self.__attemptWith=='username':
			hashed = self.hashPassword(dcData['password'])
			authSubject = self.where('username', dcData['username']).where('password', hashed).first()
		elif self.__attemptWith=='clientid':
			authSubject = self.where('client_id', dcData['client_id']).where('client_secret', dcData['client_secret']).first()
		else:
			hashed = self.hashPassword(dcData['password'])
			authSubject = self.where('email', dcData['email']).where('password', hashed).first()
		return authSubject.to_dict()

	@classmethod
	def hashPassword(self, strPassword):
		return hashlib.sha256(strPassword).hexdigest()
