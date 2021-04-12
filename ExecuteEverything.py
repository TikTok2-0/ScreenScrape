import mariadb
from colorama import Fore, Back, Style
import sys

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
        #print ("Hello World!")
    except mariadb.Error as e:
        print(Fore.RED + f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    global cursor
    cursor = conn.cursor()

connectToDB()

import titlesAndCaptions
import pictures 
import dateTextCategory
import linksVideos
import paragraphs
import jsonExportTest
import jsonExportTestMAC
import gitPush