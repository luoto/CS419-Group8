import curses
import curses.textpad as textpad

# Hand in a string to go in front of the input textbox, the y and x that string
# should start on, the max number of lines the textbox will expand to when it
# is in edit mode, the min number of lines when it is not being used, and the
# number of cols long (defaults to edge of screen).
# A border will be created around the textbox.  In addition to exapanding, both
# the prompt and the texbox can be hidden (then unhidden for later use).
class InputBox():
	def __init__(self, promptStr, y, x, maxLines, minLines=1, cols=-1):
		if cols == -1:
			w = curses.COLS - x
		else:
			w = cols + 2
		self.areaWin = curses.newwin(minLines + 2, w, y, x)
		self.prompt = promptStr
		self.hidden = False
		self.areaWin.addstr(self.prompt)
		self.areaWin.refresh()
		
		(newY, newX) = self.areaWin.getyx()
		self.x = newX
		self.y = y
		self.h = minLines + 2
		self.maxh = maxLines + 2
		if cols == -1:
			self.w = curses.COLS - newX
		else:
			self.w = cols + 2
		
		self.innerBox = curses.newwin(self.h - 2, self.w - 2, self.y + 1, self.x + 1)
		self.makeSmall()	
	
	def makeSmall(self):
		self.outerBox = curses.newwin(self.h, self.w, self.y, self.x)
		self.outerBox.border("|","|","-","-"," "," "," "," ")
		self.outerBox.refresh()

	def edit(self):
		self.outerBox = curses.newwin(self.maxh, self.w, self.y, self.x)
		self.outerBox.border("|","|","-","-"," "," "," "," ")
		self.outerBox.refresh()
		innerBox = curses.newwin(self.maxh - 2, self.w - 2, self.y + 1, self.x + 1)
		self.textbox = textpad.Textbox(innerBox)
		return self.textbox.edit()

	def getmaxyx(self):
		(y, x) = self.outerBox.getmaxyx()
		return (y, x)
	
	def getboxyx(self):
		return (self.y, self.x) 
	
	def clear(self):
		self.innerBox.clear()
		self.innerBox.refresh()
		self.outerBox.border(" "," "," "," "," "," "," "," ")
		self.outerBox.refresh()
		self.makeSmall()
	
	def hide(self):
		self.hidden = True
		self.innerBox.clear()
		self.innerBox.refresh()
		self.outerBox.border(" "," "," "," "," "," "," "," ")
		self.outerBox.refresh()
		self.areaWin.clear()
		self.areaWin.refresh()

	def unhide(self):
		self.hidden = False
		self.areaWin.addstr(0, 0, self.prompt)
		self.areaWin.refresh()
		self.makeSmall()
	
	def isHidden(self):
		return self.hidden
