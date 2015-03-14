import numpy as np
import matplotlib.pyplot as ppl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from PyQt4 import QtGui, QtCore

class VisualizationMonths(QtGui.QWidget):
	def __init__(self, expense_table, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.setGeometry(50, 50, 800, 480)

		expenses_list = expense_table.get_expenses()
		self.currencies = expense_table.currencies
		self.translate_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
		self.translate_month_back = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

		self.years = {}
		for expense in expenses_list:
			year = expense[0].split('-')[0]
			month = self.translate_month[int(expense[0].split('-')[1])]

			if year not in self.years.keys():
				self.years[year] = {}
			if month not in self.years[year].keys():
				self.years[year][month] = float(expense[3]) / self.currencies[expense[4]]
			else:
				self.years[year][month] += float(expense[3]) / self.currencies[expense[4]]

		self.which_plot = QtGui.QComboBox(self)
		self.which_plot.addItem('Histogram', 'Histogram')
		self.which_plot.addItem('Pie Chart', 'Pie Chart')
		self.which_plot.setCurrentIndex(self.which_plot.findData('Histogram'))

		self.combo_year = QtGui.QComboBox(self)
		for yy in self.years.keys():
			self.combo_year.addItem(yy, yy)
		self.combo_year.setCurrentIndex(self.combo_year.findData(max(self.years.keys(), key=lambda p: int(p))))

		self.plot_area = ppl.figure()
		self.plot_canvas = FigureCanvas(self.plot_area)
		self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)
		self.plot_layout = QtGui.QVBoxLayout()
		self.plot_layout.addWidget(self.plot_canvas)
		self.plot_layout.addWidget(self.plot_toolbar)

		self.grid = QtGui.QGridLayout(self)
		self.grid.addWidget(self.which_plot, 0, 0, 1, 1)
		self.grid.addWidget(self.combo_year, 0, 1, 1, 1)
		self.grid.addLayout(self.plot_layout, 1, 0, 3, 3)
		self.setLayout(self.grid)

		self.connect(self.which_plot, QtCore.SIGNAL('activated(int)'), self.make_which_plot)
		self.connect(self.combo_year, QtCore.SIGNAL('activated(int)'), self.make_which_plot)

		self.make_which_plot()

		self.show()

	def make_which_plot(self):
		if self.which_plot.itemData(self.which_plot.currentIndex()) == 'Histogram':
			self.make_plot_hist()
		elif self.which_plot.itemData(self.which_plot.currentIndex()) == 'Pie Chart':
			self.make_plot_pie()

	def make_plot_hist(self):
		xlist = self.years[str(self.combo_year.itemData(self.combo_year.currentIndex()).toString())].keys()
		ylist = self.years[str(self.combo_year.itemData(self.combo_year.currentIndex()).toString())].values()

		tmp = sorted(zip(xlist, ylist), key=lambda p: self.translate_month_back[p[0]])
		xlist = [x[0] for x in tmp]
		ylist = [x[1] for x in tmp]

		xpos = np.arange(len(xlist))
		width = 1.0

		ppl.cla()
		axes = self.plot_area.add_subplot(111)
		axes.set_xticks(xpos + width/2.)
		axes.set_xticklabels(xlist)
		ppl.xlim(min(xpos), max(xpos)+width)

		axes.set_xlabel('')
		axes.set_ylabel('EUR')

		barplot = ppl.bar(xpos, ylist, width, color=(0.2, 0.4, 0.6))

		for bar in barplot:
			height = bar.get_height()
			if height > 0.:
				axes.text(bar.get_x()+bar.get_width()/2., 0.5*height, '%1.2f'%float(height), ha='center', va='bottom')

		self.plot_canvas.draw()

	def make_plot_pie(self):
		xlist = self.years[str(self.combo_year.itemData(self.combo_year.currentIndex()).toString())].keys()
		ylist = self.years[str(self.combo_year.itemData(self.combo_year.currentIndex()).toString())].values()

		total_amount = sum(ylist)
		try:
			ylist = [y / total_amount for y in ylist]
		except ZeroDivisionError:
			pass

		tmp = filter(lambda p: p[1] > 0., zip(xlist, ylist))	# the amount of a month should always be greater than zero unless a month contains zero expenses only
		tmp = sorted(tmp, key=lambda p: self.translate_month_back[p[0]])
		xlist = [p[0] for p in tmp]
		ylist = [p[1] for p in tmp]

		ppl.cla()
		axes = self.plot_area.add_subplot(111)
		ppl.pie(ylist, labels=xlist, autopct='%1.1f%%', startangle=90)
		#ppl.pie(ylist, labels=xlist, autopct='%1.1f%%', startangle=90, counterclock=False)
		#ppl.pie(ylist, labels=xlist, autopct='%1.1f%%')
		self.plot_canvas.draw()


