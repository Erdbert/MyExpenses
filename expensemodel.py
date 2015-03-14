import sys
from PyQt4 import QtGui, QtCore, QtSql

import mysql_table_meta

class ExpenseModel(QtSql.QSqlTableModel):
	def __init__(self, tablename, db, parent=None):
		QtSql.QSqlTableModel.__init__(self, parent, db)

		self.tablename = tablename
		self.setTable(tablename)
		#self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
		self.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.select()
		count = 0
		for col in mysql_table_meta.columns:
			self.setHeaderData(count, QtCore.Qt.Horizontal, col)
			count += 1