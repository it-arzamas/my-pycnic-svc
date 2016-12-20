from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError
import jwt, datetime, ConfigParser, emails

from middlewares.jwt_middleware import JwtMiddleware

class Email(Handler):

	Config = ConfigParser.ConfigParser()
	Config.read("./config/app.ini")

	JWTsecret = Config.get("JWT", "secret")
	JWTlifetime = Config.getint("JWT", "lifetime")

	jwtMiddleware = JwtMiddleware()
	
	@jwtMiddleware.requires_token()
	def post(self):
		try:
			dcInput = self.request.data

			m = emails.Message(subject=dcInput['subject'],
								html=dcInput['message'],
								mail_from=(self.Config.get("SMTP", "from_name"), self.Config.get("SMTP", "from_address")))

			sendIt = m.send(to=dcInput['to'].split(','),
					smtp={"host": self.Config.get("SMTP", "host"), "port": self.Config.get("SMTP", "port"), "ssl": self.Config.get("SMTP", "ssl"), "user": self.Config.get("SMTP", "user"), "password": self.Config.get("SMTP", "pass")})

			return { "result": "email send" }
		except Exception as e:
			raise e
		
