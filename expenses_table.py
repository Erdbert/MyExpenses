import json
from PyQt4 import QtGui, QtCore, QtSql

import mysql_table_meta
from amount_styled_item_delegate import AmountStyledItemDelegate
import expensemodel
from expense_dialog import ExpenseDialog

class ExpensesTable(QtGui.QWidget):
	def __init__(self, tablename, db, mainwindow, parent):
		QtGui.QWidget.__init__(self, parent)
		#super(ExpensesTable, self).__init__()

		self.tablename = tablename
		self.db = db
		self.mainwindow = mainwindow

		self.order_by = 1
		self.order = QtCore.Qt.AscendingOrder

		self.table = QtGui.QTableView(self)
		self.model = expensemodel.ExpenseModel(tablename, db, self)
		self.model.setSort(self.order_by, self.order)
		self.table.setModel(self.model)
		self.table.hideColumn(0)
		self.table.setItemDelegateForColumn(4, AmountStyledItemDelegate(self))

		nrows = self.model.rowCount()
		self.categories = set()
		list_of_currencies = set(['EUR', 'CHF'])
		for row in range(nrows):
			self.categories.add(str(self.model.data(self.model.index(row, 2)).toString()))
			list_of_currencies.add(str(self.model.data(self.model.index(row, 5)).toString()))
		self.categories = list(self.categories)
		list_of_currencies = list(list_of_currencies)

		self.currencies = {}
		query = QtSql.QSqlQuery()
		for currency in list_of_currencies:
			query.exec_('SELECT exchange_rate_to_EUR from currencies WHERE name=\'' + currency + '\'')
			if not query.next():
				QtGui.QMessageBox.critical(self, 'Unregistered currency', 'The currency \'' + currency + '\' is not registered in the database.')
				break
			else:
				self.currencies[currency] = float(query.value(0).toString())

		self.add_expense_button = QtGui.QPushButton(QtGui.QIcon('icons/plus.jpg'), 'Add Expense', self)
		self.connect(self.add_expense_button, QtCore.SIGNAL('clicked()'), self.add_expense)

		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.table)
		self.vbox.addWidget(self.add_expense_button)

		self.setLayout(self.vbox)

		#connect horizontal header for ordering the table
		self.connect(self.table.horizontalHeader(), QtCore.SIGNAL('sectionClicked(int)'), self.change_ordering)

		#connect vertical header for context menu for the expenses
		self.connect(self.table.verticalHeader(), QtCore.SIGNAL('sectionClicked(int)'), self.context_menu)

		#sort after date:
		self.model.setSort(1, QtCore.Qt.AscendingOrder)
		self.model.select()

	def context_menu(self, section):
		mouse_pos = QtGui.QCursor.pos()
		menu = QtGui.QMenu(self)
		mremove = menu.addAction('Remove expense')
		if menu.exec_(mouse_pos) == mremove:
			if not self.model.query().exec_('DELETE FROM ' + self.model.tablename + ' WHERE ' + mysql_table_meta.columns[0] + '=' + str(self.model.data(self.model.index(section, 0)).toString()) + ';'):
				QtGui.QMessageBox.critical(self, 'Database error', self.model.query.lastError().text())
			else:
				self.model.select()

	def change_ordering(self, section):
		if self.order_by == section:
			self.model.setSort(section, (self.order+1)%2)
			self.order = (self.order+1)%2
		else:
			self.model.setSort(section, QtCore.Qt.AscendingOrder)
			self.order = QtCore.Qt.AscendingOrder
		self.model.select()
		self.order_by = section

	def save(self, filename):
		data = []
		for expense in self.list.expenses:
			data += [expense.get_content()]
		print "data to be saved: "
		print data
		with open(filename, 'w') as fp:
			json.dump(data, fp)

		self.filename = filename
		self.list.filename = filename

	def add_expense(self):
		dialog = ExpenseDialog(self.categories, self.currencies, self)
		if dialog.exec_():
			entry = dialog.get_values()
			self.categories, currencies_added = dialog.update_lists()

			if currencies_added.keys():
				for currency in currencies_added.keys():
					if not self.mode.query().exec_("INSERT INTO currencies VALUES (\'" + currency + "\', " + currencies_added[currency] + ");"):
						QtGui.QMessageBox.critical(self, 'Database Error', self.model.lastError().text())
				self.currencies.update(currencies_added)

			if not self.model.query().exec_("INSERT INTO " + self.tablename + " VALUES (0," + ",".join(entry) + ");"):
				QtGui.QMessageBox.critical(self, 'Database Error', self.model.lastError().text())
			else:
				#self.model.query().next()
				self.model.select()

	def get_expenses(self):
		nrows = self.model.rowCount()
		ncols = self.model.columnCount()
		data = []
		for row in range(nrows):
			expense = []
			for col in range(1,ncols):
				expense.append(str(self.model.data(self.model.index(row, col)).toString()))
			data.append(expense)

		return data