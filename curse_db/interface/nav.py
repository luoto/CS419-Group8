import curses
import curses.textpad as textpad
from tabbar import TabBar
from resultspane import ResultsPane
from inputbox import InputBox
from menu import Menu

# Initialize the standard screen
scr = curses.initscr()
scr.refresh()

# Start up color, then create color pair 1 and 2 (0 is resevered) for tabs
curses.start_color()
SELECTED_COLOR = 1
DESELECTED_TAB_COLOR = 2
curses.init_pair(SELECTED_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(DESELECTED_TAB_COLOR, curses.COLOR_BLACK, curses.COLOR_GREEN)

# Various setting changes
curses.noecho() # so typed letters are not echoed to the screen
#curses.cbreak() # supposedly so keys are processed instantly (no Enter)
scr.nodelay(1) # makes scr.getch() non-blocking
scr.keypad(1) # assigns special characters (such as curses.KEY_LEFT)
curses.curs_set(0) # makes cursor invisible
curses.mousemask(1) # needed to capture mouse click events

# For navigating the Main Menu (returns True if 'Quit' was pressed)
def mainMenuNav(mainMenu, x, y):
	itemName = mainMenu.itemAt(y, x)
	mainMenu.selectOnlyItem(itemName)
	return itemName

# Wait to capture a mouse click
def mouseClick():
	curses.curs_set(0)
	ch = scr.getch()
	return ch == curses.KEY_MOUSE

# Create main menu
mainMenuNames = [" Connect to Database ", " Help ", " Quit "]
mainMenuY = 4
mainMenu = Menu(3, curses.COLS/4, mainMenuY, curses.COLS, mainMenuNames, False, SELECTED_COLOR)

# Create menu for previously connected databases (then hide it)
prevDatabaseNames = ["prevDB1", "prevDB2"]
prevDatabasesMaxX = 20
mainMenuY += 3
prevDatabasesMenu = Menu(mainMenuY, 0, curses.LINES - 10, prevDatabasesMaxX, prevDatabaseNames, True, SELECTED_COLOR)
prevDatabasesMenu.hide()

# Create input boxes
inputPrompts = ["\nusername:", "\npassword:", "\n db name:", "\nhostname:", "\nnickname:"]
databaseInputBoxes = []
databaseInputBoxesX = prevDatabasesMaxX + 2
databaseInputBoxesY = []
for i in range(0, 5): 
	databaseInputBoxesY.append(mainMenuY + i*3)
	databaseInputBoxes.append(InputBox(inputPrompts[i], databaseInputBoxesY[i], databaseInputBoxesX, 1))
	databaseInputBoxes[i].hide()

# Two connect buttons
prevConnect = Menu(curses.LINES - 1, 3, 1, 12, ["connect"])
newConnect = Menu(curses.LINES - 1, databaseInputBoxesX, 1, 12, ["connect"]) 
prevConnect.hide()
newConnect.hide()

# Just for before a database is connected to, only have Main Menu
scr.addstr(0, 0, "Main Menu", curses.color_pair(SELECTED_COLOR))
scr.refresh()
connected = False
quit = False
while not connected:
	if mouseClick():
		(id, x, y, z, s) = curses.getmouse()
		itemName = mainMenuNav(mainMenu, x, y) 
		if itemName == mainMenuNames[0]:
			prevDatabasesMenu.unhide()
			for i in range(0, 5): 
				databaseInputBoxes[i].unhide()
			prevConnect.unhide()
			newConnect.unhide()
		elif itemName == mainMenuNames[2]:
			quit = True
			break
		elif prevConnect.itemAt(y, x):
			connected = True
		elif newConnect.itemAt(y, x):
			connected = True
		elif x > databaseInputBoxesX: 
			for i in range(4, -1, -1):
				if y > databaseInputBoxesY[i]:
					databaseInputBoxes[i].edit()
					break
				
		
# Create the full set of tabs at the top of the screen
tabs = TabBar(["Main Menu", "Tables", "Query", "Search", "Help"], SELECTED_COLOR, DESELECTED_TAB_COLOR)
inTab = "Main Menu"
switchTab = True

# Create Tables menu
tableNames = ["abc", "way too long for this", "third"]
tableMenu = Menu(6, 0, 10, 15, tableNames, True, SELECTED_COLOR)
tableMenu.hide()
	
# Create textBox for edit-able input
inputY = 2
inputPrompt = "\n   Enter Query: \n(ctr-g to submit)"
max_lines = curses.LINES - 10
inputBox = InputBox(inputPrompt, inputY, 0, max_lines)
(y, inputX) = inputBox.getboxyx()

# Create pane for displaying results based on input	
(inputYmax, x) = inputBox.getmaxyx()
w = curses.COLS
paneYwithInput = inputY + inputYmax + 1
h = curses.LINES - paneYwithInput
resultsWin = curses.newwin(h, w, paneYwithInput, 0)
resultsPane = ResultsPane(resultsWin)

# Create pane for non-input pages
mainPaneWin = curses.newwin(curses.LINES - 2, curses.COLS, inputY, 0)
mainPane = ResultsPane(mainPaneWin)

# Main loop, program ends when 'quit' is entered in the textbox
while not quit:
	if switchTab == True:
		switchTab = False	
		mainPane.reset()
		resultsPane.reset()
		mainMenu.hide()
		tableMenu.hide()
		inputBox.hide()		
		if inTab == "Main Menu":
			mainMenu.unhide()
		elif inTab == "Tables":
			mainPane.setResults(["Tables page", "This has not been implemented yet."])	
			
			mainPane.showResults(mainPane.getPageNum())
			tableMenu.unhide()
			tableMenu.selectItem(tableNames[0])
		elif inTab == "Query":
			inputBox.unhide()
		elif inTab == "Search":
			inputBox.unhide()
		elif inTab == "Help":
			mainPane.setResults(["Help page", "This has not been implemented yet.", "Go to Main Menu and click 'Quit' to quit.", "The Query/Search results print your input plus 1-100."])
			mainPane.showResults(mainPane.getPageNum())

	# Be ready to capture a mouse click
	if mouseClick():
		(id, x, y, z, s) = curses.getmouse()
		# if the click was in the (visible) input box
		if not inputBox.isHidden() and (y >= inputY and  y <= inputYmax and x >= inputX):
			# Get whatever the user enters into the textbox
			input = inputBox.edit()
			input = input.strip()
			
			#Display "results"
			resultsPane.reset()
			list = [input]
			for i in range(1, 101):
				list.append(str(i))
			resultsPane.setResults(list)
			resultsPane.showResults(resultsPane.getPageNum())
			
			# Make the textbox clear when next clicked on
			inputBox.clear()
		
		# if the click in the tab bar at the top of the screen
		elif y == 0:
			# select the tab at the x-position of the click
			newTab = tabs.selectTabAt(x)
			if newTab and newTab != inTab:
				inTab = newTab
				switchTab = True	
		# if the click is at the bottom of the screen (prev/next)
		elif y == curses.LINES - 1 and (inTab == "Query" or inTab == "Search"):
			if resultsPane.atNext(x):
				resultsPane.showResults(resultsPane.getPageNum() + 1)
			elif resultsPane.atPrev(x):
				resultsPane.showResults(resultsPane.getPageNum() - 1)
		elif inTab == "Tables" and tableMenu.itemAt(y, x):
			tableMenu.selectOnlyItem(tableMenu.itemAt(y, x))
		elif inTab == "Main Menu" and mainMenu.itemAt(y, x):
			if mainMenuNav(mainMenu, x, y) == mainMenuNames[2]:
				quit = True

# Make sure to clean up whatever window mode we may have gotten into
curses.echo()
curses.curs_set(1)
curses.endwin()

