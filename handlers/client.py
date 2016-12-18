from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError
import jwt, datetime, ConfigParser

from base_handler import CrudHandler
from models.client import Client as ClientModel
from middlewares.jwt_middleware import JwtMiddleware

class Crud(CrudHandler, Handler):

	def __init__(self):
		super(Crud, self).__init__(ClientModel)


class Token(Handler):

	Config = ConfigParser.ConfigParser()
	Config.read("./config/app.ini")
	JWTsecret = Config.get("JWT", "secret")
	JWTlifetime = Config.getint("JWT", "lifetime")

	jwtMiddleware = JwtMiddleware()

	def post(self):
		try:
			# Validate Client
			ClientModel.setAttemptWith('clientid')
			result = ClientModel.validate(self.request.data)
			payLoad = { 
				"iat": datetime.datetime.utcnow(),
				"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.JWTlifetime),
				"auth_object": result 
			}
			return { "token": jwt.encode(payLoad, self.JWTsecret, algorithm='HS256') }
		except Exception as e:
			raise HTTPError(401, "Unauthorized.")
	
	@jwtMiddleware.requires_token()
	def get(self):
		strAuth = self.request.get_header("Authorization")
		strToken = strAuth.replace("Bearer ", "")
		return { "payload": jwt.decode(strToken, self.JWTsecret) }
		
