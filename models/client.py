from base import CrudBase, AuthenticableBase

class Client(CrudBase, AuthenticableBase):
	__table__ = 'clients'
	__primary_key__ = 'client_id'
	__incrementing__  = False
	__fillable__ = [ 'client_id', 'client_name', 'client_secret', 'client_active' ]

	srcRawQry = ""
	srcQryBind = []

	def __init__(self):
		CrudBase.__init__(self)
		AuthenticableBase.__init__(self)
	
	## Override parent method for spesific search query
	@classmethod
	def setSrcRawQry(self, strSearch):
		self.srcRawQry = "client_id LIKE %s OR client_name LIKE %s"
		self.srcQryBind = [ "%"+strSearch+"%", "%"+strSearch+"%" ]
