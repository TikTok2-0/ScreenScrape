from re import escape
from bs4 import BeautifulSoup
import requests

URL = 'https://www.hlg-hamburg.de/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_='archive')
resultsText = str(results.text)

lenText = len(resultsText)

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
        if(satz == "weiterlesen"):
            stringArray.remove(satz)  

stringArray2 = []
for satz in stringArray:
    while "\n" in satz:
        satz = satz[:satz.find("\n")] + satz[satz.find("\n")+1:]
    stringArray2.append(satz)
    print(satz)
stringArray = stringArray2

print(stringArray)
        
