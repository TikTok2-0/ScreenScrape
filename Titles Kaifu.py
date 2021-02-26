from typing import Text
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
Text = []
lastSpace = 0
srcList = []
results = []
textSplit = []

URL2 = 'https://www.kaifu-gymnasium.de'
pageKFU = requests.get(URL2)
soupKFU = BeautifulSoup(pageKFU.content, 'html5lib')
resultsKFU = soupKFU('a')

#for item in resultsKFU:
    #print ('-------------\n',item, '\n\n')

for result in resultsKFU:
    convText = str(result)
    #print ('-------------\n',convText, '\n\n')
    if convText[3] == 'h':
        splitListFirst = convText.split('href="')
        linkContainer = splitListFirst[1]
        if linkContainer[12] == 'k' and linkContainer[13]=='a' and 'author' not in linkContainer and 'rel="' not in linkContainer and 'target="' not in linkContainer and 'src="' not in linkContainer and 'Impressum' not in linkContainer:
            linkContainer = linkContainer.split('">')
            linkContainer = linkContainer[0]
            srcList.append(linkContainer)

#print(srcList, len(srcList))

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
    results2.append(cleanText)
    #print (cleanText)
print(results2)
