import sys
import curses
import curses.textpad as textpad
# In current directory
from tabbar import TabBar
from resultspane import ResultsPane
from inputbox import InputBox
from menu import Menu
from connectscreen import mainMenuNav, mainMenuClick, hide
# In sibling utils directory
sys.path.append('../utils')
from utils import getNicknames, getHelp

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

# Wait to capture a mouse click
def mouseClick():
	curses.curs_set(0)
	ch = scr.getch()
	return ch == curses.KEY_MOUSE

# Create main menu
mainMenuNames = [" Connect to Database ", " Help ", " Quit "]
mainMenuY = 2
mainMenu = Menu(mainMenuY, curses.COLS/4, len(mainMenuNames), curses.COLS, mainMenuNames, False, SELECTED_COLOR)

# Create window to use to clear everything but the tab bar area
helpWin = curses.newwin(curses.LINES - mainMenuY + 3, curses.COLS, mainMenuY + 3, 0)

# Create menu for previously connected databases (then hide it)
prevDatabaseNames = getNicknames()
prevDatabasesMaxX = 20
mainMenuY += 4
prevDatabasesMenu = Menu(mainMenuY, 0, curses.LINES - 9, prevDatabasesMaxX, prevDatabaseNames, True, SELECTED_COLOR)
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

# Three connect buttons and a delete button for the previously save DBs
prevConnect = Menu(curses.LINES - 1, 0, 1, 12, ["connect"])
prevDelete = Menu(curses.LINES - 1, 10, 1, 12, ["delete"])
newsqlConnect = Menu(curses.LINES - 1, databaseInputBoxesX, 1, 16, ["sql connect"]) 
newpsqlConnect = Menu(curses.LINES - 1, databaseInputBoxesX + 20, 1, 17, ["psql connect"]) 
prevConnect.hide()
prevDelete.hide()
newsqlConnect.hide()
newpsqlConnect.hide()

# Just for before a database is connected to, only have Main Menu
scr.addstr(0, 0, "Main Menu", curses.color_pair(SELECTED_COLOR))
scr.refresh()
connected = False
quit = False
while not connected:
	if mouseClick():
		(mid, x, y, z, s) = curses.getmouse()
		response = mainMenuClick(x, y, mainMenu, mainMenuNames, databaseInputBoxes, prevDatabasesMenu, prevConnect, prevDelete, newsqlConnect, newpsqlConnect, helpWin)
		if response == "quit":
			quit = True
			break
		elif response == "failedConnect":
			scr.addstr(curses.LINES - 2, databaseInputBoxesX, "Make sure all 5 fields are valid.")
			scr.refresh()
		elif response == "failedOldConnect":
			scr.addstr(curses.LINES - 2, 0, "Problem connecting to database.")
			scr.refresh()
		elif isinstance(response, str):
			# clear failed connect space
			scr.addstr(curses.LINES - 2, 0, "                                                                           ");
			scr.addstr(6, 0, response)
			scr.refresh()
		elif response:
			db = response
			connected = True

# Create the full set of tabs at the top of the screen
tabs = TabBar(["Main Menu", "Tables", "Query", "Help"], SELECTED_COLOR, DESELECTED_TAB_COLOR)
inTab = "Main Menu"
switchTab = True

# Create Tables menu
if connected:
	tableNames = db.getTables()
	tableMenu = Menu(3, 0, curses.LINES - 3, 15, tableNames, True, SELECTED_COLOR)
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
mainPaneWin = curses.newwin(curses.LINES - 3, curses.COLS - 16, 3, 16)
mainPane = ResultsPane(mainPaneWin)

# Create buttons for Help tab
helpOptions = ["menu", "tables", "query"]
helpTab = helpOptions[0]
helpButtons = []
offset = 0
for i in range(0, len(helpOptions)):
	helpButtons.append(Menu(2, offset, 1, 10, [helpOptions[i]], False, SELECTED_COLOR))
	helpButtons[i].hide()
	offset += len(helpOptions[i]) + 3
