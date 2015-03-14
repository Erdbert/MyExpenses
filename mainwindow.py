#import sys
from PyQt4 import QtGui, QtCore, QtSql

try:  # check if connection details from the last session are available.
	import mysql_connection_details
except:
	with open('mysql_connection_details.py', 'w') as fp:
		fp.write('username=\'\'\npassword=\'\'\ndatabasename=\'myexpenses\'\nhostname=\'localhost\'')
	import mysql_connection_details

import language_sheet_en as language_sheet
import icon_paths
import mysql_table_meta
from menu_dialogs import OpenDialog, SignInDialog
from expenses_table import ExpensesTable
from visualization2_1 import VisualizationMonths, VisualizationCategories, VisualizationTree
from mysqlsetup import MySQLSetup

class MainWindow(QtGui.QMainWindow):
	"""
	MainWindow class. Controls the top-level actions on tables as well as the sign-in to the MySQL-database. Contains:
		- MenuBar with:
			- new table
			- open table
			- close table
			- exit application
			- add expense to current table
			- visualize current table grouped by months
			- visualize current table grouped by categories
		- ToolBar with:
			- same as MenuBar
			- Log-In to MySQL-database
		- QTabWidget to provide display of multiple tables (central widget)
		- StatusBar to display the current (top level) status of the application
	"""
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		#super(MainWindow, self).__init__()

		#self.setGeometry(QtGui.QDesktopWidget().screenGeometry())
		self.setGeometry(50, 50, 1000, 600)
		self.setWindowTitle('MyExpenses')

		self.statusBar().showMessage(language_sheet.statusbar.intro)

		#creating menubar
		menubar = self.menuBar()

		#menu file
		mfile = menubar.addMenu(language_sheet.menubar_sections.table)

		#action new
		mfile_new = QtGui.QAction(QtGui.QIcon(icon_paths.new_table), language_sheet.new_table.title, self)
		mfile_new.setShortcut(language_sheet.new_table.shortcut)
		mfile_new.setStatusTip(language_sheet.new_table.statustip)
		self.connect(mfile_new, QtCore.SIGNAL('triggered()'), self.new_file)

		mfile.addAction(mfile_new)

		#action open
		mfile_open = QtGui.QAction(QtGui.QIcon(icon_paths.open_table), language_sheet.open_table.title, self)
		mfile_open.setShortcut(language_sheet.open_table.shortcut)
		mfile_open.setStatusTip(language_sheet.open_table.statustip)
		self.connect(mfile_open, QtCore.SIGNAL('triggered()'), self.open_file)

		mfile.addAction(mfile_open)

		#action dump
		mfile_dump = QtGui.QAction(QtGui.QIcon(icon_paths.dump_table), 'Dump as json', self)
		mfile_dump.setShortcut('Ctrl+D')
		mfile_dump.setStatusTip('Save the expenses of the current table as json file')
		self.connect(mfile_dump, QtCore.SIGNAL('triggered()'), self.dump_file)

		mfile.addAction(mfile_dump)

		#action save  # commented because QSqlTableModel is configured to save-on-edit thus no manual saving of data is required.
		# mfile_save = QtGui.QAction('Save', self)
		# mfile_save.setShortcut('Ctrl+S')
		# mfile_save.setStatusTip('Saves the current expenses table')
		# self.connect(mfile_save, QtCore.SIGNAL('triggered()'), self.save_file)

		# mfile.addAction(mfile_save)

		#action close
		mfile_close = QtGui.QAction(QtGui.QIcon(icon_paths.close_table), language_sheet.close_table.title, self)
		mfile_close.setShortcut(language_sheet.close_table.shortcut)
		mfile_close.setStatusTip(language_sheet.close_table.statustip)
		self.connect(mfile_close, QtCore.SIGNAL('triggered()'), self.close_file)

		mfile.addAction(mfile_close)

		#action exit
		mfile_exit = QtGui.QAction(QtGui.QIcon(icon_paths.exit_application), language_sheet.exit_application.title, self)
		mfile_exit.setShortcut(language_sheet.exit_application.shortcut)
		mfile_exit.setStatusTip(language_sheet.exit_application.statustip)
		self.connect(mfile_exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

		mfile.addSeparator()
		mfile.addAction(mfile_exit)

		#menu edit
		medit = menubar.addMenu(language_sheet.menubar_sections.edit)

		#action add_expense
		medit_add_expense = QtGui.QAction(QtGui.QIcon(icon_paths.add_expense), language_sheet.add_expense.title, self)
		medit_add_expense.setShortcut(language_sheet.add_expense.shortcut)
		medit_add_expense.setStatusTip(language_sheet.add_expense.statustip)
		self.connect(medit_add_expense, QtCore.SIGNAL('triggered()'), self.add_expense)

		medit.addAction(medit_add_expense)

		#menu Visualization
		mvisualize = menubar.addMenu(language_sheet.menubar_sections.visualization)

		#action plot_histogram_months
		mvisualize_months = QtGui.QAction(QtGui.QIcon(icon_paths.grouped_by_months), language_sheet.grouped_by_months.title, self)
		#mvisualize_histogram_months.setShortcut(language_sheet.grouped_by_months.shortcut)
		mvisualize_months.setStatusTip(language_sheet.grouped_by_months.statustip)
		self.connect(mvisualize_months, QtCore.SIGNAL('triggered()'), self.visualize_months)

		mvisualize.addAction(mvisualize_months)

		#action plot_histogram_categories
		mvisualize_categories = QtGui.QAction(QtGui.QIcon(icon_paths.grouped_by_categories), language_sheet.grouped_by_categories.title, self)
		#mvisualize_histogram_categories.setShortcut(language_sheet.grouped_by_categories.shortcut)
		mvisualize_categories.setStatusTip(language_sheet.grouped_by_categories.statustip)
		self.connect(mvisualize_categories, QtCore.SIGNAL('triggered()'), self.visualize_categories)

		mvisualize.addAction(mvisualize_categories)

		#action plot_tree
		mvisualize_tree = QtGui.QAction(QtGui.QIcon("icons/tree2.png"), "Tree view", self)
		#mvisualize_histogram_categories.setShortcut(language_sheet.grouped_by_categories.shortcut)
		mvisualize_tree.setStatusTip("Plot expenses in a tree view.")
		self.connect(mvisualize_tree, QtCore.SIGNAL('triggered()'), self.visualize_tree)

		mvisualize.addAction(mvisualize_tree)

		#toolbar
		self.tlog_in = QtGui.QAction(QtGui.QIcon(icon_paths.login_required), language_sheet.log_in.title, self)
		self.tlog_in.setShortcut(language_sheet.log_in.shortcut)
		self.tlog_in.setStatusTip(language_sheet.log_in.statustip)
		self.connect(self.tlog_in, QtCore.SIGNAL('triggered()'), self.sign_in)
		self.toolbar_login = self.addToolBar('')
		self.toolbar_login.addAction(self.tlog_in)
		self.toolbar_login.addSeparator()
		self.toolbar_login.addAction(mfile_new)
		self.toolbar_login.addAction(mfile_open)
		self.toolbar_login.addAction(mfile_dump)
		self.toolbar_login.addAction(mfile_close)
		self.toolbar_login.addAction(mfile_exit)
		self.toolbar_login.addSeparator()
		self.toolbar_login.addAction(medit_add_expense)
		self.toolbar_login.addSeparator()
		self.toolbar_login.addAction(mvisualize_months)
		self.toolbar_login.addAction(mvisualize_categories)
		self.toolbar_login.addAction(mvisualize_tree)

		#tabs for different tables
		self.tabs = QtGui.QTabWidget(self)
		self.setCentralWidget(self.tabs)

		#meta data  # meta deta is taken from the respective MySQL-table
		# self.currencies = {'EUR': 1.0, 'CHF': 1.22}
		# self.categories = ['food', 'party', 'cinema', 'lunch', 'dinner']

		#variables  # stores the references to the visualization pop-ups to prevent auto remove by the garbage collector due to missing references
		self.popups = []

		#mysql-connection
		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')  # connect to a MySQL-database
		try:  # if available take stored values from the last session
			self.db.setUserName(mysql_connection_details.username)
			self.db.setPassword(mysql_connection_details.password)
			self.db.setDatabaseName(mysql_connection_details.databasename)
			self.db.setHostName(mysql_connection_details.hostname)
		except AttributeError, NameError:
			self.db.setUserName('')
			self.db.setPassword('')
			self.db.setDatabaseName('myexpenses')
			self.db.setHostName('localhost')

		if self.db.open():
			self.tlog_in.setIcon(QtGui.QIcon(icon_paths.login_successful))
			self.tlog_in.setToolTip(language_sheet.log_in.tooltip_login_successful(self.db.userName(), self.db.databaseName(), self.db.hostName()))
			setup = MySQLSetup(self.db)
			setup.setup_currencies()
		else:
			self.tlog_in.setToolTip(language_sheet.log_in.tooltip_login_required)
			self.statusBar().showMessage(language_sheet.statusbar.not_signed_in)

	def sign_in(self):
		"""
		Sign-in to the MySQL-database.
		Username, password, databasename and hostname can be specified. The latter two are defaulted.
		Returns the status of the sign-in in form of a string.
		"""
		sign_in_dialog = SignInDialog(self.db, self)
		if sign_in_dialog.exec_():
			sign_in_data = sign_in_dialog.get_values()
			self.db.setUserName(sign_in_data[0])
			self.db.setPassword(sign_in_data[1])
			self.db.setDatabaseName(sign_in_data[2])
			self.db.setHostName(sign_in_data[3])

			if sign_in_data[4]:
				with open('mysql_connection_details.py', 'w') as fp:
					fp.write('username=\''+sign_in_data[0]+'\'\npassword=\''+sign_in_data[1]+'\'\ndatabasename=\''+sign_in_data[2]+'\'\nhostname=\''+sign_in_data[3]+'\'')

			if self.db.open() == False:
				self.tlog_in.setIcon(QtGui.QIcon(icon_paths.login_required))
				QtGui.QMessageBox.critical(self, language_sheet.log_in_failed.title, language_sheet.log_in_failed.conditional_message(' (' + sign_in_data[0] + '@' + sign_in_data[2] + '.' + sign_in_data[3] + ').'))
				self.tlog_in.setToolTip(language_sheet.log_in.tooltip_login_required)
				self.statusBar().showMessage(language_sheet.statusbar.sign_in_failed)
				return 'failed'
			else:
				self.tlog_in.setIcon(QtGui.QIcon(icon_paths.login_successful))
				self.tlog_in.setToolTip(language_sheet.log_in.tooltip_login_successful(self.db.userName(), self.db.databaseName(), self.db.hostName()))
				self.statusBar().showMessage(language_sheet.statusbar.signed_in)
				setup = MySQLSetup(self.db)
				setup.setup_currencies()
				return 'success'
		else:
			return 'canceled'

	def new_file(self):
		"""
		Create a new table in the database.
		Table name has to be specified within this method.
		Checks the database connection is established.
		"""
		while not self.db.isOpen():
			status = self.sign_in()
			if status == 'canceled':
				return

		tablename = ''
		while not tablename:
			tablename, ok = QtGui.QInputDialog.getText(self, 'New table', 'name: ')
			if not ok:
				return
			elif not tablename:
				QtGui.QMessageBox.critical(self, language_sheet.tablename_empty.title, language_sheet.tablename_empty.message)

		query = QtSql.QSqlQuery()
		if not query.exec_('CREATE TABLE ' + tablename + ' (' + ', '.join([' '.join(p) for p in zip(mysql_table_meta.columns, mysql_table_meta.column_types)]) + ', PRIMARY KEY(' + mysql_table_meta.columns[0] + '));'):
			QtGui.QMessageBox.critical(self, language_sheet.database_error.title, query.lastError().text())
			return

		tmp_page = QtGui.QWidget()
		tmp_exptable = ExpensesTable(text, self.db, self, tmp_page)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(tmp_exptable)
		tmp_page.setLayout(hbox)
		self.tabs.addTab(tmp_page, text)
		self.tabs.setCurrentWidget(tmp_page)

		self.statusBar().showMessage(language_sheet.statusbar.new_table(text))

	def open_file(self):
		"""
		Opens a table from the database.
		Names will be suggested based on the result of 'SHOW TABLES;' (table 'currencies' excluded).
		Checks the database connection is established before.
		"""
		while not self.db.isOpen():
			status = self.sign_in()
			if status == 'canceled':
				return

		open_dialog = OpenDialog(self.db, self)
		if open_dialog.exec_():
			tablename = open_dialog.get_tablename()
		else:
			return

		tmp_page = QtGui.QWidget()
		tmp_exptable = ExpensesTable(tablename, self.db, self, tmp_page)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(tmp_exptable)
		tmp_page.setLayout(hbox)
		self.tabs.addTab(tmp_page, tablename.split("/")[-1].split('.')[0])
		self.tabs.setCurrentWidget(tmp_page)

		self.statusBar().showMessage(language_sheet.statusbar.open_table(tablename))

	def dump_file(self):
		"""
		Dump the current table as json-string.
		"""
		import json
		try:
			with open(self.tabs.tabText(self.tabs.currentIndex())+'.json', 'w') as fp:
				json.dump(self.tabs.currentWidget().layout().itemAt(0).widget().get_expenses(), fp)
		except AttributeError:
			QtGui.QMessageBox.warning(self, 'No active table', 'There is nothing to save. Open a table first.')
		except IOError:
			QtGui.QMessageBox.critical(self, 'File Error', 'Cannot write '+self.tabs.tabText(self.tabs.currentIndex())+'.json')
		except:
			QtGui.QMessageBox.critical(self, 'Unknown Error', 'Oops. Something went wrong, try again. Sorry.')
		else:
			QtGui.QMessageBox.information(self, 'Success', 'Successfully saved table '+self.tabs.tabText(self.tabs.currentIndex())+' to file '+self.tabs.tabText(self.tabs.currentIndex())+'.json.')


	def save_file(self):
		"""
		Not needed at the moment.
		Saves the changes to the current table.
		As the tables' models are set to submit-on-change all changes will immidiately be saved.
		"""
		try:
			current_table = self.tabs.currentWidget().layout().itemAt(0).widget()
		except AttributeError:
			return

		if not current_table.filename:
			filename = QtGui.QFileDialog.getSaveFileName(self, 'Save table', '', 'Expenses Tables (*.myx *.json);;All (*.*)')
		else:
			filename = current_table.filename

		if not filename:
			return

		if '.' not in filename:
			filename += '.myx'

		current_table.save(filename)

		self.tabs.setTabText(self.tabs.currentIndex(), filename.split("/")[-1].split('.')[0])
		self.statusBar().showMessage("Saved table " + filename.split("/")[-1])

	def close_file(self):
		"""
		Closes the current table.
		Current table means the table the QTabWidget has focus on. Removes the current tab from the tabwidget.
		"""
		if not self.tabs.count():
			QtGui.QMessageBox.warning(self, language_sheet.cannot_close_table.title, language_sheet.cannot_close_table.message)
		else:
			self.tabs.removeTab(self.tabs.currentIndex())
			self.statusBar().showMessage(language_sheet.statusbar.close_table(self.tabs.tabText(self.tabs.currentIndex())))

	def add_expense(self):
		"""
		Adds an expense to the current table.
		Current table means the table the QTabWidget has focus on. Is connected to Menu- or ToolBar action as well as to the shortcut 'Ctrl+A'.
		Invokes the add_expense method of the respective table.
		"""
		try:
			self.tabs.currentWidget().layout().itemAt(0).widget().add_expense()
		except AttributeError:
			QtGui.QMessageBox.warning(self, language_sheet.cannot_add_expense.title, language_sheet.cannot_add_expense.message)

	def visualize_months(self):
		"""
		Visualizes the current table based on grouping by months.
		Current table means the table the QTabWidget has focus on. Created a pop-up window with the matplotlib.pyplot results. The pop-up's reference is stored in self.popups to prevent auto remove by the garbage collector.
		"""
		try:
			self.popups += [VisualizationMonths(self.tabs.currentWidget().layout().itemAt(0).widget())]
		except AttributeError:
			QtGui.QMessageBox.warning(self, language_sheet.nothing_to_plot.title, language_sheet.nothing_to_plot.message)
		except:
			QtGui.QMessageBox.critical(self, language_sheet.visualization_error.title, language_sheet.visualization_error.message)

	def visualize_categories(self):
		"""
		Visualizes the current table based on grouping by categories.
		Current table means the table the QTabWidget has focus on. Created a pop-up window with the matplotlib.pyplot results. The pop-up's reference is stored in self.popups to prevent auto remove by the garbage collector.
		"""
		try:
			self.popups += [VisualizationCategories(self.tabs.currentWidget().layout().itemAt(0).widget())]
		except AttributeError:
			QtGui.QMessageBox.warning(self, language_sheet.nothing_to_plot.title, language_sheet.nothing_to_plot.message)
		except:
			QtGui.QMessageBox.critical(self, language_sheet.visualization_error.title, language_sheet.visualization_error.message)

	def visualize_tree(self):
		"""
		Visualization in a tree view.
		"""
		self.popups += [VisualizationTree(self.tabs.currentWidget().layout().itemAt(0).widget())]
		# try:
		# 	self.popups += [VisualizationTree(self.tabs.currentWidget().layout().itemAt(0).widget())]
		# except AttributeError:
		# 	QtGui.QMessageBox.warning(self, language_sheet.nothing_to_plot.title, language_sheet.nothing_to_plot.message)
		# except:
		# 	QtGui.QMessageBox.critical(self, language_sheet.visualization_error.title, language_sheet.visualization_error.message)


	def closeEvent(self, event):
		"""
		This event is invoked when the mainwindow is closed.
		This is obsolete at the moment.
		"""
		#self.save_file()	#disabled for convenience while debugging

		event.accept()


# app = QtGui.QApplication(sys.argv)
# main = MainWindow()
# main.show()
# sys.exit(app.exec_())