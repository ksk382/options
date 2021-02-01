import requests
from bs4 import BeautifulSoup
import pandas as pd

site = 'https://etfdb.com/compare/volume/'

res = requests.get(site).text
soup = BeautifulSoup(res,'lxml')
df = pd.DataFrame([])
df['Ticker'] = []
for items in soup.find('table'):
    data = items.find_all('tr')
    for i in data:
        print (i)
        try:
            j = i.find_all('td')[0].text
            ticker = j
            df = df.append({'Ticker':ticker}, ignore_index=True)
        except Exception as e:
            print (str(e))

print (df)
df.to_csv('etf_ticker_list.csv', index=False)
