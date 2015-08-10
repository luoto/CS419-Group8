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
		self.selected = None
	
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
		self.selected = itemName

	def deSelectItem(self, itemName):
		self.win.addstr(self.itemOffset[itemName], 0, self.displayedName(itemName), curses.color_pair(self.deSelectColor))
		self.win.refresh()

	def deSelectAll(self):
		for item in self.itemName:
			self.deSelectItem(item)
	
	def selectOnlyItem(self, itemName):
		for name in self.itemName:
			if name == itemName:
				self.selectItem(name)
			else:
				self.deSelectItem(name)
	
	def getSelected(self):
		return self.selected
	
	def itemAt(self, y, x):
		yesX = x >= self.parX and x <= self.parX + self.cols
		yesY = y >= self.parY and y <= self.parY + self.lines
		if yesX and yesY:
			index = y - self.parY
			if index >= 0 and index < len(self.itemName):
				return self.itemName[index]
		return False


