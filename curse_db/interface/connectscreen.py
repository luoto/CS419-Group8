import curses
import curses.textpad as textpad
from resultspane import ResultsPane
from inputbox import InputBox
from menu import Menu
import sys
sys.path.append('../utils')
from utils import useDB, getHelp, saveDBInfo

# For navigating the Main Menu menu, selects clicked item and returns its name
def mainMenuNav(mainMenu, x, y):
	itemName = mainMenu.itemAt(y, x)
	if itemName:
		mainMenu.selectOnlyItem(itemName)
	return itemName

# For a click on the Main Menu page, returns "quit", "connected", "failedConnect", or None
def mainMenuClick(x, y, mainMenu, mainMenuNames, databaseInputBoxes, prevDatabasesMenu, prevConnect, newsqlConnect, newpsqlConnect, helpWin):
	itemName = mainMenuNav(mainMenu, x, y) 
	(temp, databaseInputBoxesX) = databaseInputBoxes[0].getboxyx()
	databaseInputBoxesY = []
	for i in range(0, 5):
		(inputY, temp) = databaseInputBoxes[i].getboxyx()
		databaseInputBoxesY.append(inputY)
	if itemName == mainMenuNames[0]:
		helpWin.clear()
		helpWin.refresh()
		prevDatabasesMenu.unhide();
		for i in range(0, 5): 
			databaseInputBoxes[i].unhide()
		prevConnect.unhide()
		newsqlConnect.unhide()
		newpsqlConnect.unhide()
	elif itemName == mainMenuNames[1]: # help
		helpWin.clear()
		helpWin.refresh()
		hide(databaseInputBoxes)
		hide([prevDatabasesMenu, prevConnect, newsqlConnect, newpsqlConnect])
		helpWin.addstr(0, 0, getHelp("menu"))
		helpWin.refresh()
	elif itemName == mainMenuNames[2]:
		return "quit"
	elif prevConnect.itemAt(y, x):
		if prevDatabasesMenu.getSelected():
			hide(databaseInputBoxes)
			hide([prevDatabasesMenu, prevConnect, newsqlConnect, newpsqlConnect])
			return useDB(prevDatabasesMenu.getSelected())
		else:
			return "failedOldConnect"
	elif newsqlConnect.itemAt(y, x):
		return connectVia("sql", databaseInputBoxes)
	elif newpsqlConnect.itemAt(y, x):
		inputVals = ["","","","",""]
		numValid = 0	
		for i in range(0, 5):
			inputVals[i] = databaseInputBoxes[i].clear()
			if inputVals[i] != "":
				numValid += 1
		if numValid == 5:
			# nickname, db, host, port, user, password, vender
			saveDBInfo(inputVals[4], inputVals[2], inputVals[3], 51232, inputVals[0], inputVals[1], "Psql")
			return useDB(inputVals[4])
		else:
			return "failedConnect"
	elif prevDatabasesMenu.itemAt(y, x):
		prevDatabasesMenu.selectOnlyItem(prevDatabasesMenu.itemAt(y, x))
	elif x > databaseInputBoxesX: 
		for i in range(4, -1, -1):
			if y > databaseInputBoxesY[i]:
				databaseInputBoxes[i].edit()
				break
	return None

def connectVia(vender, dataInputBoxes):
	inputVals = ["","","","",""]
	numValid = 0	
	for i in range(0, 5):
		inputVals[i] = dataInputBoxes[i].clear()
		if inputVals[i] != "":
			numValid += 1
	if numValid == 5:
		# nickname, db, host, port, user, password, vender
		saveDBInfo(inputVals[4], inputVals[2], inputVals[3], 51232, inputVals[0], inputVals[1], vender)
		return "connected"
	else:
		return "failedConnect"

# Calls hide() on each item in the list
def hide(list):
	for item in list:
		item.hide()

