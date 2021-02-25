from bs4.element import ResultSet
import mariadb
import sys
from colorama import Fore, Back, Style 
from bs4 import BeautifulSoup
import requests
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
        #print ("Hello World!")
    except mariadb.Error as e:
        print(Fore.RED + f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    global cursor
    cursor = conn.cursor()

def createNewTable(name, nameColumn):
    nameTable = name
    nameFirstColumn = nameColumn
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS {} ({} VARCHAR(255))".format(nameTable, nameFirstColumn))
    except mariadb.Error as e:
        print(Fore.RED + f"There was an error during TABLE Creation: {e}")

def createRow(table, columnName, value):
    try:
        query = 'INSERT INTO {} ({}) VALUES ("{}")'.format(table, columnName,value)

        cursor.execute(query)

        conn.commit()
    except mariadb.Error as e:
        print(Fore.RED + f"There was an error during ROW creation: {e}")

def createColumn(nameTable, nameColumn):    
    try:
        cursor.execute("ALTER TABLE {} ADD {} VARCHAR(255) DEFAULT NULL".format(nameTable, nameColumn))
    except mariadb.Error as e:
        print(Fore.RED + f"There was an error during COLUMN Creation: {e}")

counter = 0
captions = []
lastSpace = 0

URL2 = 'https://www.kaifu-gymnasium.de'
pageKFU = requests.get(URL2)
soupKFU = BeautifulSoup(pageKFU.content, 'html5lib')
resultsKFU = soupKFU(class_='fusion-post-content-container')

for result in resultsKFU:
  resultsTextKFU = str(result).split('<div class="fusion-post-content-container"><p> ')
  resultsTextKFU = resultsTextKFU[1]
  resultsTextKFU = resultsTextKFU.split('</p></div>')
  resultsTextKFU = resultsTextKFU[0]
  counter = 1
  while resultsTextKFU[0] == ' ':
    resultsTextKFU = resultsTextKFU[counter:]
    counter += 1
  captions.append(resultsTextKFU)




