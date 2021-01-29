import requests
from bs4 import BeautifulSoup
import pandas as pd



site = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

res = requests.get(site).text
soup = BeautifulSoup(res,'lxml')
df = pd.DataFrame([])
df['Ticker'] = []
df['Date_added'] = []
for items in soup.find('table', class_='wikitable').find_all('tr')[1::1]:
    data = items.find_all(['th','td'])
    try:
        ticker = data[0].text.strip()
        date_added = data[6].text.strip()
        df = df.append({'Ticker':ticker, 'Date_added':date_added}, ignore_index=True)
        #print (ticker, date_added)
    except IndexError:pass

print (df)
df.to_csv('ticker_list.csv', index=False)

    #print("{}|{}|{}".format(country,title,name))
