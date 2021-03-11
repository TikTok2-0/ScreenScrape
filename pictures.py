import mariadb
import sys
from colorama import Fore, Back, Style 
from bs4 import BeautifulSoup
import requests

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

URL1 = 'https://www.hlg-hamburg.de'
pageHLG = requests.get(URL1)
soupHLG = BeautifulSoup(pageHLG.content, 'html5lib')
resultsHLG = soupHLG("img")
cleanList = []
counter = 1

for result in resultsHLG:
    convText = str(result)
    splitList = convText.split('src="')
    linkContainer = splitList[1]
    linkContainer = linkContainer[:-3]

    if 'uploads' in linkContainer and '/2014/08/London' not in linkContainer and 'DSCI02952' not in linkContainer and 'logo-footer' not in linkContainer and 'uploads/2019/06/logo.png' not in linkContainer:
        cleanList.append(linkContainer)

counter = 0
pics = []
lastSpace = 0

while len(cleanList) > 6:
    cleanList.pop(0)

print(len(cleanList))

URL2 = 'https://www.kaifu-gymnasium.de'
pageKFU = requests.get(URL2)
soupKFU = BeautifulSoup(pageKFU.content, 'html5lib')
resultsKFU = soupKFU(class_='fusion-image-wrapper')

for result in resultsKFU:
  resultsTextKFU = str(result).split('src="')
  resultsTextKFU = resultsTextKFU[1]
  resultsTextKFU = resultsTextKFU.split('class=')
  resultsTextKFU = resultsTextKFU[0]
  resultsTextKFU = resultsTextKFU.split('" srcset=')
  resultsTextKFU = resultsTextKFU[0]
  counter = 1
  while resultsTextKFU[0] == ' ':
    resultsTextKFU = resultsTextKFU[counter:]
    counter += 1
  cleanList .append(resultsTextKFU)

connectToDB()

cursor.execute("DELETE FROM jsonStorage WHERE imageURL")
conn.commit() 

for item in cleanList:
  try:
    cursor.execute('UPDATE jsonStorage SET imageURL = "{}" WHERE id = "{}"'.format(item, counter))
    conn.commit()
    counter += 1
  except mariadb.Error as e:
    print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")

