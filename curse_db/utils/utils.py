import json
import sys
sys.path.append('../db')
import connect

# TODO: Write documentation for each of the functions
# TODO: Ensure that all methods are working for MySQL
# TODO: Increase function robustness by handling edge cases and errors

def useDB(nickname):
    """ Establishes and returns connection to a database with the nickname provided"""
    connections = loadDBInfo()
    connection_string = map(lambda connection: connection["connection_string"],filter(lambda connection: connection["nickname"] == nickname, connections))[0]

    connection_string
    db = connect.Psql()
    db.connect(connection_string)
    return db


def getNicknames():
    """ Returns stored nicnames in a list of strings """
    connections = loadDBInfo();
    return map(lambda connection: connection["nickname"], connections)

def loadDBInfo():
    """ Returns a list of available connections

    Returns:
        A list of available connections
    """
    # check nickname
    f = open("../settings/config.txt", "r")
    connections = f.read()
    f.close()
    return json.loads(connections)


def deleteDBInfo(index):
    # Needs to be refactored - do not use
    connections = loadDBInfo()
    connections.pop(index)
    print(connections)

    f = open("../settings/config.txt", "w")
    for connection in connections:
        f.write(connection)
    f.close


def updateDBInfo(index, connection):
    pass


def saveDBInfo(nickname, dbname, host, port, user, password, vendor):
    """ Saves connection to the connection file as a JSON object"""

    connection_string = "dbname={} host={} user={} password={}".format(dbname, host, user, password)

    connection = {"nickname": nickname, "connection_string": connection_string, "vendor": vendor}

    connections = loadDBInfo()
    connections.append(connection)
    f = open("../settings/config.txt", "w")
    f.write(json.dumps(connections))
    f.close

    return True


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
    # {nickname: "leonard", connection_string: "'host='45.55.19.163' port=3306 user='anderleo' password='helloworld' dbname='testDB'" type: "Mysql"}

    # print arrayify("flavor blasted")

    # print loadDBInfo()

    # print getHelp("main_menu")

    # saveDBInfo("host='00.00.00.000' port=3306 user='super' password='helloworld' dbname='testDB3'")
    # print loadDBInfo()

    # print deleteDBInfo(1)
    # print loadDBInfo()

    #print loadDBInfo()
    #saveDBInfo("tony", "curses", "localhost", 51232, "postgres", "password", "Psql")
    #getNicknames()

    # Example
    myDB = useDB('tony')
    print myDB.getTables()
    print myDB.executeQuery("SELECT * FROM movies")
