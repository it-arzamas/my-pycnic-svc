from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError

from middlewares.jwt_middleware import JwtMiddleware

class CrudHandler(Handler):

	Orm = None

	jwtMiddleware = JwtMiddleware()

	def __init__(self, Model):
		self.Orm = Model

	@jwtMiddleware.requires_token()
	def get(self, id=None):
		jsonInput = self.request.json_args
		## record per page
		try:
			recPerPage = jsonInput['rp']
		except Exception as e:
			recPerPage = None
		## filters
		try:
			filter = jsonInput['f']
		except Exception as e:
			filter = None
		## search
		try:
			search = jsonInput['q']
		except Exception as e:
			search = None

		try:
			if id==None:
				result = self.Orm.getList(recPerPage, search, filter)
				return result
			else:
				result = self.Orm.getById(id)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(422, "Data not found.")

	@jwtMiddleware.requires_token()
	def post(self):
		try:
			result = self.Orm.addNew(self.request.data)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(422, "Create failed.")

	@jwtMiddleware.requires_token()
	def put(self, id):
		try:
			result = self.Orm.doUpdate(id, self.request.data)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(422, "Data not found.")

	@jwtMiddleware.requires_token()
	def delete(self, id):
		try:
			me = self.Orm.find(id)
			if me.delete():
				return "Deleted"
		except Exception as e:
			raise HTTPError(422, "Data not found.")
			