class VisualizationCategories(QtGui.QWidget):
	def __init__(self, expense_table, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.setGeometry(50, 50, 800, 480)

		expenses_list = expense_table.get_expenses()
		self.categories = expense_table.categories
		self.currencies = expense_table.currencies

		self.translate_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
		self.translate_month_back = {'Jan': 1, 'Feb': 2, 'Mar': 2, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

		self.years = []
		self.gbc = {}	#gbc = grouped by category
		for expense in expenses_list:
			year = expense[0].split('-')[0]
			month = self.translate_month[int(expense[0].split('-')[1])]
			category = expense[1]
			try:
				value = float(expense[3])
			except ValueError:
				value = 0.
			currency = expense[4]

			if year not in self.years:
				self.years += [year]

			if category not in self.gbc.keys():
				self.gbc[category] = {}
			if year not in self.gbc[category].keys():
				self.gbc[category][year] = {}
			if month not in self.gbc[category][year].keys():
				self.gbc[category][year][month] = value / self.currencies[currency]
			else:
				self.gbc[category][year][month] += value / self.currencies[currency]

		self.which_plot = QtGui.QComboBox(self)
		self.which_plot.addItem('Histogram', 'Histogram')
		self.which_plot.addItem('Pie Chart', 'Pie Chart')
		self.which_plot.setCurrentIndex(self.which_plot.findData('Histogram'))

		self.combo_year = QtGui.QComboBox(self)
		self.combo_year.addItem('all', 'all')
		for yy in self.years:
			self.combo_year.addItem(yy, yy)
		self.combo_year.setCurrentIndex(self.combo_year.findData(max(self.years, key=lambda p: int(p))))

		self.combo_month = QtGui.QComboBox(self)
		self.combo_month.addItem('all', 'all')
		for mm in self.translate_month.values():
			self.combo_month.addItem(mm, mm)
		self.combo_month.setCurrentIndex(self.combo_month.findData('all'))

		self.plot_area = ppl.figure()
		self.plot_canvas = FigureCanvas(self.plot_area)
		self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)
		self.plot_layout = QtGui.QVBoxLayout()
		self.plot_layout.addWidget(self.plot_canvas)
		self.plot_layout.addWidget(self.plot_toolbar)

		self.grid = QtGui.QGridLayout(self)
		self.grid.addWidget(self.which_plot, 0, 0, 1, 1)
		self.grid.addWidget(self.combo_year, 0, 1, 1, 1)
		self.grid.addWidget(self.combo_month, 0, 2, 1, 1)
		self.grid.addLayout(self.plot_layout, 1, 0, 3, 3)
		self.setLayout(self.grid)

		self.connect(self.which_plot, QtCore.SIGNAL('activated(int)'), self.make_which_plot)
		self.connect(self.combo_year, QtCore.SIGNAL('activated(int)'), self.make_which_plot)
		self.connect(self.combo_month, QtCore.SIGNAL('activated(int)'), self.make_which_plot)

		self.make_which_plot()

		self.show()

	def make_which_plot(self):
		if self.which_plot.itemData(self.which_plot.currentIndex()) == 'Histogram':
			self.make_plot_hist()
		elif self.which_plot.itemData(self.which_plot.currentIndex()) == 'Pie Chart':
			self.make_plot_pie()

	def make_plot_hist(self):
		xlist = self.gbc.keys()
		ylist = []

		year_value = str(self.combo_year.itemData(self.combo_year.currentIndex()).toString())
		month_value = str(self.combo_month.itemData(self.combo_month.currentIndex()).toString())

		for category in xlist:
			tmp = 0.
			if year_value == 'all':
				which_years = self.gbc[category].keys()
			else:
				which_years = [year_value]

			for year in which_years:
				if month_value == 'all':
					try:
						which_months = self.gbc[category][year].keys()
					except KeyError:
						which_months = []
				else:
					which_months = [month_value]

				for month in which_months:
					try:
						tmp += self.gbc[category][year][month]
					except KeyError:
						pass
			ylist += [tmp]

		tmp = sorted(zip(xlist, ylist), key=lambda p: p[1])
		tmp.reverse()
		xlist = [p[0] for p in tmp]
		ylist = [p[1] for p in tmp]

		xpos = np.arange(len(xlist))
		width = 1.0

		ppl.cla()
		axes = self.plot_area.add_subplot(111)
		axes.set_xticks(xpos + width/2.)
		axes.set_xticklabels(xlist)
		ppl.xlim(min(xpos), max(xpos)+width)

		axes.set_xlabel('')
		axes.set_ylabel('EUR')

		barplot = ppl.bar(xpos, ylist, width, color=(0.2, 0.4, 0.6))

		for bar in barplot:
			height = bar.get_height()
			if height > 0.:
				axes.text(bar.get_x()+bar.get_width()/2., 0.5*height, '%1.2f'%float(height), ha='center', va='bottom')

		self.plot_canvas.draw()

	def make_plot_pie(self):
		xlist = self.gbc.keys()
		ylist = []

		year_value = str(self.combo_year.itemData(self.combo_year.currentIndex()).toString())
		month_value = str(self.combo_month.itemData(self.combo_month.currentIndex()).toString())

		for category in xlist:
			tmp = 0.
			if year_value == 'all':
				which_years = self.gbc[category].keys()
			else:
				which_years = [year_value]

			for year in which_years:
				if month_value == 'all':
					try:
						which_months = self.gbc[category][year].keys()
					except KeyError:
						which_months = []
				else:
					which_months = [month_value]

				for month in which_months:
					try:
						tmp += self.gbc[category][year][month]
					except KeyError:
						pass
			ylist += [tmp]

		total_amount = sum(ylist)

		try:
			ylist = [p / total_amount for p in ylist]
		except ZeroDivisionError:
			pass

		tmp = filter(lambda p: p[1] > 0., zip(xlist, ylist))
		tmp = sorted(tmp, key=lambda p: p[1])
		xlist = [p[0] for p in tmp]
		ylist = [p[1] for p in tmp]

		ppl.cla()
		axes = self.plot_area.add_subplot(111)
		ppl.pie(ylist, labels=xlist, autopct='%1.1f%%', startangle=90)
		#ppl.pie(ylist, labels=xlist, autopct='%1.1f%%')
		self.plot_canvas.draw()

class VisualizationTree(QtGui.QWidget):
	def __init__(self, expense_table, parent=None):
		QtGui.QTreeView.__init__(self, parent)

		self.setGeometry(50, 50, 800, 480)

		self.bgroup = QtGui.QButtonGroup(self)
		self.b_what = QtGui.QRadioButton("description")
		self.b_what.setChecked(True)
		self.b_date = QtGui.QRadioButton("date")
		self.b_date.setChecked(False)
		self.bgroup.addButton(self.b_what)
		self.bgroup.addButton(self.b_date)

		self.bgroupUI = QtGui.QGroupBox("Sort by: ", self)
		blayout = QtGui.QHBoxLayout()
		blayout.addWidget(self.b_what)
		blayout.addWidget(self.b_date)
		self.bgroupUI.setLayout(blayout)

		self.tree = QtGui.QTreeView(self)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.bgroupUI)
		layout.addWidget(self.tree)
		self.setLayout(layout)

		self.tree.header().setVisible(False)

		self.translate_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

		self.expenses_list = expense_table.get_expenses()
		self.categories = expense_table.categories
		self.categories = sorted(self.categories, key=lambda x: x.lower())

		self.model = QtGui.QStandardItemModel()
		self.tree.setModel(self.model)

		self.fill(self.b_what)

		self.connect(self.bgroup, QtCore.SIGNAL("buttonClicked(QAbstractButton*)"), self.fill)

		self.show()

	def fill(self, button):
		self.model.clear()
		if button == self.b_what:
			self.fill_what()
		elif button == self.b_date:
			self.fill_date()
		else:
			QtGui.QMessageBox.critical(self, "Error", "No button selected!")

	def fill_what(self):
		for category in self.categories:
			cat = QtGui.QStandardItem(category)
			for what in sorted(list(set([p[2] for p in self.expenses_list if category in p])), key=lambda x: x.lower()):
				wha = QtGui.QStandardItem(what)
				for expense in sorted([p for p in self.expenses_list if category in p and what in p], key=lambda x: QtCore.QDate(int(x[0].split('-')[0]), int(x[0].split('-')[1]), int(x[0].split('-')[2])) ):
					wha.appendRow(QtGui.QStandardItem("{0}, {1} {2}".format("{0} {1} {2}".format(expense[0].split('-')[2].lstrip('0'), self.translate_month[int(expense[0].split('-')[1])], expense[0].split('-')[0]), expense[3], expense[4])))
				cat.appendRow(wha)
			self.model.appendRow(cat)

	def fill_date(self):
		for category in self.categories:
			cat = QtGui.QStandardItem(category)
			for date in sorted(list(set(['-'.join(p[0].split('-')[0:2]) for p in self.expenses_list if category in p])), key=lambda x: QtCore.QDate(int(x.split('-')[0]), int(x.split('-')[1]), 1) ):
				dat = QtGui.QStandardItem("{0} {1}".format(self.translate_month[int(date.split('-')[1])], date.split('-')[0]))
				for what in sorted([(p[0],p[2],p[3],p[4]) for p in self.expenses_list if category in p and date in p[0]], key=lambda x: x[1].lower()):
					dat.appendRow(QtGui.QStandardItem("{1}, {2} {3} ({0})".format("{0} {1} {2}".format(what[0].split('-')[2].lstrip('0'), self.translate_month[int(what[0].split('-')[1])], what[0].split('-')[0]), what[1], what[2], what[3])))
				cat.appendRow(dat)
			self.model.appendRow(cat)

