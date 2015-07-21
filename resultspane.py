import curses

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

