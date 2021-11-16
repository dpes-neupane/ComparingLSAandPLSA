import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os



def forReporters(URL = "https://www.reportersnepal.com/", category = "interview", save_in="interview"):
    page = requests.get(URL +"category/" + category) #can have different urls for different categories, so change as per need

    soup  = BeautifulSoup(page.content, "html.parser")
    # print(page.content)
    next_page_link = soup.select_one("ul.pagination.pagination-sm > li.page-item > i.page-link > a")
    print(next_page_link['href'])
    i = 0
    if not os.path.isdir(".\\16NepaliNews\\16719\\raw\\" + save_in):
        os.makedirs(".\\16NepaliNews\\16719\\raw\\" + save_in)
    while next_page_link is not None and i != 130: #get only 100 pages of links
        all_link_stories = soup.select("div.container > div.row.category > div.col-md-8.text-justify > a.post-list.d-flex")
        for link in all_link_stories:
            print(link['href'])
            news_page = requests.get(link['href'])
            news_soup = BeautifulSoup(news_page.content, 'html.parser')
            news_text = news_soup.find("article", class_=re.compile("post-entry")) #the divs with news text all belong to this class but also have others classes assigned to them
##            print(news_text.text)
            now = datetime.now()
            filename = now.strftime("%d_%m_%y_%H_%M_%S") + link['href'][-6:] + "reprtrnep"
            
            with open(".\\16NepaliNews\\16719\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: #saving 
                wp.write(news_text.text)
        
        next_page = requests.get(next_page_link['href']) #go to next page
        soup = BeautifulSoup(next_page.content, 'html.parser')
        next_page_link= soup.select("ul.pagination.pagination-sm > li.page-item > i.page-link > a")[-1]
        all_link_stories = []
        print(next_page_link['href'])
        i += 1

