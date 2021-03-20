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


#connectToDB()


URL_Src = 'https://www.hlg-hamburg.de'
pageSrc = requests.get(URL_Src)
soupSrc = BeautifulSoup(pageSrc.content, 'html5lib')
resultsSrc = soupSrc(class_="thumb")
cleanSrcList = []
results = []
cleanResults = []
cleanTextList = []
textSplit = []
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
    midResults = soup('article') 
    results.append(midResults) 

x = 0
cleanTextList2 = []
vielText = 'diese Seite ausdrucken Vorherige Artikel Zurück zur Übersicht Nächster Artikel'
for result in results:
    textSplit.clear()
    textConv = result[0].text
    textSplit = textConv.split('Kategorie', 6)
    x += 1
    cleanTextSplit = ''
    counter = 0
    cleanTextSplit = textSplit[1]
    cleanTextSplit = cleanTextSplit[58:-133]
    if cleanTextSplit[0].isupper() == False:
        cleanTextSplit = textSplit[1]
        cleanTextSplit = cleanTextSplit[57:-133]
    while cleanTextSplit[0] == ' ':
        cleanTextSplit = textSplit[1]
        cleanTextSplit = cleanTextSplit[58+counter:-133]
        counter += 1
    if cleanTextSplit[0] == '\n':
        cleanTextSplit = textSplit[1]
        cleanTextSplit = cleanTextSplit[60:-133]
    counter = 0
    cleanTextList.clear()
    cleanTextList.append(cleanTextSplit)
    if x < 7:
        for satz in cleanTextList:
            while "\t" in satz:
                satz = satz[:satz.find("\t")] + satz[satz.find("\t")+1:]
            while "  " in satz:
                satz = satz[:satz.find("  ")] + satz[satz.find("  ")+1:]
            while "\n\n" in satz:
                satz = satz[:satz.find("\n\n")] + satz[satz.find("\n\n")+1:]
            while vielText in satz:
                satz = satz[:satz.find(vielText)] + satz[satz.find(vielText)+78:]
            #print('SATZ', satz)
            cleanTextList2.append(satz)
cleanTextList = cleanTextList2

print(results)





srcList = []
results = []
textSplit = []

URL2 = 'https://www.kaifu-gymnasium.de'
pageKFU = requests.get(URL2)
soupKFU = BeautifulSoup(pageKFU.content, 'html5lib')
resultsKFU = soupKFU('a')

for result in resultsKFU:
    convText = str(result)
    if convText[3] == 'h':
        splitListFirst = convText.split('href="')
        linkContainer = splitListFirst[1]
        if linkContainer[12] == 'k' and linkContainer[13]=='a' and 'author' not in linkContainer and 'rel="' not in linkContainer and 'target="' not in linkContainer and 'src="' not in linkContainer and 'Impressum' not in linkContainer:
            linkContainer = linkContainer.split('">')
            linkContainer = linkContainer[0]
            srcList.append(linkContainer)

for URL in srcList:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html5lib')
    midResults = soup('article') 
    results.append(midResults)

results2 = []

for result in results:
    textSplit.clear()
    textConv = result[0].text
    while "\t" in textConv:
        textConv = textConv[:textConv.find("\t")] + textConv[textConv.find("\t")+1:]
    while "\n\n" in textConv:
        textConv = textConv[:textConv.find("\n\n")] + textConv[textConv.find('\n\n')+1:]
    if textConv[0] == '\n':
        textConv = str(textConv)[1:]
    cleanText = str(textConv)
    cleanText = cleanText[:-57]
    cleanTextList.append(cleanText)
"""
for item in cleanTextList:
  try:
    cursor.execute('UPDATE jsonStorage SET text = "{}" WHERE id = "{}"'.format(str(item), counter+1))
    conn.commit()
    counter += 1
  except mariadb.Error as e:
    print(Fore.RED + f"There was an error during DATA TRANSMISSION: {e}")
"""