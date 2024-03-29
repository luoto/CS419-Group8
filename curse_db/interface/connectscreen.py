import curses
import curses.textpad as textpad
from resultspane import ResultsPane
from inputbox import InputBox
from menu import Menu
import sys
sys.path.append('../utils')
from utils import useDB, getHelp, saveDBInfo, deleteDBInfo, getNicknames

# For navigating the Main Menu menu, selects clicked item and returns its name
def mainMenuNav(mainMenu, x, y):
	itemName = mainMenu.itemAt(y, x)
	if itemName:
		mainMenu.selectOnlyItem(itemName)
	return itemName

# For a click on the Main Menu page, returns "quit", "connected", "failedConnect", or None
def mainMenuClick(x, y, mainMenu, mainMenuNames, databaseInputBoxes, prevDatabasesMenu, prevConnect, prevDelete, newsqlConnect, newpsqlConnect, helpWin):
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
		prevDelete.unhide()
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
			db = useDB(prevDatabasesMenu.getSelected())
			if db is not None:
				hide(databaseInputBoxes)
				hide([prevDatabasesMenu, prevConnect, newsqlConnect, newpsqlConnect])
				helpWin.clear()
				helpWin.refresh()
				return db
			return "failedOldConnect"
	elif prevDelete.itemAt(y, x):
		if prevDatabasesMenu.getSelected() is not None:
			deleteDBInfo(prevDatabasesMenu.getSelected())
			prevDatabasesMenu.deSelectAll()
			prevDatabasesMenu.setItems(getNicknames())
			prevDatabasesMenu.hide()
			prevDatabasesMenu.unhide()
	elif newsqlConnect.itemAt(y, x):
		if connectVia("sql", databaseInputBoxes):
			db = useDB(databaseInputBoxes[4].gather())
			if db is not None:
				helpWin.clear()
				helpWin.refresh()
				return db			
			else:
				deleteDBInfo(databaseInputBoxes[4].gather())
		return "failedConnect"	
	elif newpsqlConnect.itemAt(y, x):
		if connectVia("Psql", databaseInputBoxes):
			db = useDB(databaseInputBoxes[4].gather())
			if db is not None:
				helpWin.clear()
				helpWin.refresh()
				return db			
			else:
				deleteDBInfo(databaseInputBoxes[4].gather())
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
		inputVals[i] = dataInputBoxes[i].gather()
		if inputVals[i] != "":
			numValid += 1
	if numValid == 5:
		# nickname, db, host, port, user, password, vender
		if saveDBInfo(inputVals[4], inputVals[2], inputVals[3], 51232, inputVals[0], inputVals[1], vender):
			return True
	return False

# Calls hide() on each item in the list
def hide(list):
	for item in list:
		item.hide()

