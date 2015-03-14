from PyQt4 import QtGui, QtCore

class NewCurrencyDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.setWindowTitle('New currency')

		self.name = QtGui.QLineEdit(self)
		self.exchange_rate = QtGui.QLineEdit(self)
		self.exchange_rate.setValidator(QtGui.QDoubleValidator())

		self.name_label = QtGui.QLabel('name (3 characters, e.g. \'EUR\')', self)
		self.exchange_rate_label = QtGui.QLabel('exchange rate to EUR', self)

		self.ok = QtGui.QPushButton('ok', self)
		self.connect(self.ok, QtCore.SIGNAL('clicked()'), QtCore.SLOT('accept()'))
		self.cancel = QtGui.QPushButton('cancel', self)
		self.connect(self.cancel, QtCore.SIGNAL('clicked()'), QtCore.SLOT('reject()'))

		grid = QtGui.QGridLayout()
		grid.addWidget(self.name_label, 0, 0, 1, 1)
		grid.addWidget(self.name, 0, 1, 1, 1)
		grid.addWidget(self.exchange_rate_label, 1, 0, 1, 1)
		grid.addWidget(self.exchange_rate, 1, 1, 1, 1)
		grid.addWidget(self.ok, 2, 0, 1, 1)
		grid.addWidget(self.cancel, 2, 1, 1 ,1)
		self.setLayout(grid)

	def get_values(self):
		return str(self.name.text()), str(self.exchange_rate.text())

class ExpenseDialog(QtGui.QDialog):
	def __init__(self, categories, currencies, parent=None):
		QtGui.QDialog.__init__(self, parent)

		self.categories = categories
		self.currencies = currencies
		self.currencies_added = {}

		self.calendar = QtGui.QCalendarWidget(self)
		self.calendar.setToolTip('date')

		self.category = QtGui.QComboBox(self)
		self.category.setToolTip('category')
		for category in categories:
			self.category.addItem(category, category)
		self.category.addItem('+ new category', '+ new category')
		self.connect(self.category, QtCore.SIGNAL('activated(int)'), self.new_category)

		self.what = QtGui.QLineEdit(self)
		self.what.setPlaceholderText('description')

		self.value = QtGui.QLineEdit(self)
		self.value.setPlaceholderText('value')
		self.value.setValidator(QtGui.QDoubleValidator())

		self.currency = QtGui.QComboBox(self)
		self.currency.setToolTip('currency')
		for currency in currencies:
			self.currency.addItem(currency, currency)
		self.currency.addItem('+ new currency', '+ new currency')
		self.connect(self.currency, QtCore.SIGNAL('activated(int)'), self.new_currency)

		self.ok = QtGui.QPushButton('ok', self)
		self.connect(self.ok, QtCore.SIGNAL('clicked()'), QtCore.SLOT('accept()'))

		self.cancel = QtGui.QPushButton('cancel', self)
		self.connect(self.cancel, QtCore.SIGNAL('clicked()'), QtCore.SLOT('reject()'))

		# hbox = QtGui.QHBoxLayout()
		# hbox.addWidget(self.calendar)
		# hbox.addWidget(self.category)
		# hbox.addWidget(self.what)
		# hbox.addWidget(self.value)
		# hbox.addWidget(self.currency)
		# self.setLayout(hbox)

		grid = QtGui.QGridLayout()
		grid.addWidget(self.calendar, 0, 0, 1, 1)
		grid.addWidget(self.category, 0, 1, 1, 1)
		grid.addWidget(self.what, 0, 2, 1, 3)
		grid.addWidget(self.value, 0, 5, 1, 1)
		grid.addWidget(self.currency, 0, 6, 1, 1)
		grid.addWidget(self.ok, 1, 5, 1, 1)
		grid.addWidget(self.cancel, 1, 6, 1, 1)
		self.setLayout(grid)

	def new_category(self):
		if self.category.itemData(self.category.currentIndex()) != '+ new category':
			return

		category, ok = QtGui.QInputDialog.getText(self, 'New category', 'Add what? ')

		if not ok or category in self.categories:
			return
			
		self.category.insertItem(self.category.currentIndex(), category, category)
		self.categories.append(category)
		self.category.setCurrentIndex(self.category.findData(category))

	def new_currency(self):
		if self.currency.itemData(self.currency.currentIndex()) != '+ new currency':
			return

		dialog = NewCurrencyDialog(self)
		if dialog.exec_():
			currency, exchange_rate = dialog.get_values()
		else:
			currency = None

		if currency in self.currencies.keys() or not currency:
			self.currency.setCurrentIndex(0)
			return
			
		self.currency.insertItem(self.currency.currentIndex(), currency, currency)
		self.currencies[currency] = exchange_rate
		self.currencies_added[currency] = exchange_rate
		self.currency.setCurrentIndex(self.currency.findData(currency))

	def get_values(self):
		return "\'"+str(self.calendar.selectedDate().toPyDate())+"\'", "\'"+str(self.category.itemData(self.category.currentIndex()).toString())+"\'", "\'"+str(self.what.text())+"\'", str(self.value.text()), "\'"+str(self.currency.itemData(self.currency.currentIndex()).toString())+"\'"

	def update_lists(self):
		return self.categories, self.currencies_added
