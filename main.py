import sys
from PyQt4 import QtGui
from mainwindow import MainWindow

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())