import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def scrapperForSetopati(URL = 'https://setopati.com/', category = 'social', save_in = 'Data-social'):
    page = requests.get(URL + category)
    soup = BeautifulSoup(page.content,"html.parser")
    
    next_page_link = soup.find('a', class_ = 'nextpostslink')
    print(next_page_link['href'])
    
    i=0
    while next_page_link is not None and i!=20: #first 20 page only
        all_news_link_nalt = soup.select('div.row.bishesh.news-cat-list > div.items.col-md-4 >a, div.row.bishesh.news-cat-list.alt > div.items.col-md-6 >a') 
        
        all_news_link =  all_news_link_nalt
        
        
        for link in all_news_link:
            print(link['href'])
            news_page = requests.get(link['href'])
            news_soup = BeautifulSoup(news_page.content,'html.parser')
            news_text = news_soup.find("div", class_='editor-box')
            now = datetime.now()
            filename = "setopati" + link['href'][-6:] + now.strftime("%d_%m_%y_%H_%M_%S")+ link['href'][-6:]
            with open("..\\16NepaliNews\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp:
                wp.write(news_text.text)
        
        next_page = requests.get(next_page_link['href']) #go to next page
        soup = BeautifulSoup(next_page.content, 'html.parser')
        next_page_link = soup.find_all("a", class_ = "nextpostslink")[-1]
        all_news_link = []
        print(next_page_link['href'])
        i += 1
        
# scrapperForSetopati(category='ghumphir',save_in='Tourism')