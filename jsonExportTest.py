import mariadb
import sys
from colorama import Fore, Back, Style 
import json

def connectToDB():
    try:
        global conn
        conn = mariadb.connect(
            user="teamhlg",
            password="1FiTUaR2UV8c.X4#p0NW0ofZ0Qic1cI3",
            host="kaifuhome.de",
            port=3307,
            database="hlg"
        )
    except mariadb.Error as e:
        print(Fore.RED + f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    global cursor
    cursor = conn.cursor()

def query_db(query, args=(), one=False):
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) \
        for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()
    return (r[0] if r else None) if one else r

connectToDB()

my_query = query_db("SELECT * FROM jsonStorage LIMIT %s", (6,))

json_output = json.dumps(my_query, ensure_ascii = False)

with open("jsonExports.json", "w") as outfile: 
  outfile.write(json_output)