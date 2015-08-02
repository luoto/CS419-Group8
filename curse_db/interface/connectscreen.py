import curses
import curses.textpad as textpad
from resultspane import ResultsPane
from inputbox import InputBox
from menu import Menu

# For navigating the Main Menu menu, selects clicked item and returns its name
def mainMenuNav(mainMenu, x, y):
	itemName = mainMenu.itemAt(y, x)
	if itemName:
		mainMenu.selectOnlyItem(itemName)
	return itemName

# For a click on the Main Menu page, returns "quit", "connected", "failedConnect", or None
def mainMenuClick(x, y, mainMenu, mainMenuNames, databaseInputBoxes, prevDatabasesMenu, prevConnect, newConnect):
	itemName = mainMenuNav(mainMenu, x, y) 
	(temp, databaseInputBoxesX) = databaseInputBoxes[0].getboxyx()
	databaseInputBoxesY = []
	for i in range(0, 5):
		(inputY, temp) = databaseInputBoxes[i].getboxyx()
		databaseInputBoxesY.append(inputY)
	if itemName == mainMenuNames[0]:
		prevDatabasesMenu.unhide()
		for i in range(0, 5): 
			databaseInputBoxes[i].unhide()
		prevConnect.unhide()
		newConnect.unhide()
	elif itemName == mainMenuNames[2]:
		return "quit"
	elif prevConnect.itemAt(y, x):
		hide(databaseInputBoxes)
		hide([prevDatabasesMenu, prevConnect, newConnect])
		return "connected"
	elif newConnect.itemAt(y, x):
		inputVals = ["","","","",""]
		numValid = 0	
		for i in range(0, 5):
			inputVals[i] = databaseInputBoxes[i].clear()
			if inputVals[i] != "":
				numValid += 1
		if numValid == 5:
			return "connected"
		else:
			return "failedConnect"
	elif x > databaseInputBoxesX: 
		for i in range(4, -1, -1):
			if y > databaseInputBoxesY[i]:
				databaseInputBoxes[i].edit()
				break
	return None

# Calls hide() on each item in the list
def hide(list):
	for item in list:
		item.hide()

