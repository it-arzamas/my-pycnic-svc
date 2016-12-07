import json

from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError

from models.client import Client as ClientModel

class Client(Handler):

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
				result = ClientModel.getList(recPerPage, search, filter)
				return result
			else:
				result = ClientModel.getById(id)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(422, "Data not found.")

	def post(self):
		try:
			result = ClientModel.addNew(self.request.data)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(422, "Create failed.")

	def put(self, id):
		try:
			result = ClientModel.doUpdate(id, self.request.data)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(422, "Data not found.")

	def delete(self, id):
		try:
			me = ClientModel.find(id)
			if me.delete():
				return "Deleted"
		except Exception as e:
			raise HTTPError(422, "Data not found.")
			