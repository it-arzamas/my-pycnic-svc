from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError

from base_handler import CrudHandler
from models.client import Client as ClientModel

class Crud(CrudHandler, Handler):

	def __init__(self):
		super(Crud, self).__init__(ClientModel)


class Login(Handler):

	def post(self):
		try:
			ClientModel.setAttemptWith('clientid')
			result = ClientModel.validate(self.request.data)
			return result
		except Exception as e:
			raise HTTPError(401, "Unauthorized.")
		
