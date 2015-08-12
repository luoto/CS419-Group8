import json
import sys
sys.path.append('../db')
import connect

def useDB(nickname):
    """ Establishes and returns connection to a database with the nickname provided"""
    connections = loadDBInfo()

    # check if exist
    if nickname not in getNicknames():
        print 'Not in nicknames...'
        return False

    vendor, connection_string = map(lambda connection: (connection["vendor"], connection["connection_string"]),filter(lambda connection: connection["nickname"] == nickname, connections))[0]

    if vendor == "Psql":
        db = connect.Psql()
        if db.connect(connection_string) is False:
            return None
    elif vendor == "Mysql":
        db = connect.Mysql()
        connection_string = arrayify(connection_string)
        if db.connect(connection_string) is False:
            return None
    else:
        return False

    return db


def getNicknames():
    """ Returns stored nicknames in a list of strings """
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


def deleteDBInfo(nickname):
    connections = loadDBInfo()
    # find index of nickname
    connections = filter(lambda connection: connection["nickname"] != nickname, connections)
    f = open("../settings/config.txt", "w")
    f.write(json.dumps(connections))
    f.close

    return True

def updateDBInfo(index, connection):
    pass


def saveDBInfo(nickname, dbname, host, port, user, password, vendor):
    """ Saves connection to the connection file as a JSON object"""

    # check for supported vendors
    if vendor != "Psql" and vendor != "Mysql":
        return False

    # check for duplicates nicknames
    nicknames = getNicknames()
    for name in nicknames:
        if name == nickname:
            return False

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
    query_array = query_string.strip().split(' ,')
    query_array = query_string.strip().split(',')
    query_array = map(lambda item: item.strip(), query_array)
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

    # myDB = useDB("tony")
    # print myDB.getTables()

    # Example
    # myDB = useDB('david')
    # cursor = myDB.connect()
    # myDB.executeQuery("CREATE TABLE newTable10( name VARCHAR(200), age INT);", cursor)
    # print myDB.getTables(cursor)


    # TEST ERROR HANDLERS
    # print saveDBInfo('tony', '1', '1', '1', '1', '1', 'Mysql')
    # print saveDBInfo('joe', '1', '1', '1', '1', '1', 'MelonSql')
    # print saveDBInfo('joe', '1', '1', '1', '1', '1', 'Psql')
    # print saveDBInfo("tony", 1, 1, 1, 1, 1, "Psql")

    # myDB = useDB("tony")
    # print myDB.executeQuery("SELECT * FROM movies WHERE title = 'Deadpool'")
    # saveDBInfo("George", "test", "localhost", "3000", "admin", "123", "Psql")
    # print loadDBInfo()

    # # deleteDBInfo('tony')
    myDB = useDB('david')
    print myDB.executeQuery("SELECT * FROM cars")
