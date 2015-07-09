# Based on: https://docs.python.org/2/howto/curses.html#for-more-information

import curses
import curses.textpad as textpad

# Hand it a list (array) of strings, one for each tab (they should be unique)
# and the numbers corresponding to the color_pairs to use to represent selected
# and deSelected tabs. The first tab will be selected by default, but you
# can change this with selectOnlyTab(name) or selectTabAt(x-position)
class TabBar():
	def __init__(self, tabNames, selectColorPair, deSelectColorPair):
		self.win = {}
		self.selectColorPair = selectColorPair	
		self.deSelectColorPair = deSelectColorPair
		self.tabStart = []
		self.tabName = []
		offset = 0
		for name in tabNames:
			self.tabStart.append(offset)
			self.tabName.append(name)
			self.win[name] = curses.newwin(1, len(name)+4, 0, offset) 	
			self.win[name].addstr(0, 0, " " + name + " ")
			offset += len(name) + 4
		self.selectOnlyTab(self.tabName[0])

	def selectTab(self, tabName):
		w = self.win[tabName]
		w.border(" "," ", " "," ", " "," "," "," ")
		w.addstr(0, 0, " " + tabName + " ", curses.color_pair(self.selectColorPair))
		w.refresh()
	
	def deSelectTab(self, tabName):
		w = self.win[tabName]
		w.bkgd(' ', curses.color_pair(self.selectColorPair))
		w.border(" "," ","_","_"," ","_"," ","_")
		w.addstr(0, 0, " " + tabName + " ", curses.color_pair(self.deSelectColorPair))
		w.refresh()
	
	def selectOnlyTab(self, tabName):
		self.selectTab(tabName)
		for name in self.win:
			if name != tabName:
				self.deSelectTab(name)

	def selectTabAt(self, x):
		for i in range(0, len(self.tabStart)):
			(h, w) = self.win[self.tabName[i]].getmaxyx()
			if x > self.tabStart[i] and x < self.tabStart[i] + w:
				self.selectOnlyTab(self.tabName[i])
				return
		
# Hand it the window where the pane should display its results.  Use 
# setResults(list) to hand it the list of strings, then call showResults(num)
# to actually show the results (for the page number num)
class ResultsPane():
	def __init__(self, win):
		self.win = win
		(y, x) = self.win.getmaxyx()
		self.lines = y
		self.cols = x

	def setResults(self, list):
		self.curPage = 0
		self.results = list
		self.numResults = len(list)
		self.numPages = self.numResults/self.lines
		#determine how many \n are in str, compare to number of lines
		#in the pane. Break str into that many parts (in a list)?
	
	#If any result string is to long, it is cut off (and given a ...)
	def showResults(self, pageNum):
		if pageNum > self.numPages:
			return False

		self.curPage = pageNum
		start = self.lines*pageNum
		end = self.lines*(pageNum + 1)
		if end > self.numResults:
			end = self.numResults
		line = 0
		for i in range(start, end): 
			str = self.results[i]
			if len(str) > self.cols:
				str = str[:self.cols - 3] + "..."
			self.win.addstr(line, 0, str)
			line += 1	
		self.win.refresh()
	
	def getPageNum(self):
		return self.curPage

	def clear(self):
		self.win.clear()
		self.win.refresh()

# Initialize the standard screen
scr = curses.initscr()

# Start up color, then create color pair 1 and 2 (0 is resevered) for tabs
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)

# Various setting changes
#curses.noecho() # So typed letters are not echoed to the screen
#curses.cbreak() # supposedly so keys are processed instantly (no Enter)
scr.nodelay(1) # makes scr.getch() non-blocking
scr.keypad(1) # Assigns special characters (such as curses.KEY_LEFT)
curses.curs_set(0) # makes cursor invisible
curses.mousemask(1) # needed to capture mouse click events

# Set up instructions just above the textbox (at the bottom of the screen) 
scr.addstr(curses.LINES - 3, 0, "You can click on the tabs above or click on the textbox below to enter something do display. Enter 'quit' to exit.", curses.A_BOLD)
scr.refresh()

# Create textBox for edit-able input
inputBox = textpad.Textbox(curses.newwin(1, curses.COLS-1, curses.LINES-1, 0))

# Creat the tabs at the top of the screen
tabs = TabBar(["Main Menu", "Tables", "Seach", "Query", "Help"], 1, 2)

# Create a small pane to display input in (for testing displaying results)	
w = 15
y = 2
x = 0
pane = ResultsPane(curses.newwin(2, w, y, x))

# Main loop, program ends when 'quit' is entered in the textbox
while 1:
	# Be ready to capture a mouse click
	curses.echo()
	curses.curs_set(0)
	ch = scr.getch()
	if ch == curses.KEY_MOUSE:
		(id, x, y, z, s) = curses.getmouse()
		# if the click was in the textbox at the bottom of the screen
		if y == curses.LINES - 1:
			# Make the cursor visible and stop echoing to the screen
			# (stopping echoing prevents mouse clicks too however)
			curses.curs_set(1)
			curses.noecho()
			# Get whatever the user enters into the textbox
			str = inputBox.edit()
			str = str.strip()
			pane.clear()
			# quit if they typed 'quit', otherwise, display input
			if str == "quit":
				break
			else:
				list = [str, "test of line 2"]
				pane.setResults(list)
				pane.showResults(pane.getPageNum())
				# Make the textbox clear when next clicked on
				inputBox = textpad.Textbox(curses.newwin(1, curses.COLS-1, curses.LINES-1, 0)) 
		# if the click in the tab bar at the top of the screen
		elif y == 0:
			# select the tab at the x-position of the click
			tabs.selectTabAt(x)	


# Make sure to clean up whatever window mode we may have gotten into
curses.echo()
curses.curs_set(1)
curses.endwin()

