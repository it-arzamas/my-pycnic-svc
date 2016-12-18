from functools import wraps
from pycnic.core import Handler
from pycnic.errors import HTTPError
import jwt, ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("./config/app.ini")
JWTsecret = Config.get("JWT", "secret")

class JwtMiddleware(Handler):

	def get_token(self, request):
		try:
			strAuth = request.get_header("Authorization")
			strToken = strAuth.replace("Bearer ", "")
			if jwt.decode(strToken, JWTsecret):
				return True
			else:
				return None
		except Exception as e:
			HTTPError(403, "Forbidden")

	def requires_token(self):
		""" Wrapper for methods that require login """
		def wrapper(f):
			@wraps(f)
			def wrapped(*args, **kwargs):
				if not self.get_token(args[0].request):
					raise HTTPError(403, "Forbidden")
				return f(*args, **kwargs)
			return wrapped
		return wrapper		