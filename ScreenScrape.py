import re
from bs4 import BeautifulSoup
import requests
import json

URL1 = 'https://www.hlg-hamburg.de'
pageHLG = requests.get(URL1)
soup = BeautifulSoup(pageHLG.content, 'html.parser')
resultsHLG = soup.find(class_='archive')
#print(resultsHLG)

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
    
cleanResultsHLG = ScrapeCleanup(resultsHLG)

counter = 0
titles = []
captions = []
    
while (counter < len(cleanResultsHLG)-1):
  if counter%2 == 0:
    titles.append(cleanResultsHLG[counter])
    counter = counter+1
  elif counter%2 != 0: 
    captions.append(cleanResultsHLG[counter])
    counter = counter+1
    
dictTestT = dict()
counterT = 0
for title in titles: 
  str(counterT)
  dictTestT[counterT] = title
  int(counterT)
  counterT += 1
  
dictTestC = dict()
counterC = 0
for caption in captions:
  str(counterC)
  dictTestC[counterC] = caption
  int(counterC)
  counterC += 1


finalDict = dict()
counterF = 0
while counterF < len(titles):
  str(counterF)
  finalDict[dictTestT[counterF]] = dictTestC[counterF]
  int(counterF)
  counterF += 1
  
print(finalDict)

dictOut = json.dumps(finalDict, indent = 2) 
with open("TitleCaption.json", "w") as outfile: 
    outfile.write(dictOut)