from PyQt4 import QtGui, QtSql

class MySQLSetup:
	def __init__(self, db):
		self.db = db

	def setup_currencies(self):
		if not self.db.open():
			return False

		query = QtSql.QSqlQuery()

		if not query.exec_('SHOW TABLES;'):
			QtGui.QMessageBox.critical(self, 'Database error', query.lastError().text())
			return False

		while query.next():
			if str(query.value(0).toString()) == 'currencies':
				return True

		if not query.exec_('CREATE TABLE currencies (name CHAR(3), exchange_rate_to_EUR FLOAT);'):
			QtGui.QMessageBox.critical(self, 'Database error', query.lastError().text())
			return False

		if not query.exec_('INSERT INTO currencies (name, exchange_rate_to_EUR) VALUES (EUR, 1.0);'):
			QtGui.QMessageBox.critical(self, 'Database error', query.lastError().text())
			return False

		return True