# class VisualizationTree(QtGui.QTreeView):
# 	def __init__(self, expense_table, parent=None):
# 		QtGui.QTreeView.__init__(self, parent)

# 		self.setGeometry(50, 50, 800, 480)

# 		self.header().setVisible(False)

# 		translate_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

# 		expenses_list = expense_table.get_expenses()
# 		categories = expense_table.categories
# 		categories = sorted(categories, key=lambda x: x.lower())

# 		model = QtGui.QStandardItemModel()
# 		self.setModel(model)

# 		for category in categories:
# 			cat = QtGui.QStandardItem(category)
# 			for what in sorted(list(set([p[2] for p in expenses_list if category in p])), key=lambda x: x.lower()):
# 				wha = QtGui.QStandardItem(what)
# 				for expense in sorted([p for p in expenses_list if category in p and what in p], key=lambda x: QtCore.QDate(int(x[0].split('-')[0]), int(x[0].split('-')[1]), int(x[0].split('-')[2])) ):
# 					wha.appendRow(QtGui.QStandardItem("{0}, {1} {2}".format("{0} {1} {2}".format(expense[0].split('-')[2].lstrip('0'), translate_month[int(expense[0].split('-')[1])], expense[0].split('-')[0]), expense[3], expense[4])))
# 				cat.appendRow(wha)
# 			model.appendRow(cat)

# 		self.show()
