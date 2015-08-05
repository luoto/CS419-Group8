import sys
sys.path.append('../db')
import connect


def getTables():
    pass


def executeQuery(query):
    """ Executes query and returns the result in a list of tuples.

    Args:
        query: The query string.

    Returns:
        A list of tuples corresponding to rows of data fetched from the
        database.
    """
    results

    # TODO: Import cursor from db depending on vendor
    cursor.execute(query)
    results = cursor.fetchall()

    return results


def loadDBInfo():
    """ Returns a list of available connections

    Returns:
        A list of available connections
    """
    connectionList = []
    with open("../settings/config.txt", "r") as f:
        connections = f.readlines()

    return map(lambda connection: connection.strip(), connections)


def deleteDBInfo(index):
    connections = loadDBInfo()
    connections.pop(1)
    print(connections)

    f = open("../settings/config.txt", "w")
    for connection in connections:
        f.write(connection)
    f.close


def updateDBInfo(index, connection):
    pass


def saveDBInfo(connection):
    """ Saves connection to the connection file

    """
    with open("../settings/config.txt", "a") as f:
        f.write(connection)


def useDB(connection):
    pass


def getHelp(tabName):
    """ Returns the contents of a help file tabName

    Args:
        tabname: The name of the help file without extensions
    """
    contents = ""

    fname = "../interface/help/" + tabName + ".txt"

    with open(fname, "r") as f:
        contents = f.read()

    return contents


def arrayify(query_string):
    """ Turns a string into a list, splitting done based on white spaces.

    Args:
        query_string: The query string to be converted.

    Returns:
        A list of words from the query_string.
    """
    query_array = query_string.strip().split()
    return query_array


if __name__ == '__main__':
    """Quick Tests"""
    # print arrayify("flavor blasted")

    # print loadDBInfo()

    # print getHelp("main_menu")

    # saveDBInfo("host='00.00.00.000' port=3306 user='super' password='helloworld' dbname='testDB3'")
    # print loadDBInfo()

    # print deleteDBInfo(1)
    # print loadDBInfo()
