import psycopg2
import pymysql

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

    def connect(self):
        connection_string = self._read('config.txt')
        print connection_string
        try:
            conn = psycopg2.connect(connection_string)
            curr = conn.cursor()
            return curr
        except psycopg2.Error, e:
            print e


class Mysql(DB):
    """This class handles all connections and queries related to MySQL.

    """
    def __init__(self):
        DB.__init__(self)

    def connect(self):
        connection_string = self._read('config.txt')
        print connection_string
        conn = pymysql.connect(host='45.55.19.163', port=3306, user='anderleo', password='helloworld', db='testDB')
        curr = conn.cursor()
        return curr

if __name__ == '__main__':
    db = Mysql()
    cursor = db.connect()
    if cursor.execute("SHOW TABLES"):
        print 'Connection Successful - Database live!'