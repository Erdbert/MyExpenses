class MenuBarSections:
	def __init__(self, table, edit, visualization):
		self.table = table
		self.edit = edit
		self.visualization = visualization

class MenuBarItem:
	def __init__(self, title, shortcut, statustip):
		self.title = title
		self.shortcut = shortcut
		self.statustip = statustip

class LogInAction:
	def __init__(self, title, shortcut, tooltip_login_required, tooltip_login_successful_base, statustip):
		self.title = title
		self.shortcut = shortcut
		self.tooltip_login_required = tooltip_login_required
		self.tooltip_login_successful_base = tooltip_login_successful_base
		self.statustip = statustip

	def tooltip_login_successful(self, username, databasename, hostname):
		return self.tooltip_login_successful_base + username + '@' + databasename + '.' + hostname

class StatusBarMessages:
	def __init__(self, intro, not_signed_in, sign_in_failed, signed_in, new_table_base, open_table_base, close_table_base):
		self.intro = intro
		self.not_signed_in = not_signed_in
		self.sign_in_failed = sign_in_failed
		self.signed_in = signed_in
		self.new_table_base = new_table_base
		self.open_table_base = open_table_base
		self.close_table_base = close_table_base

	def new_table(self, tablename):
		return self.new_table_base + ' ' + tablename

	def open_table(self, tablename):
		return self.open_table_base + ' ' + tablename

	def close_table(self, tablename):
		return self.close_table_base + ' ' + tablename

class ErrorMessage:
	def __init__(self, title, message):
		self.title = title
		self.message = message

	def conditional_message(self, value):
		return self.message + ' ' + value


menubar_sections = MenuBarSections('&Table', '&Edit', '&Visualization')

new_table = MenuBarItem('New table', 'Ctrl+N', 'Create a new expense table')
open_table = MenuBarItem('Open Table', 'Ctrl+O', 'Load an expenses table from the database')
close_table = MenuBarItem('Close Table', 'Ctrl+C', 'Close the current expense table')
exit_application = MenuBarItem('Exit', 'Ctrl+Q', 'Exit the application')
add_expense = MenuBarItem('Add expense', 'Ctrl+A', 'Add an expense to the current table')
grouped_by_months = MenuBarItem('Grouped by months', '', 'Plot the expenses per month for a certain year in either a histogram or a pie chart')
grouped_by_categories = MenuBarItem('Grouped by categories', '', 'Plot the expenses per category for a certain year and/or month in either a histogram or a pie chart')

log_in = LogInAction('Log-In', 'Ctrl+L', 'You\'re not logged in yet', 'Successfully logged in as ', 'Log-in to a database')

statusbar = StatusBarMessages('Ready', 'not signed in yet', 'sign-in failed', 'signed in successfully', 'created new table', 'loaded table', 'closed table')

log_in_failed = ErrorMessage('Log-in failed', 'Log-in failed')
tablename_empty = ErrorMessage('No name specified', 'Table name must no be empty!')
database_error = ErrorMessage('Database error', '')
cannot_close_table = ErrorMessage('No tables loaded', 'There is no table to close.')
cannot_add_expense = ErrorMessage('Cannot add expense', 'There is no table to add an expense to. Please load a table first.')
nothing_to_plot = ErrorMessage('Nothing to plot', 'There is no table available for visualization. Please load a table first.')
visualization_error = ErrorMessage('Visualization error', 'Could not create an instance of the visualization class.')