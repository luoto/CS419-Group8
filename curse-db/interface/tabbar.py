import curses

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
				return self.tabName[i]
		return False

