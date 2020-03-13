from PyQt5 import QtWidgets, QtGui
# from bs4 import BeautifulSoup
from lxml import html
import requests
import sys

class WilliamHillParser:
	def __init__(self):
		link = ""

	def parse(self):
		pass

class PariMatchParser:
	def __init__(self, main_window):
		self.link = "https://www.parimatch.com/en/live_as.html?curs=0&curName=$&shed=0"
		self.main_window = main_window

	def parse(self):
		print('bbb')
		response = requests.get(self.link)
		#soup = BeautifulSoup(response, 'lxml')
		tree = html.fromstring(response.content)
		sport_list = tree.xpath("//div[@class='wrapper']/div")
		for sport in sport_list:
			match_list = sport.xpath("./div/div/table")
			for match in match_list:
				self.name = match.xpath(".//td[@class='td_n']/a/text()")[0]
				
				#!!!!
				try:
					self.one = match.xpath(".//td[3]//i[@class='blank']/text()")[0]
				except:
					self.one = ' '

				try:
					self.x = match.xpath(".//td[4]//i[@class='blank']/text()")[0]
				except:
					self.x = ' '

				try:
					self.two = match.xpath(".//td[5]//i[@class='blank']/text()")[0]
				except:
					self.two = ' '

				# print(self.one, self.x, self.two)
				self.main_window.matchList.setRowCount(self.main_window.matchList.rowCount()+1)
				# print(self.main_window.matchList.rowCount())
				self.main_window.matchList.setItem(self.main_window.matchList.rowCount()-1, 0, QtWidgets.QTableWidgetItem(self.name))
				self.main_window.matchList.setItem(self.main_window.matchList.rowCount()-1, 1, QtWidgets.QTableWidgetItem(self.one))
				self.main_window.matchList.setItem(self.main_window.matchList.rowCount()-1, 2, QtWidgets.QTableWidgetItem(self.x))
				self.main_window.matchList.setItem(self.main_window.matchList.rowCount()-1, 3, QtWidgets.QTableWidgetItem(self.two))

				matchList += [self.name, self.one, self.x, self.two]

class MainWindow(QtWidgets.QWidget):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent) #!!!!
		self.vbox = QtWidgets.QVBoxLayout()
		self.hbox = QtWidgets.QHBoxLayout()

		self.logArea = QtWidgets.QPlainTextEdit()
		self.bookmakerList = QtWidgets.QListWidget()
		self.matchList = QtWidgets.QTableWidget()
		self.searchLine = QtWidgets.QLineEdit()
		self.parseBtn = QtWidgets.QPushButton("Parse")
		self.clearTable = QtWidgets.QPushButton("Clear")
		self.widgt = QtWidgets.QWidget()

		self.matchList.setColumnCount(5)
		self.bookmakerList.addItem("PariMatch")
		self.bookmakerList.addItem("William Hill")
		self.searchLine.textChanged.connect(self.searchRequestChanged)

		self.hbox.addWidget(self.logArea)
		self.hbox.addWidget(self.bookmakerList)
		self.widgt.setLayout(self.hbox)
		self.vbox.addWidget(self.widgt)
		self.vbox.addWidget(self.matchList)
		self.vbox.addWidget(self.searchLine)
		self.vbox.addWidget(self.parseBtn)
		self.vbox.addWidget(self.clearTable)
		self.setLayout(self.vbox)

		# self.matchList.setRowCount(3)
		self.matchList.setColumnCount(5)

		# self.matchList.setItem(1, 1, QtWidgets.QTableWidgetItem('12345678'))
		self.parseBtn.clicked.connect(self.parse)
		self.clearTable.clicked.connect(self.clear)

	def parse(self):
		matchList = []
		for i in range(self.matchList.rowCount()):
			self.matchList.removeRow(0)
		parimatch_parser = PariMatchParser(self)
		parimatch_parser.parse()

	def clear(self):
		for i in range(self.matchList.rowCount()):
			self.matchList.removeRow(0)

	def searchRequestChanged(self, text):
		if text == '':
			self.parse()
		else:
			correctRows = []
			for i in range(len(matchList)):
				if matchList[i].find(text) != -1:
					correctRows += i
			self 

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.resize(600, 800)

window.show()
sys.exit(app.exec_())