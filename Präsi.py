from bs4 import BeautifulSoup
import requests

URL1 = 'https://www.google.com'
page = requests.get(URL1)
soup = BeautifulSoup(page.content, 'html5lib')
results = soup.find('img')

print(results)