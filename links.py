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
results = []
bigGay = []
bigQwinge = []
bigCocksInDave = []


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
    midResults = soup('article') 
    results.append(midResults) 

counter = 1

for result in results:
    #counter += 1
    bigGay.clear()
    #bigCocksInDave.clear()
    splitRContent = str(result).split('<div class="r-content">',1)
    result = splitRContent[1]
    splitDivEnd = result.split('</div>', 1)
    result = splitDivEnd[0]
    splitHref = result.split('href=')
    for split in splitHref:
        if split != splitHref[0]:
            bigGay.append(split)

    for item in bigGay:
        SplitItem = item.split('rel')
        item = SplitItem[0]
        if '">h' in item:
            SplitItem = item.split('">',1)
            item = SplitItem[0]
            item = item[+1:]
            bigCocksInDave.append([item, counter])
        else: 
            item = item[1:-2]
            bigCocksInDave.append([item, counter])
    counter += 1

counter = 0
for i in range (len(bigCocksInDave)-2):
    if bigCocksInDave[i][1] == bigCocksInDave[i+1][1]:
        bigCocksInDave[i][0] = bigCocksInDave[i][0], bigCocksInDave[i+1][0]
        bigCocksInDave.pop(i+1)
        #print(bigCocksInDave[i][0])

for item in bigCocksInDave:
  try:
    print(item[0])
    cursor.execute('UPDATE jsonStorage SET Links = "{}" WHERE id = "{}"'.format(str(item[0]), str(item[1])))
    conn.commit()
    counter += 1
  except mariadb.Error as e:
    print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")

    

