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


connectToDB()


URL_Src = 'https://www.hlg-hamburg.de'
pageSrc = requests.get(URL_Src)
soupSrc = BeautifulSoup(pageSrc.content, 'html5lib')
resultsSrc = soupSrc(class_="thumb")
cleanSrcList = []
resultsDate = []
cleanResultsDate = []
resultsCat = []
cleanResultsCat = []
counter = 0

for result in resultsSrc:
    convText = str(result)
    splitListFirst = convText.split('href="')
    splitListSecond = splitListFirst[1].split('<img')
    linkContainer = splitListSecond[0]
    linkContainer = linkContainer[:-9]

    if '/2021/' in linkContainer:
        cleanSrcList.append(linkContainer)


for URL in cleanSrcList:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html5lib')
    midResultsDate = soup(class_= 'date') 
    resultsDate.append(midResultsDate) 

for result in resultsDate:
    midResultsDate = str(result).split('date">') 
    midResultDate = midResultsDate[1]
    midResultDate = midResultDate[:-8]
    cleanResultsDate.append(midResultDate)

cursor.execute("DELETE FROM jsonStorage WHERE dates")
conn.commit()

for item in cleanResultsDate:
  try:
    cursor.execute('UPDATE jsonStorage SET dates = "{}" WHERE id = "{}"'.format(str(item), counter+1))
    conn.commit()
    counter += 1
  except mariadb.Error as e:
    print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")



########     BREAK     ########
 


counter = 0

for URL in cleanSrcList:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html5lib')
    midResultsCat = soup(class_= 'category') 
    #print(midResultsCat)
    resultsCat.append(midResultsCat) 
x = 0
for result in resultsCat:
    midResultsCat = str(result).split('/">') 
    midResultCat = midResultsCat[1]
    midResultCat = midResultCat[:-23]
    if len(midResultCat) > 17:
       secondary = midResultCat.split('</a>')
       midResultCat = secondary[0]
    x += 1
    #print(midResultCat, x)
    cleanResultsCat.append(midResultCat)

cursor.execute("DELETE FROM jsonStorage WHERE category")
conn.commit()

for item in cleanResultsCat:
  try:
    cursor.execute('UPDATE jsonStorage SET category = "{}" WHERE id = "{}"'.format(str(item), counter+1))
    conn.commit()
    counter += 1
  except mariadb.Error as e:
    print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")

