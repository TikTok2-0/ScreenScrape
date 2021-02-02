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


connectToDB()


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

createNewTable("jsonStorage", "titles")

cursor.execute("DELETE FROM jsonStorage")

cleanResultsHLG = ScrapeCleanup(resultsHLG)

while (counter < len(cleanResultsHLG)-1):
  if counter%2 == 0:
    titles.append(cleanResultsHLG[counter])
    counter = counter+1
  elif counter%2 != 0: 
    captions.append(cleanResultsHLG[counter])
    counter = counter+1

#print(titles)
#print(captions)

for title in titles:
    try:
        createRow("jsonStorage", "titles", title)
    except mariadb.Error as e:
        print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")
        
for caption in captions:
    try:
        createRow("jsonStorage", "captions", caption)
    except mariadb.Error as e:
        print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")
        
"""
for title in titles: 
  str(counterT)
  dictTestT['title{}'.format(counterT)] = title
  int(counterT)
  counterT += 1

print(dictTestT)

for caption in captions:
  str(counterC)
  dictTestC[counterC] = caption
  int(counterC)
  counterC += 1

while counterF < len(titles):
  str(counterF)
  #finalDict[dictTestT[counterF]] = dictTestC[counterF]
  int(counterF)
  counterF += 1
"""


#createNewTable("test01_2", "Column_A")
#createColumn("test01_2","Column_B")
#createRow("test01_2", "Column_A", "Value1")



