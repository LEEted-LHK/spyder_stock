import requests
from bs4 import BeautifulSoup
import re

def getHTMLText(url):
  try:
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text
  except:
    return ""

def getStockList(lst, url):
  html = getHTMLText(url)
  soup = BeautifulSoup(html, 'html.parser')
  a = soup.find_all('a')
  for i in a:
    try:
      href = i.attrs['href']
      lst.append(re.findall(r's[hz]\d{6}', href)[0])
    except:
      continue

def getStockInfo(lst, stockURL, filepath):
  f = open(filepath, 'w')
  for i in lst:
    try:
      uri = stockURL + i + '.html'
      html = getHTMLText(uri)
      if not html:
        continue
      soup = BeautifulSoup(html, 'html.parser')
      info = soup.find(attrs={'class': 'stock-info'})
      name = info.find(attrs={'class': 'bets-name'}).text.strip().split()[0]
      content = info.find_all('dl')
      dic = {}
      for i in content:
        key = i.find('dt').text
        value = i.find('dd').text.lstrip()
        dic[key] = value
      if not dic:
        dic = '未开'
      res = {name: dic}
      f.writelines(str(res)+'\n')
    except:
      continue
  f.close

if __name__ == '__main__':
  lstUrl = 'http://quote.eastmoney.com/stocklist.html'
  url = 'https://gupiao.baidu.com/stock/'
  filepath = 'F:/stock.txt'
  lst = []
  getStockList(lst, lstUrl)

  getStockInfo(lst, url, filepath)
  
  
  
  