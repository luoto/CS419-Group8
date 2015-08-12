import psycopg2
import pymysql

# TODO: Implement methods for the Mysql class

class DB:
    """Generic class that is meant to be used as an interface for subclasses.

    This class is not meant to be used directly. It provides a template for
    subclasses that deal specifically with vendors.
    """

    def __init__(self):
        pass

    def _read(self, fname):
        inFile = open('../settings/' + fname).read()
        return inFile

    def connect(self):
        pass


class Psql(DB):
    """This class handles all connections and queries related to PostgreSQL.

    """
    def __init__(self):
        DB.__init__(self)
        self.connection = None
        self.cursor = None


    def connect(self, connection_string):
        """Establishes a connection to the database provided by the user

        Returns:
            A boolean, True if a connection has been successfully made, otherwise
            will return false
        """
        #connection_string = self._read('config.txt')
        try:
            self.connection = psycopg2.connect(connection_string)
            self.cursor = self.connection.cursor()
            return True
        except psycopg2.Error, e:
            return False
            print e


    def getTables(self):
        """Returns tables to the user in the form of a list of strings"""
        results = []

        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

        results = self.cursor.fetchall()
        results = map(lambda result: result[0], results)
        return results


    def getTableInfo(self, table_name):
        """ Returns column and datatype of that column """
        results = []

        self.cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}'".format(table_name))

        results = self.cursor.fetchall()
        results = map(lambda result: result[0] + "\t" + result[1], results)
        return results


    def search(self):
        # get results for the table
        pass


    def executeQuery(self, query):
        """ Executes query and returns the result in a list of strings.

        Args:
            query: The query string.

        Returns:
            A list of tuples corresponding to rows of data fetched from the
            database.
        """
        results = []

        def formatRow(row):
            """Helper function to format each row"""
            result = ""
            first = True
            for item in row:
                if first == True:
                    result += str(item)
                    first = False
                else:
                    result += "\t" + str(item)
            return result

        try:
            self.cursor.execute(query)
        except:
            return False

        results = self.cursor.fetchall()
        results = map(formatRow, results)

        return results


    def closeConnection(self):
        self.connection.close();
        return True


class Mysql(DB):
    """This class handles all connections and queries related to MySQL.

    """
    def __init__(self):
        DB.__init__(self)
        self.conn = None
        self.cursor = None

    def connect(self):#connection_string
        #connection_string = self._read('config.txt')
        self.conn = pymysql.connect(host='45.55.19.163', port=3306, user='anderleo', password='helloworld', db='testDB')
        #self.conn = pymysql.connect(connection_string)
        self.cursor = self.conn.cursor()

    def getTables(self):
        """Returns tables to the user in the form of a list of strings"""

        print 'Here are the MYSQL tables!!!'
        results = []
        self.cursor.execute("SHOW TABLES;")
        results = self.cursor.fetchall()
        results = map(lambda result: result[0], results)
        return results

    def getTableInfo(self, table_name):
        """ Returns column and datatype of that column """
        results = []

        self.cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}'".format(table_name))

        results = self.cursor.fetchall()
        results = map(lambda result: result[0] + "\t" + result[1], results)
        return results

    def executeQuery(self, query):
        """ Executes query and returns the result in a list of strings."""
        results = []

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.conn.commit()
        return results

    def search(self, table, field, string):
        # get results for the table
        results = []
        query = "SELECT * FROM " + table + " WHERE " + field + " LIKE '%" + string + "%'"

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def closeConnection(self):
        self.conn.close();
        return True

if __name__ == '__main__':
    db = Mysql()
    db.connect()     #--|___ Formly cursor = db.connect(), I had to split these two up
    #cursor = db.cursor(conn)#--|    so that I could use both the cursor and the conn (commits)
    #                               in global calls
    # #Test of getTables()
    #results = db.getTables()
    #for x in results:
    #    print x
    #
    # #Test of getTableInfo()
    #table_name = "heroes"
    #results = db.getTableInfo(table_name)
    #for x in results:
    #     print x
    #
    # #Test of executeQuery() - CREATE TABLE
    #query = "CREATE TABLE FavoriteHeroes(name VARCHAR(200), age INT);"
    #querySuccess = db.executeQuery(query)
    #print querySuccess
    #
    # #Test of executeQuery() - INSERT
    #query = "INSERT INTO FavoriteHeroes (name) VALUES('Spiderman');"
    #querySuccess = db.executeQuery(query)
    #print querySuccess
    #
    # #Test of executeQuery() - UPDATE
    #query = "UPDATE FavoriteHeroes SET age=50 WHERE name='Spiderman';"
    #querySuccess = db.executeQuery(query)
    #print querySuccess
    #
    # #Test of executeQuery() - SELECT *
    #query = "SELECT * FROM heroes;"
    #querySuccess = db.executeQuery(query)
    #print querySuccess
    #
    # Test of Search()
    #field = "name"
    #table_name = "cars"
    #string = "Ca"
    #querySuccess = db.search(cursor, table_name, field, string)
    #print querySuccess

    # PostgreSQL
    # Example use case
    # db = Psql()
    # result = db.connect("dbname=curses host=localhost user=postgres password=helloworld")
    # print db.getTables()
    # print db.getTableInfo("movies")
    # print db.executeQuery("SELECT sdgsdkkee sdf")
    # db.closeConnection()
    db.closeConnection()
