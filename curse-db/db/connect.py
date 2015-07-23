import psycopg2

def read(filename):
    inFile = open('../settings/' + filename).read()
    return inFile

def connect():
    connection_string = read('config.txt')
    try:
        conn = psycopg2.connect(connection_string)
        curr = conn.cursor()
        return curr
    except:
        print "Unable to connect to database"

if __name__ == '__main__':
    connect()
