from PyQt4 import QtGui, QtCore

class AmountStyledItemDelegate(QtGui.QStyledItemDelegate):
	"""
	Displays a floating point number with a precision of exactly 2 digits. Will be applied to a column in QTableView via setItemDelegateForColumn().
	"""
	def __init__(self, parent=None):
		QtGui.QStyledItemDelegate.__init__(self, parent)

	def displayText(self, value, locale):
		return locale.toString(value.toFloat()[0], 'f', 2)