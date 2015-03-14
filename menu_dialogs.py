from PyQt4 import QtGui, QtCore, QtSql

class OpenDialog(QtGui.QDialog):
	"""
	Dialog for opening a table from the database.
	Suggests table names based on the result 'SHOW TABLES;' (table 'currencies' excluded).
	"""
	def __init__(self, db, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.setWindowTitle('Open table')

		query = QtSql.QSqlQuery()
		if not query.exec_('SHOW TABLES;'):
			QtGui.QMessageBox.critical(self, 'Database error', query.lastError().text())

		if query.size() == 1:  # one table 'currencies'
			QtGui.QMessageBox.information(self, 'Empty database', 'There are no tables in the database. Create a table first.')
			self.close()

		self.tables = QtGui.QComboBox(self)
		while query.next():
			if str(query.value(0).toString()) == 'currencies':
				continue
			self.tables.addItem(str(query.value(0).toString()), str(query.value(0).toString()))

		self.info = QtGui.QLabel('Select a table: ', self)

		self.ok = QtGui.QPushButton('ok', self)
		self.connect(self.ok, QtCore.SIGNAL('clicked()'), QtCore.SLOT('accept()'))

		self.cancel = QtGui.QPushButton('cancel', self)
		self.connect(self.cancel, QtCore.SIGNAL('clicked()'), QtCore.SLOT('reject()'))

		grid = QtGui.QGridLayout()
		grid.addWidget(self.info, 0, 0, 1, 2)
		grid.addWidget(self.tables, 1, 0, 1, 2)
		#grid.addWidget(QtGui.QLabel('', self), 2, 0, 1, 2)  # spacer
		grid.addWidget(self.ok, 3, 0, 1, 1)
		grid.addWidget(self.cancel, 3, 1, 1, 1)
		self.setLayout(grid)

	def get_tablename(self):
		"""
		Returns the previously during 'self.exec_()' chosen tablename.
		"""
		return str(self.tables.itemData(self.tables.currentIndex()).toString())


class SignInDialog(QtGui.QDialog):
	"""
	Dialog for signing-in to the database.
	Username, password, databasename and hostname can be specified. The latter two are defaulted.
	"""
	def __init__(self, db, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.setWindowTitle('Sign-In required')

		self.info = QtGui.QLabel('You\'re not signed in yet. Please sign in first: ', self)

		self.username = QtGui.QLineEdit(self)
		self.password = QtGui.QLineEdit(self)
		self.password.setEchoMode(QtGui.QLineEdit.Password)
		self.database = QtGui.QLineEdit(db.databaseName(), self)
		self.hostname = QtGui.QLineEdit(db.hostName(), self)

		self.username_label = QtGui.QLabel('username: ', self)
		self.password_label = QtGui.QLabel('password: ', self)
		self.database_label = QtGui.QLabel('database: ', self)
		self.hostname_label = QtGui.QLabel('hostname: ', self)

		self.remember_me = QtGui.QCheckBox(self)
		self.remember_me_label = QtGui.QLabel('remember me ', self)

		self.ok = QtGui.QPushButton('ok', self)
		self.connect(self.ok, QtCore.SIGNAL('clicked()'), QtCore.SLOT('accept()'))
		self.cancel = QtGui.QPushButton('cancel', self)
		self.connect(self.cancel, QtCore.SIGNAL('clicked()'), QtCore.SLOT('reject()'))

		grid = QtGui.QGridLayout()
		grid.addWidget(self.info, 0, 0, 2, 2)
		grid.addWidget(self.username_label, 2, 0, 1, 1)
		grid.addWidget(self.username, 2, 1, 1, 1)
		grid.addWidget(self.password_label, 3, 0, 1, 1)
		grid.addWidget(self.password, 3, 1, 1, 1)
		grid.addWidget(self.database_label, 4, 0, 1, 1)
		grid.addWidget(self.database, 4, 1, 1, 1)
		grid.addWidget(self.hostname_label, 5, 0, 1, 1)
		grid.addWidget(self.hostname, 5, 1, 1, 1)
		grid.addWidget(self.remember_me_label, 6, 0, 1, 1)
		grid.addWidget(self.remember_me, 6, 1, 1, 1)
		grid.addWidget(self.ok, 7, 0, 1, 1)
		grid.addWidget(self.cancel, 7, 1, 1, 1)
		self.setLayout(grid)

	def get_values(self):
		"""
		Returns the previously during 'self.exec_()' set values.
		"""
		return str(self.username.text()), str(self.password.text()), str(self.database.text()), str(self.hostname.text()), self.remember_me.isChecked()