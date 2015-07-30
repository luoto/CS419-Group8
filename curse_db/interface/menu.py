import curses

# Hand it a window and a list of strings (one for each menu item, and the list 
# can be changed later).
# No item will be selected as the default.
# The menu is verticle. If there are too many items, up (and down) arrows will
# be displayed.
class Menu():
	def __init__(self, y, x, lines, cols, itemNames=[], sideBar=False, cpNumSel=0, cpNumDeSel=0):
		self.win = curses.newwin(lines, cols, y, x)
		self.parY = y
		self.parX = x
		(self.lines, self.cols) = self.win.getmaxyx()
		self.selectColor = cpNumSel
		self.deSelectColor = cpNumDeSel
		self.border = sideBar
		self.setItems(itemNames)
	
	def displayedName(self, name):
		if len(name) + 3 > self.cols:
			return "[" + name[:self.cols - 6] + "..." + "]"
		else:
			return "[" + name + "]"

	def setItems(self, itemNames):
		self.itemOffset = {}
		self.itemName = itemNames
		offset = 0
		for name in self.itemName:
			self.itemOffset[name] = offset
			self.win.addstr(offset, 0, self.displayedName(name))
			offset += 1
		self.win.refresh()

	def unhide(self):
		if (self.border):
			self.win.border(" ", "|", " ", " ", " ", "|", " ", "|")
		self.setItems(self.itemName)

	def hide(self):
		self.win.clear();
		self.win.refresh()
	
	def selectItem(self, itemName):
		self.win.addstr(self.itemOffset[itemName], 0, self.displayedName(itemName), curses.color_pair(self.selectColor))
		self.win.refresh()

	def deSelectItem(self, itemName):
		self.win.addstr(self.itemOffset[itemName], 0, self.displayedName(itemName), curses.color_pair(self.deSelectColor))
		self.win.refresh()

	def selectOnlyItem(self, itemName):
		for name in self.itemName:
			if name == itemName:
				self.selectItem(name)
			else:
				self.deSelectItem(name)

	def itemAt(self, y, x):
		yesX = x >= self.parX and x <= self.parX + self.cols
		yesY = y >= self.parY and y <= self.parY + self.lines
		if yesX and yesY:
			index = y - self.parY
			if index >= 0 and index < len(self.itemName):
				return self.itemName[index]
		return False


'''	
	def deSelectItem(self, itemName):
		w = self.win[tabName]
		w.bkgd(' ', curses.color_pair(self.selectColorPair))
		w.border(" "," ","_","_"," ","_"," ","_")
		w.addstr(0, 0, " " + tabName + " ", curses.color_pair(self.deSelectColorPair))
		w.refresh()
	
	def selectOnlyItem(self, itemName):
		self.selectTab(tabName)
		for name in self.win:
			if name != tabName:
				self.deSelectTab(name)

	def selectItemAt(self, x):
		for i in range(0, len(self.tabStart)):
			(h, w) = self.win[self.tabName[i]].getmaxyx()
			if x > self.tabStart[i] and x < self.tabStart[i] + w:
				self.selectOnlyTab(self.tabName[i])
				return self.tabName[i]
		return False

	#If any result string is to long, it is cut off (and given a ...)
	def showResults(self, pageNum):
		if pageNum > self.numPages:
			return False
		
		self.win.clear()
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
		if self.hasPrev():
			self.win.addstr(self.lines, 1, self.PREV)
		if self.hasNext():
			self.win.addstr(self.lines, self.nextX(), self.NEXT)	
		self.win.refresh()
	
	def getPageNum(self):
		return self.curPage

	def reset(self):
		self.win.clear()
		self.win.refresh()
		self.curPage = -1
		self.results = []
		self.numResults = 0
		self.numPages = 0
	
	# True if the x is within the next button (should work even if 
	# ResultsPane is not alligned with the parent)
	# Always False if there is no next.
	def atNext(self, x):
		if self.hasNext():
			(parY, parX) = self.win.getparyx()
			return x >= (self.nextX() + parX) and x <= (self.cols + parX)
		else:
			return False

	# True if the x is within the prev button (should work even if 
	# ResultsPane is not alligned with the parent)
	# Always False if there is no prev
	def atPrev(self, x):
		if self.hasPrev():
			(parY, parX) = self.win.getparyx()
			return x <= (self.prevX() + parX) and x >= parX
		else:
			return False

	# returns the inner-edge of the next button
	def nextX(self):
		return self.cols - len(self.NEXT) - 1

	# returns the inner-edge of the prev button
	def prevX(self):
		return len(self.PREV) + 1
'''
