from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError
import jwt

from models.client import Client as ClientModel

class Login(Handler):

	def post(self):
		try:
			result = ClientModel.addNew(self.request.data)
			return result.to_dict()
		except Exception as e:
			raise HTTPError(403, "Unauthorized.")