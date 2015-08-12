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

    def connect(self):
        #connection_string = self._read('config.txt')
        conn = pymysql.connect(host='45.55.19.163', port=3306, user='anderleo', password='helloworld', db='testDB')
        #curr = conn.cursor()
        return conn

    def cursor(self,conn):
        curr = conn.cursor()
        return curr

    def getTables(self, cursor):
        """Returns tables to the user in the form of a list of strings"""

        print 'Here are the MYSQL tables!!!'
        results = []
        cursor.execute("SHOW TABLES;")
        results = cursor.fetchall()
        results = map(lambda result: result[0], results)
        return results

    def getTableInfo(self, table_name):
        """ Returns column and datatype of that column """
        results = []

        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}'".format(table_name))

        results = cursor.fetchall()
        results = map(lambda result: result[0] + "\t" + result[1], results)
        return results

    def executeQuery(self, query, cursor, conn):
        """ Executes query and returns the result in a list of strings."""
        results = []

        cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        return results

    def search(self, cursor, table, string):
        # get results for the table
        results = []
        query = "SELECT * FROM " + table + " WHERE name LIKE '%" + string + "%'"

        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def closeConnection(self, connection):
        connection.close();
        return True

    def commit(self):
        conn.commit()

if __name__ == '__main__':
    db = Mysql()
    conn = db.connect()     #--|___ Formly cursor = db.connect(), I had to split these two up
    cursor = db.cursor(conn)#--|    so that I could use both the cursor and the conn (commits)
    #                               in global calls
    # #Test of getTables()
    #results = db.getTables(cursor)
    #for x in results:
    #    print x
    #
    # #Test of getTableInfo()
    table_name = "cars"
    #results = db.getTableInfo(table_name)
    #for x in results:
    #     print x
    #
    # #Test of executeQuery()
    #query = "INSERT INTO cars (name) VALUES ('Camero');"
    #querySuccess = db.executeQuery(query, cursor, conn)
    #print querySuccess

    #query = "SELECT * FROM cars;"
    #querySuccess = db.executeQuery(query, cursor, conn)
    #print querySuccess

    querySuccess = db.search(cursor, "cars", "Ca")
    print querySuccess

    # PostgreSQL
    # Example use case
    # db = Psql()
    # result = db.connect("dbname=curses host=localhost user=postgres password=helloworld")
    # print db.getTables()
    # print db.getTableInfo("movies")
    # print db.executeQuery("SELECT sdgsdkkee sdf")
    # db.closeConnection()
    db.closeConnection(cursor)
