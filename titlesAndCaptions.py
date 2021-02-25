import mariadb
import sys
from colorama import Fore, Back, Style 
from bs4 import BeautifulSoup
import requests
import json

### DB FUNCTIONS ###

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

def ScrapeCleanup(results):
  resultsText = results.text
  stringArray = []
  lastSpace = 0
  
  for i in range(len(resultsText)):
    if (resultsText[i]=="\n"):
      stringArray.append(resultsText[lastSpace:i]) 
      lastSpace = i

  
  for i in range(5):
    for satz in stringArray:
      if(satz == "\n"):
        stringArray.remove(satz) 

  
  stringArray2 = []
  for satz in stringArray:
    while "\n" in satz:
      satz = satz[:satz.find("\n")] + satz[satz.find("\n")+1:]
    while "weiterlesen" in satz:
      satz = satz[:satz.find("weiterlesen")] + satz[satz.find("weiterlesen")+12:]
    stringArray2.append(satz)  
  stringArray = stringArray2
  
  for satz in stringArray:
    if satz == '' or satz == ' ':
      stringArray.remove(satz)
          
  
  return stringArray

### DB FUNCTIONS ENDE ###


connectToDB()


### HLG ###

counter = 0
titles = []
captions = []

URL1 = 'https://www.hlg-hamburg.de'
pageHLG = requests.get(URL1)
soupHLG = BeautifulSoup(pageHLG.content, 'html.parser')
resultsHLG = soupHLG.find(class_='archive')

dictTestT = dict()
counterT = 0
dictTestC = dict()
counterC = 0
finalDict = dict()
counterF = 0

createNewTable("jsonStorage", "title")

cursor.execute("DELETE FROM jsonStorage")

cleanResultsHLG = ScrapeCleanup(resultsHLG)

while (counter < len(cleanResultsHLG)-1):
  if counter%2 == 0:
    titles.append(cleanResultsHLG[counter])
    counter = counter+1
  elif counter%2 != 0: 
    captions.append(cleanResultsHLG[counter])
    counter = counter+1

### HLG ENDE ###


### KAIFU TITEL ###

URL2 = 'https://www.kaifu-gymnasium.de'
pageKFU = requests.get(URL2)
soupKFU = BeautifulSoup(pageKFU.content, 'html5lib')
resultsKFU = soupKFU(id='content')

for result in resultsKFU:
  resultsTextKFU = str(result).split('aria-label="')
  for item in resultsTextKFU:
    itemList = item.split('/">')
    item = itemList[0]
    if item[0] != '<':
      itemList = item.split('" href')
      item = itemList[0]
      print (item)
      titles.append(item)

### KAIFU TITEL ENDE ###


### KAIFU CAPTIONS ###

counter = 0
#captions = []
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

### DB PUSH ###

titles.append("dummy")
captions.append("dummy")

counter2 = 0
for title in titles:
  try:
    createRow("jsonStorage", "title", title)
    if counter2 < 12:
      cursor.execute('UPDATE jsonStorage SET caption = "{}" WHERE title = "{}"'.format(captions[counter2], title))
    cursor.execute('UPDATE jsonStorage SET id = "{}" WHERE title = "{}"'.format(counter2+1, title))
    if counter2 >= 6:
      cursor.execute('UPDATE jsonStorage SET school = "{}" WHERE title = "{}"'.format('KFU', title))
    else:
      cursor.execute('UPDATE jsonStorage SET school = "{}" WHERE title = "{}"'.format('HLG', title))
    counter2 += 1
  except mariadb.Error as e:
    print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")
    
try:
  cursor.execute('DELETE FROM jsonStorage WHERE title = "dummy"')
  conn.commit()
except mariadb.Error as e:
  print(Fore.RED + f"There was an error during ROW DELETION: {e}")


