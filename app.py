## GLOBAL MODULES
from pycnic.core import WSGI

## PROJECT MODULES
from handlers import client

############# LOG HANDLER

import logging

logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query %(query)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

############# APP

class app(WSGI):
	debug = True
	routes = [
    	# ('/', client.Client()),
    	('/client', client.Client()),
    	('/client/([\w]+)', client.Client())
	]