helpButtons[0].selectItem(helpTab)

# Main loop, program ends when 'quit' is entered in the textbox
while not quit:
	if switchTab == True:
		switchTab = False	
		scr.clear()
		scr.refresh()
		tabs.selectOnlyTab(inTab)
		mainPane.reset()
		resultsPane.reset()
		hide([mainMenu, tableMenu, inputBox])		
		if inTab == "Main Menu":
			mainMenu.unhide()
		elif inTab == "Tables":
			tableNames = db.getTables()
 			tableMenu.setItems(tableNames)
			tableMenu.unhide()
			if len(tableNames) > 0:
				tableMenu.selectItem(tableNames[0])
				mainPane.setResults(db.getTableInfo(tableMenu.getSelected()))	
				mainPane.showResults(mainPane.getPageNum())
				
		elif inTab == "Query":
			inputBox.unhide()
		elif inTab == "Search":
			inputBox.unhide()
		elif inTab == "Help":
			for b in helpButtons:
				b.unhide()	
				b.selectOnlyItem(helpTab)
			helpWin.addstr(0, 0, getHelp(helpTab))
			helpWin.refresh()

	# Be ready to capture a mouse click
	if mouseClick():
		(mid, x, y, z, s) = curses.getmouse()
		
		# if the click in the tab bar at the top of the screen
		if y == 0:
			# select the tab at the x-position of the click
			newTab = tabs.selectTabAt(x)
			if newTab and newTab != inTab:
				inTab = newTab
				switchTab = True
			
		# Click anywhere on Main Menu page
		elif inTab == "Main Menu":
			response = mainMenuClick(x, y, mainMenu, mainMenuNames, databaseInputBoxes, prevDatabasesMenu, prevConnect, prevDelete, newsqlConnect, newpsqlConnect, helpWin)
			if response == "quit":
				quit = True
			elif response == "failedConnect":
				scr.addstr(curses.LINES - 2, databaseInputBoxesX, "Must provide all 5 fields.")
				scr.refresh()
			elif response == "failedOldConnect":
				scr.addstr(curses.LINES - 2, 0, "Problem connecting to database.")
				scr.refresh()
			elif isinstance(response, str):
				# clear failed connect space
				scr.addstr(curses.LINES - 2, 0, "                                                                           ");
				scr.addstr(6, 0, response)
				scr.refresh()
			elif response:
				db = response
				connected = True
		
		# Click in Tables menu
		elif inTab == "Tables" and tableMenu.itemAt(y, x):
			tableMenu.selectOnlyItem(tableMenu.itemAt(y, x))
		
		# if the click was in the Query or Search input box
		if not inputBox.isHidden() and (y >= inputY and  y <= inputYmax and x >= inputX):
			# Get whatever the user enters into the textbox
			queryInput = inputBox.edit()
			
			#Display "results"
			resultsPane.reset()
			queryResults = db.executeQuery(queryInput)
			if queryResults != False:
				resultsPane.setResults(queryResults)
			else:
				resultsPane.setResults(["Error in query"])
			resultsPane.showResults(resultsPane.getPageNum())
			
			# Make the textbox clear when next clicked on
			inputBox.clear()

		# If the click is at the bottom of the Query or Seach screen 
		elif y == curses.LINES - 1 and (inTab == "Query" or inTab == "Search"):
			if resultsPane.atNext(x):
				resultsPane.showResults(resultsPane.getPageNum() + 1)
			elif resultsPane.atPrev(x):
				resultsPane.showResults(resultsPane.getPageNum() - 1)
		elif inTab == "Help":
			for b in helpButtons:
				if b.itemAt(y, x):
					helpTab = b.itemAt(y, x)
					switchTab = True
		

# Make sure to clean up whatever window mode we may have gotten into
curses.echo(True)
curses.curs_set(True)
curses.endwin()

