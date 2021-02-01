import mariadb
import sys

def connectToDB():

    try:
        conn = mariadb.connect(
            user="teamhlg",
            password="1FiTUaR2UV8c.X4#p0NW0ofZ0Qic1cI3",
            host="kaifuhome.de",
            port=3307,
            database="hlg"
        )
        #print ("Hello World!")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    global cursor
    cursor = conn.cursor()

def createNewTable(name, nameRow):
    nameTable = name
    nameFirstRow = nameRow
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS {} ({} VARCHAR(255))".format(nameTable, nameFirstRow))
    except mariadb.Error as e:
        print(f"There was an error during Table Creation: {e}")

def createRow(table, name, value):
    try:
        cursor.execute("INSERT INTO {} ({}) VALUES ({})".format(table, name, value))
    except mariadb.Error as e:
        print(f"There was an error during Row creation: {e}")



connectToDB()
createNewTable("users_2", "name")
createRow("users_2", "name", "%s")
