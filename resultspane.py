import curses

# Hand it the window where the pane should display its results.  Use 
# setResults(list) to hand it the list of strings, then call showResults(num)
# to actually show the results (for the page number num)
class ResultsPane():
	def __init__(self, win):
		self.win = win
		(y, x) = self.win.getmaxyx()
		self.lines = y - 1
		self.cols = x
		self.reset()
		self.NEXT = "[Next->]"
		self.PREV = "[<-Prev]"

	def setResults(self, list):
		self.curPage = 0
		self.results = list
		self.numResults = len(list)
		self.numPages = int(.5 + self.numResults/self.lines)
		#determine how many \n are in str, compare to number of lines
		#in the pane. Break str into that many parts (in a list)?
		
	def hasPrev(self):
		return self.curPage > 0
	
	def hasNext(self):
		return self.curPage < self.numPages

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
